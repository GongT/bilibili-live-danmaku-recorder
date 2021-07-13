from sys import stderr
from .blivedm.blivedm import BLiveClient, DanmakuMessage, GiftMessage, GuardBuyMessage, SuperChatMessage
from mylib.constants import MSG_KIND_GIFT, MSG_KIND_NORMAL, MSG_KIND_GUARD, MSG_KIND_SUPER_CHAT


def noop(*_args):
    pass


class BLiveDMBridge(BLiveClient):
    def __init__(self, room_id, callback, uid=0, log_dm=False, dm_filter=None):
        super().__init__(room_id, uid=uid, ssl=True)
        if not log_dm:
            self.debug_msg_log = noop
        self.dm_filter = dm_filter
        self.callback = callback

        async def __debug_show_data(self, command):
            print(command, file=stderr)

        handlers = BLiveClient._COMMAND_HANDLERS.copy()
        # handlers['STOP_LIVE_ROOM_LIST'] = None
        # handlers['WIDGET_BANNER'] = None
        # handlers['ONLINE_RANK_COUNT'] = None
        # handlers['ONLINE_RANK_V2'] = None
        # handlers['ONLINE_RANK_TOP3'] = None
        # handlers['HOT_RANK_CHANGED'] = None
        handlers['INTERACT_WORD'] = __debug_show_data
        handlers['ENTRY_EFFECT'] = __debug_show_data
        handlers['WELCOME_GUARD'] = __debug_show_data
        handlers['WELCOME'] = __debug_show_data
        handlers['room_admin_entrance'] = __debug_show_data
        self._COMMAND_HANDLERS = handlers

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
