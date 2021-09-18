from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from string import *
from random import choice
from binascii import hexlify
import sys


def gen_key():
    s = choice(ascii_letters) + choice(ascii_letters) + choice(ascii_letters) + choice(ascii_letters)
    key = pad(s.encode(), AES.block_size)
    return key


if __name__ == "__main__":
    try:
        message = sys.argv[1]
    except:
        print("Vous n'avez pas fourni de message à chiffrer")
        sys.exit(1)


key1 = gen_key()
key2 = gen_key()


AES1 = AES.new(key1, AES.MODE_ECB)
AES2 = AES.new(key2, AES.MODE_ECB)


cipher1 = (AES1.encrypt(pad(message.encode(), AES.block_size)))
cipher2 = (AES2.encrypt(cipher1))

print(hexlify(cipher2))
