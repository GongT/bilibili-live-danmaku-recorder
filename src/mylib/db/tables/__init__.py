from abc import abstractmethod
from cachetools import cached, TTLCache
from sqlalchemy.engine import Connection
from sqlalchemy.sql.expression import select, text, insert
from mylib.db.connection import get_instance, create_table_if_not, table_name
from sqlalchemy import Column, Index, Integer, JSON, MetaData, String, TIMESTAMP, Table, func
from mylib.constants import DB_COL_EX_FIELD, DB_COL_HASH, DB_COL_PK, DB_COL_TIME
from mylib.db.helper import is_special_key


class BaseTable():
    ignored_columes: list[str] = []

    @abstractmethod
    def create_columns(self) -> list[Column]:
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

        columns = self.create_columns()
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
        original_data = data.copy()
        for col in self.table.columns:
            if is_special_key(col.key):
                continue

            if col.name in data:
                row[col.name] = data[col.name]
                del data[col.name]
                continue

            data_getter = getattr(self, 'get_column_' + col.name, None)
            if data_getter is None:
                if col.default or col.nullable:
                    continue
                else:
                    raise Exception(f"missing field {col.name}")

            ret = data_getter(original_data, col)
            if ret is None:
                raise Exception(f"missing field {col.name}")

            row[col.name] = ret

        for col_name in self.ignored_columes:
            del data[col_name]

        row[DB_COL_EX_FIELD] = data

        stmt = insert(self.table).values(row)
        ret = conn.execute(stmt)
        inserted_id = ret.inserted_primary_key
