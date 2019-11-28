
import pika
from RabbitMQ import RabbitMQ
import json
import threading
import time


def log(message, show=True):
    if show:
        print(message)


class Server:
    userlist = []

    def __init__(self):
        self.connection = RabbitMQ(self.onConnect)

    def onConnect(self):
        log("Connected to RabbitMQ")
        self.start_channels()

    def empty(self):
        return

    def start_channels(self):
        log("Starting Channels")
        self.connection.join_channel(
            "auth", self.processAuthMessage, self.empty)
        self.connection.join_channel(
            "control", self.processControlMessage, self.empty)

    def passMessage(self, ch, method, properties, body):
        response = json.loads(body)
        self.connection.sendMessage(
            "CHAN_"+response.to, response.to, response.message, response.userID)

    def processControlMessage(self, ch, method, properties, body):
        response = json.loads(body)
        if response.message == "USERLIST":
            self.connection.sendMessage(
                "control", response.userID, self.userlist, "SERVER")

    def processAuthMessage(self, ch, method, properties, body):
        log("Received LOGIN message")
        response = json.loads(body)
        if response.to == "" and response.userID != "":
            ch.basic_ack(delivery_tag=method.delivery_tag)
            userlist.append(response.userID)
            toSend = {
                status: "CONNECTION_ACCEPTED",
                channel: "CHAN_"+response.userID
            }
            self.connection.sendMessage(
                "auth", response.userID, "", "SERVER", toSend)
            self.connection.join_channel(toSend.channel, self.passMessage)


server = Server()
