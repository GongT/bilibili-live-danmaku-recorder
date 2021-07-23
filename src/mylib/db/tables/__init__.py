from abc import abstractmethod
from cachetools import cached, TTLCache
from sqlalchemy.engine import Connection
from sqlalchemy.sql.expression import select, text, insert
from sqlalchemy.util.langhelpers import md5_hex
from mylib.db.connection import get_instance, create_table_if_not
from sqlalchemy import Column, Index, Integer, JSON, MetaData, String, TIMESTAMP, Table, func
from mylib.constants import DB_COL_CONTENT, DB_COL_HASH, DB_COL_PK, DB_COL_TIME, DB_COL_TYPE


class BaseTable():
    ignored_columes: list[str] = []

    @abstractmethod
    def _hash_row(self, row) -> str:
        raise NotImplementedError()

    def hash_row(self, row) -> str:
        return md5_hex(self._hash_row(row) + ':' + self.get_message_type())

    @staticmethod
    @abstractmethod
    def get_message_type() -> str:
        raise NotImplementedError()

    def __init__(self, room_id: int) -> None:
        self.engine = get_instance()
        self.room_id = room_id

        self.metadata = MetaData()

        self.table = Table(
            str(room_id),
            self.metadata,
            Column(DB_COL_PK, Integer, primary_key=True, autoincrement=True),
            Column(DB_COL_HASH, String(32), nullable=True),
            Column(DB_COL_TYPE, String(32), nullable=False),
            Column(DB_COL_CONTENT, JSON(), nullable=False),
            Column(DB_COL_TIME, TIMESTAMP(), server_default=text('CURRENT_TIMESTAMP'), nullable=False),
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
        row[DB_COL_TYPE] = self.get_message_type()
        row[DB_COL_CONTENT] = data

        stmt = insert(self.table).values(row)
        ret = conn.execute(stmt)
        inserted_id = ret.inserted_primary_key
