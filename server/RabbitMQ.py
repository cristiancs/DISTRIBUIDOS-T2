import pika
import time
import uuid
from datetime import datetime
import json
import threading
from functools import partial


def log(message, show=True):
    if show:
        print(message)


class RabbitMQ:
    status = "idle"
    channels = {}
    currentIndexNumber = 0

    def __init__(self):
        while self.status != "connected":
            try:
                self.connection = pika.BlockingConnection(
                    pika.ConnectionParameters('rabbitmq_1'))
                self.status = "connected"
            except Exception as e:
                log("Trying in 2 seconds")
                time.sleep(2)

    def join_channel(self, tojoin, handle_message_callback, handle_on_channel_open=""):
        self.channel = self.connection.channel()  # start a channel
        self.channel.queue_declare(
            queue=tojoin, durable=True)  # Declare a queue
        self.channel.basic_consume(tojoin,
                                   handle_message_callback,
                                   auto_ack=False)
        if(handle_on_channel_open != ""):
            handle_on_channel_open()
        self.channel.start_consuming()

    def close(self):
        self.connection.close()

    def sendMessage(self, toChannel, userTo, message, userID, raw={}):
        now = datetime.now()
        toSend = {
            "uuid": str(uuid.uuid4()),
            "date": now.strftime("%D %H:%M:%S"),
            "to": userTo,
            "message": message,
            "userID": userID,
            **raw
        }
        log(f"Sending {toSend}")
        self.channel.basic_publish(
            exchange='', routing_key=toChannel, body=json.dumps(toSend))
