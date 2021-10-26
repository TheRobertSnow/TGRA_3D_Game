# TODO: Þarf að gera class sem sér um network draslið
import socket
from socket import *
from src.essentials.settings import *

class NetInterface:
    def __init__(self):
        # Create a UDP IPv4 socket
        self.sock = socket(AF_INET, SOCK_DGRAM, protocol=0)
        self.sock.setblocking(False)

    def host(self):
        self.sock.bind(INADDR_ANY, PORT)
        self.sock.listen()
        conn, addr = self.sock.accept()
        conn.setblocking(False)

    def connect_to(self):
        self.sock.connect()
        self.sock.setblocking(False)
