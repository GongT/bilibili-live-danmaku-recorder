from sys import stderr
from .blivedm.blivedm import BLiveClient, DanmakuMessage, GiftMessage, GuardBuyMessage, SuperChatMessage
from mylib.constants import MSG_KIND_GIFT, MSG_KIND_NORMAL, MSG_KIND_GUARD, MSG_KIND_SUPER_CHAT


def noop(*_args):
    pass


class BLiveDMBridge(BLiveClient):
    _COMMAND_HANDLERS = BLiveClient._COMMAND_HANDLERS.copy()

    _COMMAND_HANDLERS['STOP_LIVE_ROOM_LIST'] = None
    _COMMAND_HANDLERS['WIDGET_BANNER'] = None
    _COMMAND_HANDLERS['ONLINE_RANK_COUNT'] = None
    _COMMAND_HANDLERS['ONLINE_RANK_V2'] = None
    _COMMAND_HANDLERS['ONLINE_RANK_TOP3'] = None
    _COMMAND_HANDLERS['HOT_RANK_CHANGED'] = None

    def __init__(self, room_id, callback, uid=0, log_dm=False, dm_filter=None):
        super().__init__(room_id, uid=uid, ssl=True)
        if not log_dm:
            self.debug_msg_log = noop
        self.dm_filter = dm_filter
        self.callback = callback

    def debug_msg_log(self, room: int, msg: str):
        print(msg, file=stderr)

    async def _on_receive_danmaku(self, message: DanmakuMessage):
        if self.dm_filter is not None and self.dm_filter(message):
            self.debug_msg_log(self.room_id, f'弹幕：{message.uname}：{message.msg}')
            await self.callback(self.room_id, MSG_KIND_NORMAL, message)
        else:
            self.debug_msg_log(self.room_id, f'忽略弹幕：{message.uname}：{message.msg}')

    async def _on_receive_gift(self, message: GiftMessage):
        await self.callback(self.room_id, MSG_KIND_GIFT, message)
        self.debug_msg_log(
            self.room_id,
            f'{message.uname} 赠送{message.gift_name}x{message.num} （{message.coin_type}币x{message.total_coin}）')

    async def _on_buy_guard(self, message: GuardBuyMessage):
        await self.callback(self.room_id, MSG_KIND_GUARD, message)
        self.debug_msg_log(self.room_id, f'{message.username} 购买{message.gift_name}')

    async def _on_super_chat(self, message: SuperChatMessage):
        await self.callback(self.room_id, MSG_KIND_SUPER_CHAT, message)
        self.debug_msg_log(self.room_id, f'醒目留言 ¥{message.price} {message.uname}：{message.message}')
