from pwn import *
import copy
import base64


ENC = bytearray(base64.b64decode("4Ipgzg64vNPsPRcGcO+MElyU1Uo9sLyUGBE9xpo7yhg="))
BSIZE = 16
C = [ENC[i:i+BSIZE] for i in range(0, len(ENC), BSIZE)]
PADDING = b"Erreur de remplissage..."

conn = remote("challs.hackademint.org", 2008)

findblock = len(C) - 1
result = b""
Cp = copy.deepcopy(C)
for padding in range(1, BSIZE+1):
    for i in range(0xff+1):
        # si on atteint la fin du padding result et padding s'annule
        if i > 0 or (len(result) > 0 and result[0] == padding):
            Cp[-2][-padding] = i ^ C[-2][-padding]
            #print(i, C[-2][-padding], i ^ C[-2][-padding])
            #print(b''.join(Cp).hex())
            conn.sendline(base64.b64encode(b''.join(Cp)))
            answer = conn.recvline()
            #print(answer)
            if not PADDING in answer:
                print("GOOD %d %d" % (i, Cp[-2][-padding]))
                result = bytes([i ^ padding]) + result
                break

    print(result)

    for i in range(1, padding+1):
        Cp[-2][-i] = C[-2][-i] ^ result[-i] ^ (padding+1)

conn.close()

# HackademINT{P4dd1n9}