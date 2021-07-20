from mylib.db.tables.battle_end import BattleEndTable
from mylib.db.tables.battle_settle import BattleSettleTable
from mylib.db.tables.battle_start import BattleStartTable
from mylib.db.tables.interact_word import InteractWordTable
from .tables.entry_effect import EntryEffectTable
from .tables.normal_danmaku import NormalDanmakuTable
from .tables.gift import GiftTable
from .tables.sc import SuperChatTable
from .tables.guard import GuardTable
from mylib.constants import MSG_KIND_BATTLE_END, MSG_KIND_BATTLE_SETTLE, MSG_KIND_BATTLE_START, MSG_KIND_ENTRY_EFFECT, MSG_KIND_GIFT, MSG_KIND_GUARD, MSG_KIND_INTERACT_WORD, MSG_KIND_NORMAL, MSG_KIND_SUPER_CHAT

cache = {}


def find_table(kind: str, room_id: int):
    if kind in cache and room_id in cache[kind]:
        return cache[kind][room_id]

    print(f'Init table: {kind} -> {room_id}')
    if kind == MSG_KIND_NORMAL:
        ins = NormalDanmakuTable(room_id)
    elif kind == MSG_KIND_GIFT:
        ins = GiftTable(room_id)
    elif kind == MSG_KIND_GUARD:
        ins = GuardTable(room_id)
    elif kind == MSG_KIND_SUPER_CHAT:
        ins = SuperChatTable(room_id)
    elif kind == MSG_KIND_ENTRY_EFFECT:
        ins = EntryEffectTable(room_id)
    elif kind == MSG_KIND_INTERACT_WORD:
        ins = InteractWordTable(room_id)
    elif kind == MSG_KIND_BATTLE_START:
        ins = BattleStartTable(room_id)
    elif kind == MSG_KIND_BATTLE_END:
        ins = BattleEndTable(room_id)
    elif kind == MSG_KIND_BATTLE_SETTLE:
        ins = BattleSettleTable(room_id)
    else:
        return None
    if kind not in cache:
        cache[kind] = {}
    cache[kind][room_id] = ins
    return ins
