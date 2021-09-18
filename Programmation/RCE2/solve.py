from pwn import *
from datetime import datetime

import random

conn = remote("challs.hackademint.org", 40006)
random.seed(int(datetime.now().timestamp() + 1) & 0xf)

real_command = input("$ ").rstrip().ljust(5)
payload = "abcdefghijklmnopqrct"

for c in real_command:
    payload = payload.replace(c.lower(), c.upper())

command = payload
for i in range(15):
    r = random.randrange(len(command))
    command = command[:r] + command[r+1:]

for i, c in enumerate(real_command):
    payload = payload.replace(command[i], c)
    
conn.recvuntil(b"$ ")
conn.sendline(payload.encode())

conn.interactive()
# cat *
# HackademINT{YouR3_1N_t1m3}