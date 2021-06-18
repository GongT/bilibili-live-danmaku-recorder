"""
普通弹幕过滤器，复制到danmaku-filter.py并编写相应代码
"""
from re import match
from blivedm.blivedm import DanmakuMessage


def danmaku_filter(message: DanmakuMessage):
    """
    Returns:
        bool: 为True时保存此弹幕，否则忽略
    """
    if match(r"我要做.*的狗", message.msg):
        return True

    return False
