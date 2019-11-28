import pika
from RabbitMQ import RabbitMQ
import uuid
import json
import threading
import time


def log(message, show=True):
    if show:
        print(message)


class Client:
    clientId = str(uuid.uuid4())
    status = "disconnected"
    messagingChannel = ""

    def __init__(self):
        time.sleep(5)
        self.connection = RabbitMQ(self.onConnect)

    def onConnect(self):
        log("Connected to RabbitMQ")
        self.auth()

    def processMessage(self, ch, method, properties, body):
        response = json.loads(body)
        print(response.date+" "+response.message)

    def sendMessage(self, user, message):
        self.connection.sendMessage("", "", "USERLIST", self.clientId)

    def processControlMessages(self, ch, method, properties, body):
        response = json.loads(body)
        if response.to == self.clientId:
            ch.basic_ack(delivery_tag=method.delivery_tag)
            if response.type == "USERLIST":
                toPrint = ""
                for x in response.users:
                    toPrint += x+"\n"
                print(toPrint)

    def getClients(self):
        self.connection.sendMessage("")

    def waitForMessages(self):
        process_messages = True
        print("Conexión Establecida, para enviar un mensaje escriba: /msg user mensaje")
        while process_messages:
            text = input("")
            params = text.split(" ")
            command = params.pop(0).replace("/", "")
            if command == "msg":
                user = params.pop(0)
                message = " ".join(params)
                self.sendMessage(user, message)
            if command == "quit":
                process_messages = False
                log("TODO: Disconnected")
            if command == "list":
                this.getClients()

    def processLoginMessage(self, ch, method, properties, body):
        log("Logging Response Received (General)")
        response = json.loads(body)
        if response.to == self.clientId:
            log("Loggin is for us")
            ch.basic_ack(delivery_tag=method.delivery_tag)
            if response.status == "CONNECTION_ACCEPTED":
                self.status = "logged_in"
                ch.stop_consuming()
                self.messagingChannel = response.channel
                self.connection.join_channel(
                    response.channel, self.processMessage)
                self.connection.join_channel(
                    "control", self.processControlMessages)
                threading.Thread(target=self.waitForMessages, args=(1,))

    def handleAuthOpen(self):
        log("Requesting Login")
        self.connection.sendMessage("auth", "", "LOGIN_REQUEST", self.clientId)

    def auth(self):
        log("Starting Auth")
        self.status = "authenticating"
        self.connection.join_channel(
            "auth", self.processLoginMessage, self.handleAuthOpen)


client = Client()
