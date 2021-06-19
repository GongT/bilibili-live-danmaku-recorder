from blivedm.blivedm import DanmakuMessage


def filter(dm: DanmakuMessage):
    msg = str(dm.msg)
    if msg.find('(') >= 0:
        return False

    if len(msg.replace('?', '').strip()) == 0:
        return False
    if len(msg.replace('？', '').strip()) == 0:
        return False

    return True
