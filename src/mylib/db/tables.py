from abc import abstractmethod
from cachetools import cached, TTLCache
from sqlalchemy.engine import Connection
from sqlalchemy.sql.expression import select, text, insert
from sqlalchemy.engine.cursor import CursorResult
from mylib.db.connection import get_instance, create_table_if_not, table_name
from sqlalchemy import func, Column, Integer, BigInteger, TIMESTAMP, String, JSON, MetaData, Table, Index, SmallInteger, Text
from mylib.constants import DB_COL_EX_FIELD, DB_COL_HASH, DB_COL_PK, DB_COL_TIME, MSG_KIND_GIFT, MSG_KIND_NORMAL, MSG_KIND_GUARD, MSG_KIND_SUPER_CHAT


def is_special_key(k: str):
    return k == DB_COL_PK or k == DB_COL_HASH or k == DB_COL_EX_FIELD or k == DB_COL_TIME


class BaseTable():
    @abstractmethod
    def create_columns(self, room_id: int) -> list[Column]:
        raise NotImplementedError()

    @abstractmethod
    def hash_row(self, row) -> str:
        raise NotImplementedError()

    @staticmethod
    @abstractmethod
    def get_table_kind() -> str:
        raise NotImplementedError()

    def __init__(self, room_id: int) -> None:
        self.engine = get_instance()
        self.room_id = room_id

        self.table_name = table_name(room_id, self.get_table_kind())
        self.metadata = MetaData()

        columns = self.create_columns(room_id)
        self.table = Table(
            self.table_name,
            self.metadata,
            Column(DB_COL_PK, Integer, primary_key=True, autoincrement=True),
            Column(DB_COL_HASH, String(32), nullable=False),
            *columns,
            Column(DB_COL_EX_FIELD, JSON(), nullable=False),
            Column(DB_COL_TIME, TIMESTAMP(), server_default=text('CURRENT_TIMESTAMP'), nullable=False),
            mariadb_engine='InnoDB',
            mariadb_charset='utf8mb4',
        )

        Index('line_hash', self.table.c[DB_COL_HASH], mysql_using='hash', mariadb_using='hash', unique=True)

        create_table_if_not(self.engine, self.table)

    @cached(cache=TTLCache(maxsize=1024, ttl=30))
    def find_hash(self, conn: Connection, hash: str) -> bool:
        stmt = select(func.count()).select_from(self.table).where(self.table.c[DB_COL_HASH] == hash)
        ret = conn.execute(stmt)
        return ret.first()[0] > 0

    def do_insert(self, conn, hash: str, data: dict):
        row = {}
        row[DB_COL_HASH] = hash
        for col in self.table.columns:
            if is_special_key(col.key):
                continue
            if col.name not in data:
                raise Exception(f"missing field {col.name}")

            row[col.name] = data[col.name]
            del data[col.name]
        row[DB_COL_EX_FIELD] = data

        stmt = insert(self.table).values(row)
        inserted_id = conn.execute(stmt).inserted_primary_key


