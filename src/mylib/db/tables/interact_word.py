from sqlalchemy import BigInteger, Column, Integer, JSON, String, Text
from mylib.constants import MSG_KIND_INTERACT_WORD

from .normal_danmaku import BaseTable


class InteractWordTable(BaseTable):
    ignored_columes = []

    def hash_row(self, row) -> str:
        return f'{row["uid"]}{row["roomid"]}{row["timestamp"]}'

    @staticmethod
    def get_table_kind():
        return MSG_KIND_INTERACT_WORD

    def create_columns(self) -> list[Column]:
        return [
            Column('contribution', JSON, comment="?", nullable=False),
            Column('dmscore', Integer, comment="?", nullable=False),
            Column('fans_medal', JSON, comment="粉丝牌", nullable=False),
            Column('identities', JSON, comment="?", nullable=False),
            Column('is_spread', JSON, comment="?", nullable=False),
            Column('msg_type', JSON, comment="?", nullable=False),
            Column('roomid', JSON, comment="真实房间号", nullable=False),
            Column('score', JSON, comment="?", nullable=False),
            Column('spread_desc', Text, comment="?", nullable=False),
            Column('spread_info', Text, comment="?", nullable=False),
            Column('tail_icon', Integer, comment="?", nullable=False),
            Column('timestamp', BigInteger, comment="", nullable=False),
            Column('trigger_time', BigInteger, comment="?", nullable=False),
            Column('uid', BigInteger, comment='用户ID', nullable=False),
            Column('uname', String(128), comment='用户名', nullable=False),
            Column('uname_color', String(8), comment="", nullable=False),
        ]
