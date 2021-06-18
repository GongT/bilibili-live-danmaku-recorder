import asyncio
from mylib.db.record import record_table, connection, engine
from sqlalchemy import insert
from blivedm import blivedm
from config.config import LIVEROOM_ID

if __name__ != '__main__':
    raise Exception("此文件必须直接运行")

try:
    from config.danmaku_filter import danmaku_filter
    print("使用弹幕过滤器")
except:

    def danmaku_filter(message: blivedm.DanmakuMessage):
        return True


def create_log(kind: int, body):
    with connection.begin():
        ret = connection.execute(insert(record_table).values(raw_data=body, type=kind))
        print("inserted id: ", ret.inserted_primary_key[0])


def serialize_class(instance):
    ret = {}
    for attribute, value in instance.__dict__.items():
        ret[attribute] = value
    print(ret)
    return ret


class MyBLiveClient(blivedm.BLiveClient):
    async def _on_receive_danmaku(self, danmaku: blivedm.DanmakuMessage):
        if danmaku_filter(danmaku):
            print(f'弹幕：{danmaku.uname}：{danmaku.msg}')
            create_log(1, serialize_class(danmaku))
        else:
            print(f'忽略弹幕：{danmaku.uname}：{danmaku.msg}')

    async def _on_receive_gift(self, gift: blivedm.GiftMessage):
        print(f'{gift.uname} 赠送{gift.gift_name}x{gift.num} （{gift.coin_type}币x{gift.total_coin}）')

    async def _on_buy_guard(self, message: blivedm.GuardBuyMessage):
        print(f'{message.username} 购买{message.gift_name}')

    async def _on_super_chat(self, message: blivedm.SuperChatMessage):
        print(f'醒目留言 ¥{message.price} {message.uname}：{message.message}')


async def main():
    room_id = int(LIVEROOM_ID)
    print(f'连接直播间：{room_id}')
    client = MyBLiveClient(room_id, ssl=True)
    await client.start()


try:
    asyncio.get_event_loop().run_until_complete(main())
except KeyboardInterrupt:
    connection.close()
