
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
        self.connection_control = RabbitMQ()
        self.connection_auth = RabbitMQ()
        self.start_channels()

    def join_auth(self):
        self.connection_auth.join_channel(
            "auth", self.processAuthMessage)

    def join_control(self):
        self.connection_control.join_channel(
            "control", self.processControlMessage)

    def start_channels(self):
        log("Starting Channels")
        t = threading.Thread(target=self.join_auth, args=())
        t2 = threading.Thread(target=self.join_control, args=())

        t.start()
        t2.start()

    def passMessage(self, ch, method, properties, body):
        response = json.loads(body)

        toSendConnection = ""
        for el in self.userlist:
            if el["username"] == response["to"]:
                toSendConnection = el.connection

        if toSendConnection == "":
            log("User "+response["to"]+" not found")
        else:
            toSendConnection.sendMessage(
                "CHAN_"+response["to"], response["to"], response["message"], response["userID"])

    def processControlMessage(self, ch, method, properties, body):
        response = json.loads(body)
        log(response)
        if response["message"] == "USERLIST":
            toSend = []
            for el in self.userlist:
                toSend.append(el["username"])
            self.connection_control.sendMessage(
                "control", response["userID"], toSend, "SERVER", {
                    "type": "USERLIST"
                })

    def join_communication_channel(self, currentConnection, channel):
        currentConnection.join_channel(channel, self.passMessage)

    def processAuthMessage(self, ch, method, properties, body):
        log("Received LOGIN message")
        response = json.loads(body)
        print(response)
        if response["to"] == "" and response["userID"] != "":
            ch.basic_ack(delivery_tag=method.delivery_tag)

            current_connection = RabbitMQ()
            self.userlist.append({
                "username": response["userID"],
                "connection": current_connection}
            )
            toSend = {
                "status": "CONNECTION_ACCEPTED",
                "channel": "CHAN_"+response["userID"]
            }
            self.connection_auth.sendMessage(
                "auth", response["userID"], "", "SERVER", toSend)
            t = threading.Thread(
                target=self.join_communication_channel, args=(current_connection, toSend["channel"]))
            t.start()


server = Server()
