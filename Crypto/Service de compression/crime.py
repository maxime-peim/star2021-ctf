from Crypto.Cipher import ChaCha20
from os import urandom
import zlib
from secret import flag



def compress(message):
    return zlib.compress(message)

def encrypt(plaintext):
    secret = os.urandom(32)
    cipher = ChaCha20.new(key=secret)
    return cipher.nonce + cipher.encrypt(plaintext)


def main(connection):
    p=urandom(1) #Byte aléatoire pour empecher des attaques simples
    print("Bienvenue sur mon service de chiffrement.")
    while True:
        inp=input("Veuillez entrer le message en hex que vous voulez chiffrer: ")
        try:
            message=bytes.fromhex(inp)
        except:
            print("Erreur dans la réception de votre message, merci de recommencer")
            continue
        compressed_text = compress(p + flag + message)
        encrypted = encrypt(compressed_text)

        nonce = encrypted [:8]
        ciphertext = encrypted [8:]
        print("Le nonce utilisé: " + nonce.hex())
        print("Le ciphertext: " + ciphertext.hex())

