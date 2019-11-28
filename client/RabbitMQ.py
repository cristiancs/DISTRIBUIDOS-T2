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

    def __init__(self, callback):
        time.sleep(10)
        self.connection = pika.SelectConnection(
            pika.ConnectionParameters('rabbitmq_1'), on_open_callback=partial(
                self.onConnect, callback=callback), on_open_error_callback=self.connectionError)

        t = threading.Thread(target=self.connection.ioloop.start)
        t.start()

    def connectionError(self, error, err2):
        log(err2)

    def onConnect(self, interface, callback):
        log("Connected")
        self.status = "connected"
        callback()

    def getChannelNumber(self, channelName):
        if channelName not in self.channelNumbers.keys():
            self.channelNumbers[channelName] = self.currentIndexNumber
            self.currentIndexNumber += 1
        return self.channelNumbers[channelName]

    def getStatus(self):
        return self.status

    def start_consuming(self, frame):
        log("Queue of "+frame.method.queue+" cleared")
        # channel.basic_consume(
        #    queue=frame.method.queue, on_message_callback=handle_message_callback, auto_ack=False)
        #t = threading.Thread(target=new_channel.start_consuming)
        # t.start()
        # handle_opened_callback()

    def joinedChannel(self, new_channel, tojoin, handle_message_callback, handle_opened_callback):
        log("Joined "+tojoin)
        a = new_channel.queue_declare(self.start_consuming, "prueba123")
        log("Hola")

    def join_channel(self, tojoin, handle_message_callback, handle_opened_callback):
        log("Joining " + tojoin)
        channel = self.connection.channel(on_open_callback=partial(
            self.joinedChannel, tojoin=tojoin, handle_message_callback=handle_message_callback, handle_opened_callback=handle_opened_callback))

    def sendMessage(self, toChannel, user, message, userID, raw={}):
        log("Sending {message} to channel {toChannel} [{userID}]")
        now = datetime.now()
        toSend = {
            "uuid": str(uuid.uuid4()),
            "date": now.strftime("%D %H:%M:%S"),
            "to": user,
            "message": message,
            "userID": userID,
            **raw
        }
        channelNumber = self.getChannelNumber(toChannel)
        channel = self.connection.channel(channelNumber)
        channel.basic_publish(
            exchange='', routing_key=toChannel, body=json.dumps(toSend))
