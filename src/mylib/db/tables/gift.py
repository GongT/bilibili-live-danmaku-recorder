from sqlalchemy import BigInteger, Column, Integer, SmallInteger, String, Text
from mylib.constants import MSG_KIND_GIFT

from .normal_danmaku import BaseTable


class GiftTable(BaseTable):
    def _hash_row(self, row) -> str:
        return f'{row["uid"]}{row["num"]}{row["gift_id"]}{row["rnd"]}'

    @staticmethod
    def get_message_type():
        return MSG_KIND_GIFT

    # def create_columns(self) -> list[Column]:
    #     return [
    #         Column('gift_name', String(128), comment="礼物名", nullable=False),
    #         Column('num', Integer, comment="礼物数量", nullable=False),
    #         Column('uname', String(128), comment="用户名", nullable=False),
    #         Column('face', Text, comment="用户头像URL", nullable=False),
    #         Column('guard_level', SmallInteger, comment="舰队等级，0非舰队，1总督，2提督，3舰长", nullable=False),
    #         Column('uid', BigInteger, comment="用户ID", nullable=False),
    #         Column('timestamp', BigInteger, comment="时间戳", nullable=False),
    #         Column('gift_id', Integer, comment="礼物ID", nullable=False),
    #         Column('gift_type', Integer, comment="礼物类型（未知）", nullable=False),
    #         Column('action', String(32), comment="目前遇到的有'喂食'、'赠送'", nullable=False),
    #         Column('price', Integer, comment="礼物单价瓜子数", nullable=False),
    #         Column('rnd', String(64), comment="随机数", nullable=False),
    #         Column('coin_type', String(32), comment="瓜子类型，'silver'或'gold'", nullable=False),
    #         Column('total_coin', Integer, comment="总瓜子数", nullable=False),
    #     ]
