import pika
from RabbitMQ import RabbitMQ
import uuid
import json
import threading
import time
from random import randint, choice

def log(message, show=True):
    if show:
        print(message)


class Client:
    clientId = str(uuid.uuid4())
    status = "disconnected"
    control_enabled = False
    messagingChannel = ""
    userPicked = ""

    def __init__(self):
        self.connection_auth = RabbitMQ()
        log("Connected to RabbitMQ")
        time.sleep(2)  # Para darle tiempo al servidor a inicializarse
        self.auth()

    def processMessage(self, ch, method, properties, body):
        response = json.loads(body)
        date = response["date"]
        userID = response["userID"]
        message = response["message"]

        log("Mensaje recibido")
        if response["to"] == self.clientId:
            log("Mensaje es para nosotros")
            print(f"[{date}] {userID}: {message}")

    def processControlMessages(self, ch, method, properties, body):
        response = json.loads(body)
        if response["to"] == self.clientId:
            if response["type"] == "USERLIST":
                print("Listado de Usuarios")
                toPrint = ""
                i = 1
                for x in response["message"]:
                    toPrint += str(i)+": "+x+"\n"
                    i += 1
                # Para simular en docker
                self.userPicked = choice(response["message"])
                print(toPrint)
            if response["type"] == "SENT_MESSAGES":
                print("Mensajes enviados por ti")
                for x in response["message"]:
                    print(x)

    def requestList(self):
        # La pide esta conexión por el tema de los threads
        self.connection_messages.sendMessage(
            "control", "", "USERLIST", self.clientId)

    def requestMessages(self):
        # La pide esta conexión por el tema de los threads
        self.connection_messages.sendMessage(
            "control", "", "SENT_MESSAGES", self.clientId)

    def startControlThread(self):
        self.connection_control = RabbitMQ()
        self.connection_control.join_channel(
            "control_"+self.clientId, self.processControlMessages, self.enableControl)

    def enableControl(self):
        log("Joined control channel")
        self.control_enabled = True

    def waitForMessages(self):
        process_messages = True
        t2 = threading.Thread(target=self.startControlThread, args=())
        t2.start()
        while process_messages:
            try:
                text = input("")
            except EOFError:
                seg = randint(0, 10000)
                log("Es docker, enviando mensaje random en "+str(seg/1000.0))
                time.sleep(seg/1000.0)
                log("Seleccionando mensaje")
                if(self.userPicked != ""):
                    text = choice(
                        ["/list", "/mymessages", "/msg "+self.userPicked+" prueba de mensajes"])
                else:
                    text = "/list"
                log("Enviando: "+text)

            params = text.split(" ")
            command = params.pop(0).replace("/", "")

            if command == "msg":
                user = params.pop(0)
                message = " ".join(params)
                self.connection_messages.sendMessage(
                    self.messagingChannel, user, message, self.clientId)
            elif command == "quit":
                process_messages = False
                log("TODO: Disconnected")
            elif command == "list":
                self.requestList()
            elif command == "mymessages":
                self.requestMessages()
            else:
                print("Comando no reconocido")

    def processLoginMessage(self, ch, method, properties, body):
        log("Logging Response Received (General)")
        response = json.loads(body)
        log(response)
        if response["to"] == self.clientId:
            log("Loggin is for us")
            if response["status"] == "CONNECTION_ACCEPTED":
                print(f"Conexión Establecida, tu usuario es: {self.clientId}")
                print(
                    "Comandos disponibles:\n /msg user mensaje [envia mensaje a user] \n /list [Devuelve la lista de todos los usuarios]")
                print(" /mymessages [Listado de canales]")
                self.status = "logged_in"
                ch.stop_consuming()
                self.connection_auth.close()
                self.messagingChannel = response["channel"]

                self.connection_messages = RabbitMQ()

                self.connection_messages.join_channel(
                    response["channel"]+"_receive", self.processMessage, self.waitForMessages)

    def handleAuthOpen(self):
        log("Requesting Login")
        self.connection_auth.sendMessage(
            "auth", "", "LOGIN_REQUEST", self.clientId)

    def auth(self):
        log("Starting Auth")
        self.status = "authenticating"
        self.connection_auth.join_channel(
            "auth_"+self.clientId, self.processLoginMessage, self.handleAuthOpen)


client = Client()
