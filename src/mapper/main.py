import json
import argparse
from time import time
from sys import stderr
from pika import spec
from pika.adapters.blocking_connection import BlockingChannel
from sqlalchemy.util.langhelpers import md5_hex
from mylib.mq import add_arguments, connect_message_queue
from mylib.db import create_connection, find_table
from mylib.constants import MSG_KIND_GIFT, MSG_KIND_NORMAL, MSG_KIND_GUARD, MSG_KIND_SUPER_CHAT, BODY_ADDON_KEY_ROOM_ID


def split_room_id(body):
    return body.pop(BODY_ADDON_KEY_ROOM_ID)


def handle_inner(kind: str, body: bytes):
    json_data = json.loads(body.decode('utf-8'))
    room_id = split_room_id(json_data)

    table = find_table(kind, room_id)
    if table is None:
        raise Exception(f"invalid message kind: {kind}")

    hash = md5_hex(table.hash_row(json_data))

    with engine.connect().execution_options(autocommit=True) as conn:
        exists = table.find_hash(conn, hash)
        if exists:
            return
        # print(f"[{hash}] <<< {room_id} | {kind} <<< {json_data}")
        table.do_insert(conn, hash, json_data)
        conn.commit()


def callback(kind: str, ch: BlockingChannel, method: spec.Basic.Deliver, properties: spec.BasicProperties, body: bytes):
    try:
        handle_inner(kind, body)
    except Exception as e:
        print("failed handle message:", type(e).__name__, end='', file=stderr)
        for i in e.args:
            print(' ' + str(i), end='', file=stderr)

        print(" | " + body.decode('utf-8'), file=stderr)
        ch.basic_nack(method.delivery_tag)
    else:
        # ch.basic_ack(method.delivery_tag)
        pass


def register_handler(kind):
    cb = lambda *args: callback(kind, *args)
    rmq.basic_consume(queue=kind, auto_ack=False, on_message_callback=cb)


parser = argparse.ArgumentParser(description='直播弹幕数据保存')
add_arguments(parser)
parser.add_argument('--database', type=str, help='...', required=True)
args = parser.parse_args()

engine = create_connection(args.database)
rmq = connect_message_queue(args.server, args.cacert)

register_handler(MSG_KIND_GIFT)
# register_handler(MSG_KIND_NORMAL)
# register_handler(MSG_KIND_GUARD)
# register_handler(MSG_KIND_SUPER_CHAT)

try:
    rmq.start_consuming()
except KeyboardInterrupt:
    pass

rmq.close()
