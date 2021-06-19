import argparse
import asyncio
from pathlib import Path
from sys import stderr
from pika import BasicProperties
from pika.exceptions import UnroutableError
import json
from collector.brdige import BLiveDMBridge
from mylib.mq import connect_message_queue
from mylib.constants import BODY_ADDON_KEY_ROOM_ID, MSG_KIND_GIFT, MSG_KIND_NORMAL, MSG_KIND_GUARD, MSG_KIND_SUPER_CHAT


def url_parse(st):
    from urllib.parse import urlparse
    u = urlparse('http://' + st)
    if u.username is None:
        raise argparse.ArgumentError("URL中没有用户名")
    if u.password is None:
        raise argparse.ArgumentError("URL中没有密码")
    if u.hostname is None:
        raise argparse.ArgumentError("URL中没有服务器IP或域名")
    if u.port is None:
        raise argparse.ArgumentError("URL中没有端口")
    return {"username": u.username, "password": u.password, "hostname": u.hostname, "port": u.port}


parser = argparse.ArgumentParser(description='直播弹幕数据收集')
parser.add_argument('rooms', metavar='id', nargs='+', type=int, help='直播间ID（URL结尾数字）')
parser.add_argument('--server', '-s', type=url_parse, help='消息队列服务器URL（用户名:密码@服务器:端口）', required=True)
parser.add_argument('--verbose', '-v', action='store_true', help='日志记录弹幕内容')
parser.add_argument('--filter', type=str, help='弹幕过滤器文件', default=None)
parser.add_argument('--cacert', type=str, help='（消息队列服务器）自签名根证书文件路径', default=None)
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


def create_log(room_id, kind, body):
    body = serialize_class(body)
    body[BODY_ADDON_KEY_ROOM_ID] = room_id
    content = json.dumps(body, ensure_ascii=False, check_circular=False).encode('utf8')
    try:
        rmq.basic_publish(exchange='',
                          routing_key=kind,
                          body=content,
                          properties=BasicProperties(content_type='application/json',
                                                     content_encoding='utf-8',
                                                     delivery_mode=2),
                          mandatory=True)
    except UnroutableError:
        print(f'Message was returned: {content}')

rmq = connect_message_queue(args.server, args.cacert)
clients = []
print(rmq.basic_publish('','', 'test publish'))


async def run(room_id):
    print(f'连接直播间：{room_id}')
    client = BLiveDMBridge(room_id, callback=create_log, log_dm=args.verbose, dm_filter=danmaku_filter)
    clients.append(client)
    await client.start()


async def stop_all():
    for client in clients:
        await client.close()
    rmq.close()


try:
    tasks = []
    for room_id in args.rooms:
        tasks.append(asyncio.ensure_future(run(room_id)))
    asyncio.get_event_loop().run_until_complete(asyncio.wait(tasks))
except KeyboardInterrupt:
    pass
except SystemExit:
    pass


asyncio.get_event_loop().run_until_complete(stop_all())
