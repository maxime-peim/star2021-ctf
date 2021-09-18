import socket
import threading
from secret import flag
from string import printable


def check(inp):
    secret = flag
    blacklist = '!"#$%&*+-./;<=>?@[\\]^`|~"\t\n\r\x0b\x0c'
    if not all(map(lambda i: i in printable, inp)):
        return "C'est non"
    if any(map(lambda i: i in blacklist, inp)):
        return "C'est non"
    if len(inp) > 35:
        return "C'est non"

    local = locals().copy()
    local['type'] = type
    local['__builtins__'] = None
    try:
        exec('a = type(' + inp + ')', local)
        res = str(local['a'])
        return res[:30]
    except Exception:
        return "C'est non"


class ClientThread(threading.Thread):

    def __init__(self, ip, port, clientsocket):
        super().__init__()
        self.__clientsocket = clientsocket

    def run(self):
        self.__clientsocket.send("Mouhahaha je suis le TYPE CHECKER 9000, je peux trouver TOUS LES TYPES DU MOOOOOOOOOOOONDE\n".encode())
        while True:
            r = self.__clientsocket.recv(2048)
            try:
                rez = check(r[:-1].decode('utf-8'))
                self.__clientsocket.send(rez.encode() + b'\n')
            except UnicodeDecodeError:
                self.__clientsocket.send("C'est non\n".encode())
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
