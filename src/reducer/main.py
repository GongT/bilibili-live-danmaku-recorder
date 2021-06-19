from mylib.mq import rmq
from mylib.constants import MSG_KIND_GIFT, MSG_KIND_NORMAL, MSG_KIND_GUARD, MSG_KIND_SUPER_CHAT
from mylib.db. import

def callback(ch, method, properties, body):
    print(" [x] Received %r" % body.decode('utf-8'))


rmq.basic_consume(queue=MSG_KIND_GIFT, auto_ack=False, on_message_callback=callback)
rmq.basic_consume(queue=MSG_KIND_NORMAL, auto_ack=False, on_message_callback=callback)
rmq.basic_consume(queue=MSG_KIND_GUARD, auto_ack=False, on_message_callback=callback)
rmq.basic_consume(queue=MSG_KIND_SUPER_CHAT, auto_ack=False, on_message_callback=callback)

try:
    rmq.start_consuming()
except KeyboardInterrupt:
    pass

rmq.close()
