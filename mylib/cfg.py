from config import config

sep = getattr(config, 'TABLE_SEP', '__')

TABLE_NAME_NORMAL = config.LIVEROOM_ID + sep + getattr(config, 'DM_TABLE_NORMAL', 'danmaku')
TABLE_NAME_GIFT = config.LIVEROOM_ID + sep + getattr(config, 'DM_TABLE_GIFT', 'gift')
TABLE_NAME_GUARD = config.LIVEROOM_ID + sep + getattr(config, 'DM_TABLE_GUARD', 'guard')
TABLE_NAME_SUPER_CHAT = config.LIVEROOM_ID + sep + getattr(config, 'DM_TABLE_SUPER_CHAT', 'super_chat')

TABLE_NAME_RECORD = config.LIVEROOM_ID + sep + getattr(config, 'DM_TABLE_RECORD', 'record')
