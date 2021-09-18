import socket
import threading
import random
from secret import flag


def check(x, nb):
    if x-nb is x-nb:
        return False
    if x-(nb+1) is not x-(nb+1):
        return False
    return True


class ClientThread(threading.Thread):

    def __init__(self, ip, port, clientsocket):
        super().__init__()
        self.__clientsocket = clientsocket

    def run(self):
        nb = random.randint(0, 1E10)
        self.__clientsocket.send(f"Moi j'te file ça : {nb}, tu me propose quoi?\n".encode())
        while True:
            r = self.__clientsocket.recv(2048)
            try:
                v = int(r)
            except ValueError:
                try:
                    self.__clientsocket.send("C'pas un nombre ça\n".encode())
                except BrokenPipeError:
                    return
                continue
            if check(v, nb):
                try:
                    self.__clientsocket.send(flag.encode() + b"\n")
                    self.__clientsocket.close()
                except BrokenPipeError:
                    None
                finally:
                    return
            else:
                try:
                    self.__clientsocket.send("Nope\n".encode())
                except BrokenPipeError:
                    return


if __name__ == '__main__':
    tcpsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcpsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    tcpsock.bind(("", 2042))

    while True:
        tcpsock.listen(10)
        (clientsocket, (ip, port)) = tcpsock.accept()
        newthread = ClientThread(ip, port, clientsocket)
        newthread.start()
