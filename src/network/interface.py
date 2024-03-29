# TODO: Þarf að gera class sem sér um network draslið
import selectors
import socket
import types

from src.essentials.settings import *

from socket import *

IP_ADDR = "157.97.11.131"
PORT = 6969 #Nice

class Interface:
    def __init__(self):
        self.isAvailable = False
        self.sock = socket(AF_INET, SOCK_STREAM)
        self.sock.setblocking(False)
        try:
            self.sock.connect_ex((IP_ADDR, PORT))
            self.isAvailable = True
        except socket.error:
            print("Caught exception socket.error")
        # events = selectors.EVENT_READ | selectors.EVENT_WRITE
        # data = types.SimpleNamespace(addr=addr, inb=b'', outb=b'')

    def send(self, data):
        try:
            self.sock.send(bytes(data, "utf-8"))
        except OSError:
            print("Unable to send")
            self.isAvailable = False

    def recv(self):
        try:
            data = self.sock.recv(1024)
            return data.decode("utf-8")
        except BlockingIOError:
            return ""
        except OSError:
            self.isAvailable = False
            return ""

    def closeSock(self):
        self.sock.close()

if __name__ == "__main__":
    net = Interface()