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
        self.connection_auth = RabbitMQ()
        log("Connected to RabbitMQ")
        time.sleep(2)  # Para darle tiempo al servidor a inicializarse
        self.auth()

    def processMessage(self, ch, method, properties, body):
        response = json.loads(body)
        if response["to"] == self.clientId:
            print("["+response["date"]+"] "+response["message"])

    def sendMessage(self, user, message):
        self.connection_messages.sendMessage(
            self.messagingChannel, user, message, self.clientId)

    def processControlMessages(self, ch, method, properties, body):
        response = json.loads(body)
        if response["to"] == self.clientId:
            ch.basic_ack(delivery_tag=method.delivery_tag)
            if response["type"] == "USERLIST":
                toPrint = ""
                i = 1
                for x in response["message"]:
                    toPrint += str(i)+": "+x+"\n"
                    i += 1
                print(toPrint)
                ch.stop_consuming()

    def requestList(self):
        self.connection_control.sendMessage(
            "control", "", "USERLIST", self.clientId)

    def getClients(self):
        log("Getting Clientes")
        self.connection_control = RabbitMQ()
        self.connection_control.join_channel(
            "control", self.processControlMessages, self.requestList)

    def waitForMessages(self):
        process_messages = True
        print("Conexión Establecida, para enviar un mensaje escriba: /msg user mensaje")
        while process_messages:
            text = input("")
            log(text)
            params = text.split(" ")
            command = params.pop(0).replace("/", "")

            log(command, params)
            if command == "msg":
                user = params.pop(0)
                message = " ".join(params)
                self.sendMessage(user, message)
            elif command == "quit":
                process_messages = False
                log("TODO: Disconnected")
            elif command == "list":
                self.getClients()
            else:
                print("Comando no reconocido")

    def processLoginMessage(self, ch, method, properties, body):
        log("Logging Response Received (General)")
        response = json.loads(body)
        print(response, self.clientId)
        if response["to"] == self.clientId:
            log("Loggin is for us")
            ch.basic_ack(delivery_tag=method.delivery_tag)
            if response["status"] == "CONNECTION_ACCEPTED":
                self.status = "logged_in"
                ch.stop_consuming()
                self.connection_auth.close()
                self.messagingChannel = response["channel"]

                t = threading.Thread(target=self.waitForMessages, args=())
                t.start()
                self.connection_messages = RabbitMQ()
                self.connection_messages.join_channel(
                    response["channel"], self.processMessage)

    def handleAuthOpen(self):
        log("Requesting Login")
        self.connection_auth.sendMessage(
            "auth", "", "LOGIN_REQUEST", self.clientId)

    def auth(self):
        log("Starting Auth")
        self.status = "authenticating"
        self.connection_auth.join_channel(
            "auth", self.processLoginMessage, self.handleAuthOpen)


client = Client()
