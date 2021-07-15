import argparse

from mylib.mq import add_arguments

parser = argparse.ArgumentParser(description='直播弹幕数据收集')
parser.add_argument('rooms', metavar='id', nargs='+', type=int, help='直播间ID（URL结尾数字）')
parser.add_argument('--verbose', '-v', action='store_true', help='日志记录弹幕内容')
parser.add_argument('--filter', type=str, help='弹幕过滤器文件', default=None)
add_arguments(parser)
parser.epilog = '【弹幕过滤器文件】 可指定一个python文件，其中包含filter函数，参数是blivedm.DanmakuMessage，返回布尔值，为False时直接忽略该弹幕。礼物等信息无条件记录，不会调用该函数。'

args = parser.parse_args()
