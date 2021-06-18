import asyncio
from os import environ
from pathlib import Path
from sys import path, stderr
from pika import BasicProperties
from pika.exceptions import UnroutableError
import json

path.append(Path(__file__).parent.parent.as_posix())

from blivedm import blivedm
from config.config import LIVEROOM_ID
from mylib.mq import rmq
from mylib.constants import BODY_ADDON_KEY_ROOM_ID, MSG_KIND_GIFT, MSG_KIND_NORMAL, MSG_KIND_GUARD, MSG_KIND_SUPER_CHAT

if __name__ != '__main__':
    raise Exception("此文件必须直接运行")

if 'DEBUG' in environ and environ['DEBUG']:

    def debug_msg_log(msg: str):
        print(msg, file=stderr)
else:

    def debug_msg_log(msg: str):
        pass


try:
    from config.danmaku_filter import danmaku_filter
    print("使用弹幕过滤器")
except:
    print("无条件记录所有弹幕")

    def danmaku_filter(message: blivedm.DanmakuMessage):
        return True


def create_log(kind, body):
    body[BODY_ADDON_KEY_ROOM_ID] = client.room_id
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


def serialize_class(instance):
    ret = {}
    for attribute, value in instance.__dict__.items():
        ret[attribute] = value
    return ret


class MyBLiveClient(blivedm.BLiveClient):
    _COMMAND_HANDLERS = blivedm.BLiveClient._COMMAND_HANDLERS.copy()

    _COMMAND_HANDLERS['STOP_LIVE_ROOM_LIST'] = None
    _COMMAND_HANDLERS['WIDGET_BANNER'] = None
    _COMMAND_HANDLERS['ONLINE_RANK_COUNT'] = None
    _COMMAND_HANDLERS['ONLINE_RANK_V2'] = None
    _COMMAND_HANDLERS['HOT_RANK_CHANGED'] = None

    async def _on_receive_danmaku(self, message: blivedm.DanmakuMessage):
        if danmaku_filter(message):
            debug_msg_log(f'弹幕：{message.uname}：{message.msg}')
            create_log(MSG_KIND_NORMAL, serialize_class(message))
        else:
            debug_msg_log(f'忽略弹幕：{message.uname}：{message.msg}')

    async def _on_receive_gift(self, message: blivedm.GiftMessage):
        create_log(MSG_KIND_GIFT, serialize_class(message))
        debug_msg_log(
            f'{message.uname} 赠送{message.gift_name}x{message.num} （{message.coin_type}币x{message.total_coin}）')

    async def _on_buy_guard(self, message: blivedm.GuardBuyMessage):
        create_log(MSG_KIND_GUARD, serialize_class(message))
        debug_msg_log(f'{message.username} 购买{message.gift_name}')

    async def _on_super_chat(self, message: blivedm.SuperChatMessage):
        create_log(MSG_KIND_SUPER_CHAT, serialize_class(message))
        debug_msg_log(f'醒目留言 ¥{message.price} {message.uname}：{message.message}')


room_id = int(LIVEROOM_ID)
print(f'连接直播间：{room_id}')
client = MyBLiveClient(room_id, ssl=True)

try:
    asyncio.get_event_loop().run_until_complete(client.start())
except KeyboardInterrupt:
    pass

rmq.close()
asyncio.get_event_loop().run_until_complete(client.close())
