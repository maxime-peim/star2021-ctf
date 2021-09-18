import subprocess
import random
import socket
from datetime import datetime
from _thread import *

serverSideSocket = socket.socket()
host = "0.0.0.0"
port = 40006
threadCount = 0
try:
    serverSideSocket.bind((host, port))
except socket.error as e:
    print(str(e))

print("Socket listening...")
serverSideSocket.listen(5)


def rce2(connection):
    random.seed(int(datetime.now().timestamp()) & 0xf)

    connection.send(b"Welcome to my super secure shell V2.\n")
    connection.send(b"Do you think you can achieve Random Code Execution ?\n")
    connection.send(b"You'll never be able to execute commands as I'll destroy everything you type.\n")
    connection.send(b"Good luck !! Mwah ah ah !!\n\n")


    data = b""
    command = b""
    connection.send(b"$ ")
    while b"\n" not in data:
        data = connection.recv(2048)
        command += data
    
    command = command[:command.find(b"\n")]
    command = command[:20]
    for i in range(len(command), 20):
        command += b"Z"
    print(command)
    for i in range(15):
        r = random.randrange(len(command))
        command = command[:r] + command[r+1:]
    connection.send(b"Executing your command : %s\n" % command)
    result = subprocess.getoutput(command)
    connection.send(result.encode() + b"\n")
    connection.send(b"NOPE ! You failed ! Goodbye !\n\n")
    connection.close()

while True:
    client, address = serverSideSocket.accept()
    print("Connected to : " + str(address[0]) + ":" + str(address[1]))
    start_new_thread(rce2, (client,))
    threadCount += 1
    print("Thread number : " + str(threadCount))
serverSideSocket.close()