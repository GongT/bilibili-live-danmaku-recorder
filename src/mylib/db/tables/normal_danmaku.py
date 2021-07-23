from sqlalchemy import BigInteger, Column, Integer, SmallInteger, String
from mylib.constants import MSG_KIND_NORMAL

from . import BaseTable


class NormalDanmakuTable(BaseTable):
    def _hash_row(self, row) -> str:
        return f'{row["timestamp"]}{row["msg"]}{row["uid"]}'

    @staticmethod
    def get_message_type():
        return MSG_KIND_NORMAL

    # def create_columns(self) -> list[Column]:
    #     return [
    #         Column('mode', SmallInteger, comment="弹幕显示模式（滚动、顶部、底部）", nullable=False),
    #         Column('font_size', SmallInteger, comment="字体尺寸", nullable=False),
    #         Column('color', Integer, comment="颜色", nullable=False),
    #         Column('timestamp', BigInteger, comment="时间戳", nullable=False),
    #         Column('rnd', String(64), comment="随机数", nullable=False),
    #         Column('uid_crc32', String(8), comment="用户ID文本的CRC32", nullable=False),
    #         Column('msg_type', SmallInteger, comment="是否礼物弹幕（节奏风暴）", nullable=False),
    #         Column('bubble', SmallInteger, comment="右侧评论栏气泡", nullable=False),
    #         Column('msg', String(200), comment="弹幕内容", nullable=False),
    #         Column('uid', BigInteger, comment="用户ID", nullable=False),
    #         Column('uname', String(128), comment="用户名", nullable=False),
    #         Column('admin', SmallInteger, comment="是否房管", nullable=False),
    #         Column('vip', SmallInteger, comment="是否月费老爷", nullable=False),
    #         Column('svip', SmallInteger, comment="是否年费老爷", nullable=False),
    #         Column('urank', Integer, comment="用户身份，用来判断是否正式会员，猜测非正式会员为5000，正式会员为10000", nullable=False),
    #         Column('mobile_verify', SmallInteger, comment="是否绑定手机", nullable=False),
    #         Column('uname_color', String(32), comment="用户名颜色"),  # ,nullable=False??
    #         Column('medal_level', Integer, comment="勋章等级", nullable=False),
    #         Column('medal_name', String(20), comment="勋章名", nullable=False),
    #         Column('runame', String(128), comment="勋章房间主播名", nullable=False),
    #         Column('room_id', Integer, comment="勋章房间ID", nullable=False),
    #         Column('mcolor', Integer, comment="勋章颜色", nullable=False),
    #         Column('special_medal', String(32), comment="特殊勋章", nullable=False),
    #         Column('user_level', Integer, comment="用户等级", nullable=False),
    #         Column('ulevel_color', Integer, comment="用户等级颜色", nullable=False),
    #         Column('ulevel_rank', String(32), comment="用户等级排名，>50000时为'>50000'", nullable=False),
    #         Column('old_title', String(32), comment="旧头衔", nullable=False),
    #         Column('title', String(32), comment="头衔", nullable=False),
    #         Column('privilege_type', SmallInteger, comment="舰队类型，0非舰队，1总督，2提督，3舰长", nullable=False),
    #     ]
