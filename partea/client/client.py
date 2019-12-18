import threading
from Tkinter import *
import grpc
import chat_pb2 as chat
import chat_pb2_grpc as rpc

address = 'localhost'
port = 11912

class Client:

    def __init__(self, u, window):
        self.window = window
        self.usuario = u
        channel = grpc.insecure_channel(address + ':' + str(port))
        self.connection = rpc.ChatServerStub(channel)
        threading.Thread(target=self.__listen_for_messages).start()
        self.initialize()
        self.window.mainloop()

    def __listen_for_messages(self):
        for note in self.connection.ChatStream(chat.Empty()):
            print("R[{}] {}".format(note.name, note.message))
            self.chat_list.insert(END, "[{}] {}\n".format(note.name, note.message))

    def send_message(self, event):
        message = self.envio_mensaje.get()
        if message is not '':
            n = chat.Note()
            n.name = self.usuario
            n.message = message
            print("S[{}] {}".format(n.name, n.message))
            self.connection.SendNote(n)

    def initialize(self):
        self.chat_list = Text()
        self.chat_list.pack(side=TOP)
        self.lbl_usuario = Label(self.window, text=self.usuario)
        self.lbl_usuario.pack(side=LEFT)
        self.envio_mensaje = Entry(self.window, bd=5)
        self.envio_mensaje.bind('<Return>', self.send_message)
        self.envio_mensaje.focus()
        self.envio_mensaje.pack(side=BOTTOM)

root = Tk()
frame = Frame(root, width=300, height=300)
frame.pack()
print("Coloque su nombre de usuario:")
user = raw_input ()
root.withdraw()
root.deiconify()
Client(user, frame)
