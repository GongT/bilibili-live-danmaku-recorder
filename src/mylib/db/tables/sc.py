from sqlalchemy import BigInteger, Column, Integer, SmallInteger, String, Text
from mylib.constants import MSG_KIND_SUPER_CHAT

from .normal_danmaku import BaseTable


class SuperChatTable(BaseTable):
    def hash_row(self, row) -> str:
        return f'{row["uid"]}{row["gift_id"]}{row["message"]}{row["start_time"]}'

    @staticmethod
    def get_table_kind():
        return MSG_KIND_SUPER_CHAT

    def create_columns(self) -> list[Column]:
        return [
            Column('price', Integer, comment='价格（人民币）', nullable=False),
            Column('message', String(200), comment='消息', nullable=False),
            Column('message_jpn', String(200), comment='消息日文翻译（目前只出现在SUPER_CHAT_MESSAGE_JPN）', nullable=False),
            Column('start_time', BigInteger, comment='开始时间戳', nullable=False),
            Column('end_time', BigInteger, comment='结束时间戳', nullable=False),
            Column('time', Integer, comment='剩余时间', nullable=False),
            Column('id', BigInteger, comment='消息ID，删除时用', nullable=False),
            Column('gift_id', Integer, comment='礼物ID', nullable=False),
            Column('gift_name', String(128), comment='礼物名', nullable=False),
            Column('uid', BigInteger, comment='用户ID', nullable=False),
            Column('uname', String(128), comment='用户名', nullable=False),
            Column('face', Text, comment='用户头像URL', nullable=False),
            Column('guard_level', SmallInteger, comment='舰队等级，0非舰队，1总督，2提督，3舰长', nullable=False),
            Column('user_level', Integer, comment='用户等级', nullable=False),
            Column('background_bottom_color', String(32), comment='底部背景色', nullable=False),
            Column('background_color', String(32), comment='背景色', nullable=False),
            Column('background_icon', Text, comment='背景图标', nullable=False),
            Column('background_image', Text, comment='背景图', nullable=False),
            Column('background_price_color', String(32), comment='背景价格颜色', nullable=False),
        ]
