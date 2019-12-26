
import uuid
import json
import threading
import time
import grpc
from random import randint, choice
from concurrent import futures
from datetime import datetime
import chat_pb2
import chat_pb2_grpc
import sys


def log(message, show=False):
    if show:
        print(message)


class Client:
    clientId = str(uuid.uuid4())
    status = "disconnected"
    messagingChannel = ""
    userPicked = ""

    def __init__(self):
        ip_server = sys.argv[1] if len(sys.argv) > 1 else 'server_1:50051'
        self.connection_auth = grpc.insecure_channel(ip_server)
        self.stub = chat_pb2_grpc.ChatServerStub(self.connection_auth)

        # Iniciar servidor para escuchar mensajes de otros users
        self.port = randint(20000, 50000)
        intentar = True
        while intentar:
            try:
                self.listen_server = grpc.server(
                    futures.ThreadPoolExecutor(max_workers=10))
                chat_pb2_grpc.add_ChatServerServicer_to_server(
                    self, self.listen_server)
                self.listen_server.add_insecure_port('[::]:'+str(self.port))
                self.listen_server.start()
                intentar = False
            except Exception as e:
                log(e)
                self.port = randint(20000, 50000)

        self.auth()

    def formatMessage(self, toChannel, user, message, userID, raw={}):

        now = datetime.now()
        toSend = {
            "uuid": str(uuid.uuid4()),
            "date": now.strftime("%D %H:%M:%S"),
            "to": user,
            "message": message,
            "userID": userID,
            **raw
        }
        return json.dumps(toSend)

    def passMessage(self, request, context):
        response = json.loads(request.message)
        date = response["date"]
        userID = response["userID"]
        message = response["message"]

        log("Mensaje recibido")
        if response["to"] == self.clientId:
            log("Mensaje es para nosotros")
            print(f"[{date}] {userID}: {message}")
        return chat_pb2.Empty()

    def ControlMessage(self, request, context):
        return

    def AuthMessage(self, request, context):
        return

    def processControlMessages(self, request):
        response = json.loads(request.message)
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
        mensaje = self.formatMessage(
            "control", "", "USERLIST", self.clientId)
        mensaje = chat_pb2.Mensaje(message=mensaje)
        response = self.stub.ControlMessage(mensaje)
        log(response)
        return response

    def requestMessages(self):
        mensaje = self.formatMessage(
            "control", "", "SENT_MESSAGES", self.clientId)
        mensaje = chat_pb2.Mensaje(message=mensaje)
        response = self.stub.ControlMessage(mensaje)
        return response

    def waitForMessages(self):
        process_messages = True

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
                        ["/list", "/msg "+self.userPicked+" prueba de mensajes"])
                else:
                    text = "/list"
                log("Enviando: "+text)

            params = text.split(" ")
            command = params.pop(0).replace("/", "")

            if command == "msg":
                user = params.pop(0)
                message = " ".join(params)

                mensaje = self.formatMessage(
                    self.messagingChannel, user, message, self.clientId)
                mensaje = chat_pb2.Mensaje(message=mensaje)
                self.stub.passMessage(mensaje)
            elif command == "quit":
                process_messages = False
                log("TODO: Disconnected")
            elif command == "list":
                self.processControlMessages(self.requestList())
            elif command == "mymessages":
                self.processControlMessages(self.requestMessages())
            else:
                print("Comando no reconocido")

    def auth(self):
        log("Starting Auth")
        self.status = "authenticating"

        mensaje = self.formatMessage(
            "auth", "", "LOGIN_REQUEST", self.clientId, {"port": self.port})
        log(mensaje)
        mensaje = chat_pb2.Mensaje(message=mensaje)
        log(mensaje)
        # make the call

        response = self.stub.AuthMessage(mensaje)
        log("Logging Response Received (General)")
        response = json.loads(response.message)
        log(response)
        if response["to"] == self.clientId:
            log("Loggin is for us")
            if response["status"] == "CONNECTION_ACCEPTED":
                print(f"Conexión Establecida, tu usuario es: {self.clientId}")
                print(
                    "Comandos disponibles:\n /msg user mensaje [envia mensaje a user] \n /list [Devuelve la lista de todos los usuarios]")
                print(" /mymessages [Listado de canales]")
                self.status = "logged_in"
                self.messagingChannel = response["channel"]
                self.waitForMessages()


client = Client()
