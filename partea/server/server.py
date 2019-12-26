import grpc
import json
import threading
import time
from datetime import datetime
import uuid
import chat_pb2
import chat_pb2_grpc
from concurrent import futures

write_lock = threading.Lock()


def log(message, show=False):
    if show:
        print(message)


class Server:
    userlist = {}

    def __init__(self):
        self.server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        chat_pb2_grpc.add_ChatServerServicer_to_server(
            self, self.server)
        self.server.add_insecure_port('[::]:50051')
        self.server.start()
        while True:
            time.sleep(86400)

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
        log(response)
        date = response["date"]
        userID = response["userID"]
        message = response["message"]

        toWrite = f"[{date}] {userID}: {message} \n"

        write_lock.acquire()

        logs = open("log.txt", "a")
        logs.write(toWrite)
        logs.close()
        write_lock.release()

        self.userlist[response["userID"]]["messages"].append(toWrite)

        connection = grpc.insecure_channel(
            self.userlist[response["to"]]["channel"])
        log(self.userlist[response["to"]]["channel"])
        stub = chat_pb2_grpc.ChatServerStub(connection)

        mensaje = self.formatMessage(
            "CHAN_"+response["to"]+"_receive", response["to"], response["message"], response["userID"])
        mensaje = chat_pb2.Mensaje(message=mensaje)
        stub.passMessage(mensaje)
        connection.close()

        return chat_pb2.Empty()

    def ControlMessage(self, request, context):
        toReply = chat_pb2.Mensaje()
        response = json.loads(request.message)
        log(response)
        if response["message"] == "USERLIST":
            toSend = list(self.userlist.keys())
            toReply.message = self.formatMessage(
                "control_"+response["userID"], response["userID"], toSend, "SERVER", {
                    "type": "USERLIST"
                })
        if response["message"] == "SENT_MESSAGES":
            toSend = self.userlist[response["userID"]]["messages"]
            toReply.message = self.formatMessage(
                "control_"+response["userID"], response["userID"], toSend, "SERVER", {
                    "type": "SENT_MESSAGES"
                })
        return toReply

    def AuthMessage(self, request, context):
        toReply = chat_pb2.Mensaje()
        log("Received LOGIN message")

        ipCliente = context.peer().split(":")[1]
        response = json.loads(request.message)
        print(response)
        if response["to"] == "" and response["userID"] != "":
            self.userlist[response["userID"]] = {
                "channel": ipCliente+":"+str(response["port"]),
                "messages": []
            }
            toSend = {
                "status": "CONNECTION_ACCEPTED",
                "channel": "CHAN_"+response["userID"]
            }
        toReply.message = self.formatMessage(
            "auth_"+response["userID"], response["userID"], "", "SERVER", toSend)
        return toReply


server = Server()
