# très etrange, pour une différence de 257 on passe les tests
# check(257, 0) = True

from pwn import *
import re

conn = remote("challs.hackademint.org", 40051)

nb = int(re.findall(r"Moi j'te file ça : (.*), tu me propose quoi?", conn.recvline().decode())[0])
conn.sendline(str(nb+257).encode())
print(conn.recvline().decode())

conn.close()