class NormalDanmakuTable(BaseTable):
    def hash_row(self, row) -> str:
        return f'{row["timestamp"]}{row["msg"]}{row["uid"]}'

    @staticmethod
    def get_table_kind():
        return MSG_KIND_NORMAL

    def create_columns(self, room_id: int) -> list[Column]:
        return [
            Column('mode', SmallInteger, comment="弹幕显示模式（滚动、顶部、底部）", nullable=False),
            Column('font_size', SmallInteger, comment="字体尺寸", nullable=False),
            Column('color', Integer, comment="颜色", nullable=False),
            Column('timestamp', BigInteger, comment="时间戳", nullable=False),
            Column('rnd', String(64), comment="随机数", nullable=False),
            Column('uid_crc32', String(8), comment="用户ID文本的CRC32", nullable=False),
            Column('msg_type', SmallInteger, comment="是否礼物弹幕（节奏风暴）", nullable=False),
            Column('bubble', SmallInteger, comment="右侧评论栏气泡", nullable=False),
            Column('msg', String(200), comment="弹幕内容", nullable=False),
            Column('uid', BigInteger, comment="用户ID", nullable=False),
            Column('uname', String(128), comment="用户名", nullable=False),
            Column('admin', SmallInteger, comment="是否房管", nullable=False),
            Column('vip', SmallInteger, comment="是否月费老爷", nullable=False),
            Column('svip', SmallInteger, comment="是否年费老爷", nullable=False),
            Column('urank', Integer, comment="用户身份，用来判断是否正式会员，猜测非正式会员为5000，正式会员为10000", nullable=False),
            Column('mobile_verify', SmallInteger, comment="是否绑定手机", nullable=False),
            Column('uname_color', String(32), comment="用户名颜色"),  # ,nullable=False??
            Column('medal_level', Integer, comment="勋章等级", nullable=False),
            Column('medal_name', String(20), comment="勋章名", nullable=False),
            Column('runame', String(128), comment="勋章房间主播名", nullable=False),
            Column('room_id', Integer, comment="勋章房间ID", nullable=False),
            Column('mcolor', Integer, comment="勋章颜色", nullable=False),
            Column('special_medal', String(32), comment="特殊勋章", nullable=False),
            Column('user_level', Integer, comment="用户等级", nullable=False),
            Column('ulevel_color', Integer, comment="用户等级颜色", nullable=False),
            Column('ulevel_rank', String(32), comment="用户等级排名，>50000时为'>50000'", nullable=False),
            Column('old_title', String(32), comment="旧头衔", nullable=False),
            Column('title', String(32), comment="头衔", nullable=False),
            Column('privilege_type', SmallInteger, comment="舰队类型，0非舰队，1总督，2提督，3舰长", nullable=False),
        ]


class GiftTable(BaseTable):
    def hash_row(self, row) -> str:
        return f'{row["uid"]}{row["gift_id"]}{row["timestamp"]}{row["rnd"]}'

    @staticmethod
    def get_table_kind():
        return MSG_KIND_GIFT

    def create_columns(self, room_id: int) -> list[Column]:
        return [
            Column('gift_name', String(128), comment="礼物名", nullable=False),
            Column('num', Integer, comment="礼物数量", nullable=False),
            Column('uname', String(128), comment="用户名", nullable=False),
            Column('face', Text, comment="用户头像URL", nullable=False),
            Column('guard_level', Integer, comment="舰队等级，0非舰队，1总督，2提督，3舰长", nullable=False),
            Column('uid', BigInteger, comment="用户ID", nullable=False),
            Column('timestamp', BigInteger, comment="时间戳", nullable=False),
            Column('gift_id', Integer, comment="礼物ID", nullable=False),
            Column('gift_type', Integer, comment="礼物类型（未知）", nullable=False),
            Column('action', String(32), comment="目前遇到的有'喂食'、'赠送'", nullable=False),
            Column('price', Integer, comment="礼物单价瓜子数", nullable=False),
            Column('rnd', String(64), comment="随机数", nullable=False),
            Column('coin_type', String(32), comment="瓜子类型，'silver'或'gold'", nullable=False),
            Column('total_coin', Integer, comment="总瓜子数", nullable=False),
        ]


cache = {}


def find_table(kind: str, room_id: int):
    if kind in cache and room_id in cache[kind]:
        return cache[kind][room_id]

    print(f'Init table: {kind} -> {room_id}')
    if kind == MSG_KIND_NORMAL:
        ins = NormalDanmakuTable(room_id)
    elif kind == MSG_KIND_GIFT:
        ins = GiftTable(room_id)
    # elif kind==MSG_KIND_GUARD:
    # elif kind==MSG_KIND_SUPER_CHAT:
    else:
        return None
    if kind not in cache:
        cache[kind] = {}
    cache[kind][room_id] = ins
    return ins
