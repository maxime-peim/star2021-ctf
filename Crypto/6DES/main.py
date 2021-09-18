from Crypto.Cipher import DES
from Crypto.Util.Padding import pad, unpad
from os import urandom
from pwn import xor
from secret import flag

def main():
    print("Est-ce que vous êtes prêts à voir mon super programme de chiffrement ? Je suis sûr que vous ne pourrez pas récuperer le flag !")
    print("Je l'ai appelé 6DES, il doit donc être au moins deux fois plus sûr que le 3DES !")
    inp=input("Donnez-moi votre clé en hex et je vous montrerai un flag vraiment chiffré !")
    while True:
        blacklist=[bytes.fromhex("0000000000000000"),bytes.fromhex("ffffffffffffffff")] #J'ai lu quelque part que ces clés étaient à bannir
        try:
            key=bytes.fromhex(inp.decode('ascii'))
            if key in blacklist:
                print("Cette clé est bizarre, merci d'en envoyer une autre")
                continue
            des = DES.new(key, DES.MODE_ECB)
        except:
            print("Gépakompri, merci de renvoyer une vraie clé DES")
            continue

        flag=pad(flag,8)

        IV=urandom(8) #Comme ça je suis sur de ne pas avoir de problèmes à cause de l'ECB!
        for i in range(6):

            flag=xor(flag,IV)

            flag=des.encrypt(flag)

            flag=xor(IV,flag)

        try:
            print("Voilà le résultat :" + unpad(flag,8).hex())
        except:
            print("Voila le resultat:" + flag.hex())
        print("Vous pouvez réessayer, mais vous n'arriverez jamais à trouver mon flag !")

