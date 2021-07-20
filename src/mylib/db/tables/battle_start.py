from sqlalchemy import BigInteger, Column, Integer, JSON
from mylib.constants import MSG_KIND_BATTLE_START

from .normal_danmaku import BaseTable


class BattleStartTable(BaseTable):
    def hash_row(self, row) -> str:
        return f'{row["pk_id"]}'

    @staticmethod
    def get_table_kind():
        return MSG_KIND_BATTLE_START

    def get_column_target_room(self, msg):
        return msg['data']['match_info']['room_id']

    def create_columns(self) -> list[Column]:
        return [
            Column('pk_id', BigInteger, comment='乱斗序号', nullable=False),
            Column('data', JSON, comment='乱斗初始化数据', nullable=False),
            Column('target_room', BigInteger, comment='对手房间ID', nullable=False),
            Column('pk_status', Integer, comment='?', nullable=False),
            Column('timestamp', BigInteger, comment='?时间', nullable=False),
        ]
