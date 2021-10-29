import selectors
import types
from socket import *

IP_ADDR = "10.1.116.141"
PORT = 6969

class Server:
    def __init__(self):
        self.clientList = []
        self.sel = selectors.DefaultSelector()
        self.lsock = socket(AF_INET, SOCK_STREAM)
        self.lsock.bind((IP_ADDR, PORT))
        self.lsock.listen()
        print('listening on', (IP_ADDR, PORT))
        self.lsock.setblocking(False)
        self.sel.register(self.lsock, selectors.EVENT_READ, data=None)

        self.program_loop()

    def program_loop(self):
        while True:
            events = self.sel.select(timeout=None)
            for key, mask in events:
                if key.data is None:
                    self.accept_wrapper(key.fileobj)
                else:
                    self.service_connection(key, mask)

    def accept_wrapper(self, sock):
        conn, addr = sock.accept()
        print('accepted connection from', addr)
        conn.setblocking(False)
        data = types.SimpleNamespace(addr=addr, inb=b'', outb=b'')
        events = selectors.EVENT_READ | selectors.EVENT_WRITE
        self.sel.register(conn, events, data=data)
        self.clientList.append(conn)

    def service_connection(self, key, mask):
        sock = key.fileobj
        data = key.data
        if mask & selectors.EVENT_READ:
            recv_data = sock.recv(1024)  # Should be ready to read
            if recv_data:
                data.outb = recv_data
                self.forward(data, sock)
            else:
                print('closing connection to', data.addr)
                self.sel.unregister(sock)
                self.clientList.remove(sock)
                sock.close()
        if mask & selectors.EVENT_WRITE:
            if data.outb:
                print('echoing', repr(data.outb), 'to', data.addr)
                # sent = sock.send(data.outb)  # Should be ready to write
                # data.outb = data.outb[sent:]

    def forward(self, msg, sock):
        # TODO: Forward the message to all other clients but the sender
        for s in self.clientList:
            print(type(s))
            if s != sock:
                try:
                    s.send(msg.outb)
                except BlockingIOError:
                    print("Could not send")



if __name__ == "__main__":
    server = Server()
