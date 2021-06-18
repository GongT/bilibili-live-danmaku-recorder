import ssl
import pika
from config import config
from ..constants import MSG_KIND_NORMAL, MSG_KIND_GIFT, MSG_KIND_GUARD, MSG_KIND_SUPER_CHAT

credentials = pika.PlainCredentials(config.RMQ_USER, config.RMQ_PASS)

ssl_ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
ssl_ctx.load_verify_locations(config.RMQ_SERVER_CERT)
ssl_ctx.verify_mode = ssl.CERT_REQUIRED
ssl_ctx.check_hostname = False

connect_info = pika.ConnectionParameters(host=config.RMQ_SERVER,
                                         port=config.RMQ_PORT,
                                         credentials=credentials,
                                         ssl_options=pika.SSLOptions(ssl_ctx))

print("连接 RabbitMQ...")
connection = pika.BlockingConnection(connect_info)
rmq = connection.channel()
rmq.queue_declare(queue=MSG_KIND_NORMAL, durable=True)
rmq.queue_declare(queue=MSG_KIND_GIFT, durable=True)
rmq.queue_declare(queue=MSG_KIND_GUARD, durable=True)
rmq.queue_declare(queue=MSG_KIND_SUPER_CHAT, durable=True)
rmq.confirm_delivery()
