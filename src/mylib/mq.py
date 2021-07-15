from argparse import ArgumentParser
import argparse
from os import environ
import ssl
import pika
from .constants import MSG_KIND_NORMAL, MSG_KIND_GIFT, MSG_KIND_GUARD, MSG_KIND_SUPER_CHAT, MSG_KIND_INTERACT_WORD, MSG_KIND_ENTRY_EFFECT, MSG_KIND_BATTLE_START, MSG_KIND_BATTLE_END, MSG_KIND_BATTLE_SETTLE

QUEUE_NAMES = [
    MSG_KIND_NORMAL, MSG_KIND_GIFT, MSG_KIND_GUARD, MSG_KIND_SUPER_CHAT, MSG_KIND_INTERACT_WORD, MSG_KIND_ENTRY_EFFECT,
    MSG_KIND_BATTLE_START, MSG_KIND_BATTLE_END, MSG_KIND_BATTLE_SETTLE
]


def connect_message_queue(u, tls_ca):
    username = u['username']
    password = u['password']
    credentials = pika.PlainCredentials(username, password)

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

    print(f"连接 RabbitMQ -> {username}:{password}@{u['hostname']}:{u['port']}")
    try:
        connection = pika.BlockingConnection(connect_info)
        if connection.is_open:
            print('  -- OK')
    except Exception as error:
        print('Error:', error.args)
        exit(1)
    rmq = connection.channel()

    for i in QUEUE_NAMES:
        rmq.queue_declare(queue=i, durable=True)

    rmq.confirm_delivery()
    return rmq


def url_parse(st):
    from urllib.parse import urlparse
    u = urlparse('http://' + st)
    if u.username is None:
        raise argparse.ArgumentError("URL中没有用户名")
    if u.password is None:
        raise argparse.ArgumentError("URL中没有密码")
    if u.hostname is None:
        raise argparse.ArgumentError("URL中没有服务器IP或域名")
    if u.port is None:
        raise argparse.ArgumentError("URL中没有端口")
    return {"username": u.username, "password": u.password, "hostname": u.hostname, "port": u.port}


def add_arguments(parser: argparse.ArgumentParser):
    parser.add_argument('--server', '-s', type=url_parse, help='消息队列服务器URL（用户名:密码@服务器:端口）', required=True)
    parser.add_argument('--cacert', type=str, help='（消息队列服务器）自签名根证书文件路径', default=None)
