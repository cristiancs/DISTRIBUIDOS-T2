from concurrent import futures
import grpc
import time
import chat_pb2 as chat
import chat_pb2_grpc as rpc

class ChatServer(rpc.ChatServerServicer):

    def __init__(self):
        self.chats = []

    def ChatStream(self, request_iterator, context):
        contador = 0
        while True:
            while len(self.chats) > contador:
                a = self.chats[contador]
                contador += 1
                yield a

    def SendNote(self, request, context):
        print("[{}] {}".format(request.name, request.message))
        self.chats.append(request)
        return chat.Empty()

port = 11912
server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
rpc.add_ChatServerServicer_to_server(ChatServer(), server)
print('Servidor esperando a usuarios')
server.add_insecure_port('[::]:' + str(port))
server.start()
while True:
    time.sleep(64 * 64 * 100)
