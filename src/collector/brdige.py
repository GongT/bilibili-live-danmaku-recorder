from sys import stderr
from typing import Any, Callable
from .blivedm.blivedm import BLiveClient, DanmakuMessage, GiftMessage, GuardBuyMessage, SuperChatMessage
from mylib.constants import MSG_KIND_BATTLE_END, MSG_KIND_BATTLE_SETTLE, MSG_KIND_BATTLE_START, MSG_KIND_GIFT, MSG_KIND_NORMAL, MSG_KIND_GUARD, MSG_KIND_SUPER_CHAT, MSG_KIND_ENTRY_EFFECT, MSG_KIND_INTERACT_WORD

from collector.args import args


def debug(room: int, msg: str, *args):
    print(f'[{room}]' + msg, *args, file=stderr)


if not args.verbose:
    debug = lambda *_args: None


async def on_interact_word(roomid, message):
    uid = message['uid']
    un = message['uname']
    debug(roomid, f'欢迎用户 {un}({uid}) 进入直播间')
    return MSG_KIND_INTERACT_WORD


async def on_entry_effect(roomid, message):
    uid = message['uid']
    um = message['copy_writing_v2']
    debug(roomid, f'进场特效 [{uid}]: {um}')
    return MSG_KIND_ENTRY_EFFECT


async def on_battle_start(roomid, message):
    debug(roomid, "大乱斗开始", message)
    return MSG_KIND_BATTLE_START


async def on_battle_end(roomid, message):
    debug(roomid, "大乱斗结束", message)
    return MSG_KIND_BATTLE_END


async def on_battle_settle(roomid, message):
    debug(roomid, "大乱斗结算", message)
    return MSG_KIND_BATTLE_SETTLE


blacklist_message_ids = [
    'STOP_LIVE_ROOM_LIST',
    'WIDGET_BANNER',
    'ONLINE_RANK_COUNT',
    'ONLINE_RANK_V2',
    'ONLINE_RANK_TOP3',
    'HOT_RANK_CHANGED',
    'PK_BATTLE_SETTLE',
    'PK_BATTLE_PROCESS',
]


def debug_show_data(roomid: int, cmd: str, body):
    print("==================================\x1B[38;5;11m",
          cmd,
          "\x1B[0m==================================",
          file=stderr)
    print('[room]' + str(roomid), file=stderr)
    print(body, file=stderr)
    print("==================================\x1B[38;5;9m",
          cmd,
          "\x1B[0m==================================",
          file=stderr)


class BLiveDMBridge(BLiveClient):
    def __init__(self, room_id, callback, uid=0, dm_filter=None):
        super().__init__(room_id, uid=uid, ssl=True)
        self.dm_filter = dm_filter
        self.callback = callback

        handlers = BLiveClient._COMMAND_HANDLERS.copy()
        self._COMMAND_HANDLERS = handlers

        self.mute_unknown_messages(*blacklist_message_ids)
        self.development_watch_message('WELCOME_GUARD')
        self.development_watch_message('WELCOME')
        self.development_watch_message('room_admin_entrance')
        self.development_watch_message('COMMON_NOTICE_DANMAKU')
        self.development_watch_message('NOTICE_MSG')

        self.register_message_handler('INTERACT_WORD', on_interact_word)
        self.register_message_handler('ENTRY_EFFECT', on_entry_effect)

        self.register_message_handler('PK_BATTLE_PROCESS_NEW', on_battle_start)
        self.register_message_handler('PK_BATTLE_END', on_battle_end)
        self.development_watch_message('PK_BATTLE_SETTLE_USER')
        self.register_message_handler('PK_BATTLE_SETTLE_V2', on_battle_settle)

    async def _on_receive_danmaku(self, message: DanmakuMessage):
        if self.dm_filter is not None and self.dm_filter(message):
            debug(self.room_id, f'弹幕：{message.uname}：{message.msg}')
            await self.callback(self.room_id, MSG_KIND_NORMAL, message)
        else:
            debug(self.room_id, f'忽略弹幕：{message.uname}：{message.msg}')

    async def _on_receive_gift(self, message: GiftMessage):
        await self.callback(self.room_id, MSG_KIND_GIFT, message)
        debug(self.room_id,
              f'{message.uname} 赠送{message.gift_name}x{message.num} （{message.coin_type}币x{message.total_coin}）')

    async def _on_buy_guard(self, message: GuardBuyMessage):
        await self.callback(self.room_id, MSG_KIND_GUARD, message)
        debug(self.room_id, f'{message.username} 购买{message.gift_name}')

    async def _on_super_chat(self, message: SuperChatMessage):
        await self.callback(self.room_id, MSG_KIND_SUPER_CHAT, message)
        debug(self.room_id, f'醒目留言 ¥{message.price} {message.uname}：{message.message}')

    def register_message_handler(self, msg_type: str, handler: Callable[[int, Any], str]):
        async def _handler(s, raw):
            if 'data' in raw:
                data = raw['data']
            else:
                data = raw
            msgtype = await handler(self.room_id, data)
            if msgtype is None:
                return
            await self.callback(self.room_id, msgtype, data)

        self._COMMAND_HANDLERS[msg_type] = _handler

    def mute_unknown_messages(self, *msg_types: str):
        for msg_type in msg_types:
            self._COMMAND_HANDLERS[msg_type] = None

    def development_watch_message(self, *msg_types: str):
        async def _debug_show_data_wrap(s, raw):
            try:
                debug_show_data(self.room_id, raw['cmd'], raw['data'])
            except KeyError:
                debug_show_data(self.room_id, "???", raw)

        for msg_type in msg_types:
            self._COMMAND_HANDLERS[msg_type] = _debug_show_data_wrap
