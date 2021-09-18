import socket
import threading
import asyncio
from secret import flag


class ClientThread(threading.Thread):

    def __init__(self, ip, port, clientsocket):
        super().__init__()
        self.__clientsocket = clientsocket
        self.__allow = False

    def run(self):
        self.__clientsocket.send("Vroum vroum, je vroum et toi?\n".encode())
        while True:
            r = self.__clientsocket.recv(2048)
            asyncio.run(self.main(r))
            self.__clientsocket.close()
            return

    async def check_flag(self, user_input):
        self.__allow = True
        user_input.decode('utf-8')
        if user_input != flag:
            self.__allow = False

    async def send_flag(self):
        if self.__allow:
            self.__clientsocket.send(flag.encode() + b'\n')
        else:
            self.__clientsocket.send("Non\n".encode())

    async def main(self, user_input):
        asyncio.create_task(self.check_flag(user_input))
        asyncio.create_task(self.send_flag())


if __name__ == '__main__':
    tcpsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcpsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    tcpsock.bind(("", 2042))

    while True:
        tcpsock.listen(10)
        (clientsocket, (ip, port)) = tcpsock.accept()
        newthread = ClientThread(ip, port, clientsocket)
        newthread.start()
