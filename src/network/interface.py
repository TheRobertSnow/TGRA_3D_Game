# TODO: Þarf að gera class sem sér um network draslið
import selectors
import types

from src.essentials.settings import *

from socket import *

IP_ADDR = "127.0.0.1"
PORT = 6969 #Nice

class Interface:
    def __init__(self):
        self.sock = socket(AF_INET, SOCK_STREAM)
        self.sock.setblocking(False)
        self.sock.connect_ex((IP_ADDR, PORT))
        # events = selectors.EVENT_READ | selectors.EVENT_WRITE
        # data = types.SimpleNamespace(addr=addr, inb=b'', outb=b'')

    def send(self, data):
        self.sock.send(bytes(data, "utf-8"))

    def recv(self):
        try:
            data = self.sock.recv(1024)
            return repr(data)
        except BlockingIOError:
            return ""

if __name__ == "__main__":
    net = Interface()