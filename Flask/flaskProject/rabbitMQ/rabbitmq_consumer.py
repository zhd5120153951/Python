'''
@FileName   :rabbitmq_consumer.py
@Description:从RabbitMQ队列接受图像以及节点编码等信息
@Date       :2024/06/13 10:20:13
@Author     :曾贺东
@Copyright  :Greatech
@License    :None
@version    :1.0
@Email      :2462491568@qq.com
'''
import pika
import json
from multiprocessing import Process, Queue

# 从RabbitMQ队列获取数据


def consumeRabbitMQ(queue):
    # 设置RabbitMQ服务器的凭证（用户名和密码）
    creentials = pika.PlainCredentials("admin", "greatech")
    # 连接到RabbitMQ服务器，并提供凭证
    connection = pika.BlockingConnection(
        pika.ConnectionParameters('192.168.20.5', 5672, '/', creentials))
    # 创建一个新的channel
    channel = connection.channel()
    # 声明队列
    channel.queue_declare(queue='accept_queue')

    def callback(ch, method, properties, body):
        print(f"Received message: {body}")
        # 将消息放入共享队列中
        queue.put(json.loads(body))
        ch.basic_ack(delivery_tag=method.delivery_tag)

    channel.basic_consume(queue='accept_queue', on_message_callback=callback)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()

# 从队列中把数据post到统一接口服务


def sendQueue(queue):
    while True:


if __name__ == '__main__':
    shared_queue = Queue(maxsize=16)
    consumer_process = Process(target=consumeRabbitMQ, args=(shared_queue,))
    send_process = Process(target=sendQueue, args=(shared_queue,))
    consumer_process.start()
    send_process.start()
