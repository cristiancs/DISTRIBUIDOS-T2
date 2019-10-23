#!/usr/bin/env python
import pika
import time

connecting = True
while connecting:
    try:
        connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='rabbitmq_1'))
        connecting = False
    except Exception as e:
        print("Trying to connect to RabbitMQ")
        time.sleep(5)

channel = connection.channel()

channel.queue_declare(queue='hello')

channel.basic_publish(exchange='', routing_key='hello', body='Hello World!')
print(" [x] Sent 'Hello World!'")
connection.close()