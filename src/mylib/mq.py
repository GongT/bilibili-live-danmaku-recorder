import ssl
import pika
from .constants import MSG_KIND_NORMAL, MSG_KIND_GIFT, MSG_KIND_GUARD, MSG_KIND_SUPER_CHAT


def connect_message_queue(u, tls_ca):
    credentials = pika.PlainCredentials(u['username'], u['password'])

    ssl_ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    ssl_ctx.verify_mode = ssl.CERT_REQUIRED
    if tls_ca:
        print(f"使用自签名证书: {tls_ca}")
        ssl_ctx.load_verify_locations(tls_ca)
        ssl_ctx.check_hostname = False
    else:
        print(f"使用系统证书")
        ssl_ctx.load_default_certs()

    connect_info = pika.ConnectionParameters(host=u['hostname'],
                                             port=u['port'],
                                             credentials=credentials,
                                             ssl_options=pika.SSLOptions(ssl_ctx))

    print(f"连接 RabbitMQ -> {u['hostname']}:{u['port']}")
    try:
        connection = pika.BlockingConnection(connect_info)
        if connection.is_open:
            print('  -- OK')
    except Exception as error:
        print('Error:', error.args)
        exit(1)
    rmq = connection.channel()
    rmq.queue_declare(queue=MSG_KIND_NORMAL, durable=True)
    rmq.queue_declare(queue=MSG_KIND_GIFT, durable=True)
    rmq.queue_declare(queue=MSG_KIND_GUARD, durable=True)
    rmq.queue_declare(queue=MSG_KIND_SUPER_CHAT, durable=True)
    rmq.confirm_delivery()
    return rmq
