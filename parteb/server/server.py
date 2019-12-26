
import pika
from RabbitMQ import RabbitMQ
import json
import threading
import time

write_lock = threading.Lock()


def log(message, show=False):
    if show:
        print(message)


class Server:
    userlist = {}

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
        self.userlist[response["userID"]]["channel"].sendMessage(
            "CHAN_"+response["to"]+"_receive", response["to"], response["message"], response["userID"])

    def processControlMessage(self, ch, method, properties, body):
        response = json.loads(body)
        log(response)
        if response["message"] == "USERLIST":
            #    ch.basic_ack(delivery_tag=method.delivery_tag)
            toSend = list(self.userlist.keys())
            self.connection_control.sendMessage(
                "control_"+response["userID"], response["userID"], toSend, "SERVER", {
                    "type": "USERLIST"
                })
        if response["message"] == "SENT_MESSAGES":
            toSend = self.userlist[response["userID"]]["messages"]
            self.connection_control.sendMessage(
                "control_"+response["userID"], response["userID"], toSend, "SERVER", {
                    "type": "SENT_MESSAGES"
                })

    def logJoin(self):
        log("Joined Channel")

    def join_communication_channel(self, userID, channel):
        self.userlist[userID]["channel"] = RabbitMQ()
        self.userlist[userID]["channel"].join_channel(
            channel, self.passMessage, self.logJoin)

    def processAuthMessage(self, ch, method, properties, body):
        log("Received LOGIN message")
        response = json.loads(body)
        print(response)
        if response["to"] == "" and response["userID"] != "":
            self.userlist[response["userID"]] = {
                "channel": "",
                "messages": []
            }
            toSend = {
                "status": "CONNECTION_ACCEPTED",
                "channel": "CHAN_"+response["userID"]
            }
            self.connection_auth.sendMessage(
                "auth_"+response["userID"], response["userID"], "", "SERVER", toSend)
            t = threading.Thread(
                target=self.join_communication_channel, args=(response["userID"], toSend["channel"]))
            t.start()


server = Server()
