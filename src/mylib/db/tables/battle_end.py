from sqlalchemy import BigInteger, Column, Integer, JSON
from sqlalchemy.sql.sqltypes import SmallInteger
from mylib.constants import MSG_KIND_BATTLE_END

from .normal_danmaku import BaseTable


class BattleEndTable(BaseTable):
    def _hash_row(self, row) -> str:
        return f'{row["pk_id"]}'

    @staticmethod
    def get_message_type():
        return MSG_KIND_BATTLE_END

    # def create_columns(self) -> list[Column]:
    #     return [
    #         Column('pk_id', BigInteger, comment='乱斗序号', nullable=False),
    #         Column('data', JSON, comment='乱斗初始化数据', nullable=False),
    #         Column('target_room', BigInteger, comment='对手房间ID', nullable=False),
    #         Column('winner', SmallInteger, comment='胜者 0：对方，1：己方', nullable=False),
    #         Column('pk_status', Integer, comment='?', nullable=False),
    #         Column('timestamp', BigInteger, comment='?时间', nullable=False),
    #     ]
