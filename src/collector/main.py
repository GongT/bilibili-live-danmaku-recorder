import signal
import argparse
import asyncio
from pathlib import Path
from sys import stderr
from pika import BasicProperties
from pika.exceptions import UnroutableError, AMQPConnectionError, ChannelClosed, ChannelWrongStateError
import json
from collector.brdige import BLiveDMBridge
from mylib.mq import connect_message_queue, add_arguments
from mylib.constants import BODY_ADDON_KEY_ROOM_ID, MSG_KIND_GIFT, MSG_KIND_NORMAL, MSG_KIND_GUARD, MSG_KIND_SUPER_CHAT

parser = argparse.ArgumentParser(description='直播弹幕数据收集')
parser.add_argument('rooms', metavar='id', nargs='+', type=int, help='直播间ID（URL结尾数字）')
parser.add_argument('--verbose', '-v', action='store_true', help='日志记录弹幕内容')
parser.add_argument('--filter', type=str, help='弹幕过滤器文件', default=None)
add_arguments(parser)
parser.epilog = '【弹幕过滤器文件】 可指定一个python文件，其中包含filter函数，参数是blivedm.DanmakuMessage，返回布尔值，为False时直接忽略该弹幕。礼物等信息无条件记录，不会调用该函数。'

args = parser.parse_args()


def danmaku_filter():
    return True


if args.filter is not None:
    from importlib.util import spec_from_file_location, module_from_spec
    from pathlib import Path
    from os.path import splitext
    import sys
    f = Path(args.filter).absolute()
    if not f.is_file():
        print("过滤器文件不存在: " + f.as_posix())
        exit(1)
    sys.path.insert(0, f.parent.as_posix())
    spec = spec_from_file_location(splitext(f.name)[0], f.as_posix())
    mdl = module_from_spec(spec)
    sys.modules["danmaku_filter"] = mdl
    spec.loader.exec_module(mdl)
    danmaku_filter = getattr(mdl, 'filter')
    if danmaku_filter is None:
        print("过滤器文件错误，需要定义filter函数")
        exit(1)


def serialize_class(instance):
    ret = {}
    for attribute, value in instance.__dict__.items():
        ret[attribute] = value
    return ret


lock = asyncio.Lock()


async def create_log(room_id, kind, body):
    global rmq
    body = serialize_class(body)
    body[BODY_ADDON_KEY_ROOM_ID] = room_id
    content = json.dumps(body, ensure_ascii=False, check_circular=False).encode('utf8')

    tryies = 0
    while True:
        try:
            rmq.basic_publish(exchange='',
                              routing_key=kind,
                              body=content,
                              properties=BasicProperties(content_type='application/json',
                                                         content_encoding='utf-8',
                                                         delivery_mode=2),
                              mandatory=True)
        except UnroutableError:
            print(f'message was rejected: {content}', file=stderr)
        except (AMQPConnectionError, ChannelClosed, ConnectionResetError, ChannelWrongStateError) as error:
            tryies += 1
            print(f'connection lost: {error}, try to reconnect ({tryies} times)...')
            await asyncio.sleep(1)
            async with lock:
                if rmq.is_closed:
                    rmq = connect_message_queue(args.server, args.cacert)
            continue
        except Exception as e:
            print("<FATAL> publish rabbitmq failed:", type(e), e)
            exit(1)
        break


rmq = connect_message_queue(args.server, args.cacert)
clients = []


async def run(room_id):
    print(f'连接直播间：{room_id}')
    client = BLiveDMBridge(room_id, callback=create_log, log_dm=args.verbose, dm_filter=danmaku_filter)
    clients.append(client)
    await client.start()


async def stop_all():
    for client in clients:
        await client.close()
    rmq.close()


def signal_handler(*args):
    asyncio.get_event_loop().run_until_complete(stop_all())


signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

try:
    tasks = []
    for room_id in args.rooms:
        tasks.append(asyncio.ensure_future(run(room_id)))
    asyncio.get_event_loop().run_until_complete(asyncio.wait(tasks))
except KeyboardInterrupt:
    pass

asyncio.get_event_loop().run_until_complete(stop_all())
