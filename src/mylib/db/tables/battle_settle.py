from sqlalchemy import BigInteger, Column, Integer, JSON
from sqlalchemy.sql.sqltypes import SmallInteger
from mylib.constants import MSG_KIND_BATTLE_END, MSG_KIND_BATTLE_SETTLE

from .normal_danmaku import BaseTable


class BattleSettleTable(BaseTable):
    def hash_row(self, row) -> str:
        return f'{row["pk_id"]}'

    @staticmethod
    def get_table_kind():
        return MSG_KIND_BATTLE_SETTLE

    def get_column_winner(self, msg, col):
        return msg['data']['init_info']['winner_type'] > 0

    def create_columns(self) -> list[Column]:
        return [
            Column('pk_id', BigInteger, comment='乱斗序号', nullable=False),
            Column('data', JSON, comment='乱斗初始化数据', nullable=False),
            Column('settle_status', SmallInteger, comment='状态', nullable=False),
            Column('pk_status', Integer, comment='?', nullable=False),
            Column('timestamp', BigInteger, comment='?时间', nullable=False),
        ]
