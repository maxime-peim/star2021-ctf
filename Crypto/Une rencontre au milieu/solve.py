from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from string import *
from random import choice
from binascii import hexlify
import sys


def gen_key():
    for a in ascii_letters:
        for b in ascii_letters:
            for c in ascii_letters:
                for d in ascii_letters:
                    yield pad((a+b+c+d).encode(), AES.block_size)

if __name__ == "__main__":
    ciphertext = bytes.fromhex("4ae89cef4852d83ad311dab17a6afd6eaa022d917cc94ceebaf1f5bfdb6657c5b880978c2f9164bdc8d7e04237fab30bc5a76d5afbde869493d72e66f2ac719e")
    message = pad(b"Revolution", AES.block_size)
    message_cipher = bytes.fromhex("8bf7e3e084f3d1321a894d05e1f6cec1")

    middle = {}
    print("[+] Generating encrypted")
    K = gen_key()
    for k1 in K:
        AES1 = AES.new(k1, AES.MODE_ECB)
        middle1 = AES1.encrypt(message)
        middle[middle1] = k1

    print(len(middle))

    print("[+] Generating decrypted")
    K = gen_key()
    for k2 in K:
        AES2 = AES.new(k2, AES.MODE_ECB)
        middle2 = AES2.decrypt(message_cipher)

        if middle2 in middle:
            key1, key2 = middle[middle2], k2
            break

    AES1 = AES.new(key1, AES.MODE_ECB)
    AES2 = AES.new(key2, AES.MODE_ECB)

    pt2 = AES2.decrypt(ciphertext)
    pt1 = AES1.decrypt(pt2)

    print(pt1)

# HackademINT{D0uble_AES_15n't_3n0ugh_try_D0ubl3_R0t13_1n5t34d}