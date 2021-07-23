from sqlalchemy import BigInteger, Column, Integer, SmallInteger, String, Text
from mylib.constants import MSG_KIND_ENTRY_EFFECT

from .normal_danmaku import BaseTable


class EntryEffectTable(BaseTable):
    ignored_columes = ['copy_writing']

    def _hash_row(self, row) -> str:
        return f'{row["uid"]}{row["target_id"]}{row["trigger_time"]}'

    @staticmethod
    def get_message_type():
        return MSG_KIND_ENTRY_EFFECT

    # def create_columns(self) -> list[Column]:
    #     return [
    #         Column('uid', BigInteger, comment="用户ID", nullable=False),
    #         Column('target_id', Integer, comment="真实房间号", nullable=False),
    #         Column('mock_effect', Integer, comment="未知", nullable=False),
    #         Column('face', Text, comment="用户头像URL", nullable=False),
    #         Column('privilege_type', SmallInteger, comment="舰队类型，0非舰队，1总督，2提督，3舰长", nullable=False),
    #         Column('copy_color', String(8), comment="未知", nullable=False),
    #         Column('highlight_color', String(8), comment="未知", nullable=False),
    #         Column('priority', SmallInteger, comment="未知", nullable=False),
    #         Column('basemap_url', Text, comment="背景条图片url", nullable=False),
    #         Column('show_avatar', SmallInteger, comment="未知", nullable=False),
    #         Column('effective_time', Integer, comment="未知", nullable=False),
    #         Column('web_basemap_url', Text, comment="未知", nullable=False),
    #         Column('web_effective_time', Integer, comment="未知", nullable=False),
    #         Column('web_effect_close', Integer, comment="未知", nullable=False),
    #         Column('web_close_time', Integer, comment="未知", nullable=False),
    #         Column('business', SmallInteger, comment="未知", nullable=False),
    #         Column('copy_writing_v2', String(128), comment="欢迎信息", nullable=False),
    #         Column('max_delay_time', Integer, comment="", nullable=False),
    #         Column('trigger_time', BigInteger, comment="", nullable=False),
    #         Column('identities', Integer, comment="", nullable=False),
    #     ]
