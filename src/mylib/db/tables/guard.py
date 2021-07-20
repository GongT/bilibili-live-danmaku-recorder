from sqlalchemy import BigInteger, Column, Integer, SmallInteger, String
from mylib.constants import MSG_KIND_GUARD

from .normal_danmaku import BaseTable


class GuardTable(BaseTable):
    def hash_row(self, row) -> str:
        return f'{row["uid"]}{row["num"]}{row["gift_id"]}{row["end_time"]}'

    @staticmethod
    def get_table_kind():
        return MSG_KIND_GUARD

    def create_columns(self) -> list[Column]:
        return [
            Column('uid', BigInteger, comment='用户ID', nullable=False),
            Column('username', String(128), comment='用户名', nullable=False),
            Column('guard_level', SmallInteger, comment='舰队等级，0非舰队，1总督，2提督，3舰长', nullable=False),
            Column('num', Integer, comment='数量', nullable=False),
            Column('price', Integer, comment='单价金瓜子数', nullable=False),
            Column('gift_id', Integer, comment='礼物ID', nullable=False),
            Column('gift_name', String(128), comment='礼物名', nullable=False),
            Column('start_time', BigInteger, comment='开始时间戳？', nullable=False),
            Column('end_time', BigInteger, comment='结束时间戳？', nullable=False),
        ]
