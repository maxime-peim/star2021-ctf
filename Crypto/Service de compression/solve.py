from pwn import *
from string import printable
import sys

def read_next(conn, payload):
    conn.recvuntil(b"chiffrer: ")
    conn.sendline(payload.hex().encode())

    conn.recvuntil("utilisé: ".encode("utf8"))
    nonce = conn.recvline()
    conn.recvuntil(b"ciphertext: ")
    ciphertext = conn.recvline()

    return len(ciphertext)

conn = remote("157.159.191.52", 25007)

conn.recvline()

flag = b"HackademINT{"
current = read_next(conn, flag)

while flag[-1] != b'}':
    mn = current + 100
    possibles = []
    for c in printable:
        tmp_flag = flag + c.encode()
        l = read_next(conn, tmp_flag)

        if mn == l:
            possibles.append(c)
        elif mn > l:
            possibles.clear()
            possibles.append(c)
            mn = l

    if len(possibles) > 1:
        print(possibles)
        c = ' '
        while c not in possibles:
            c = input(">>> ")
    else:
        c = possibles[0]
        
    flag += c.encode()
    current = mn
    print(flag.decode())

conn.close()

# HackademINT{Cr1m35_4nd_Pun1shm3n75}