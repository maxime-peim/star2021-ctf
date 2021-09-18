from Crypto.Cipher import DES
from Crypto.Util.Padding import pad, unpad
from os import urandom
from pwn import xor
from secret import flag

def main(connection):

    print("Bon, mon super programme de chiffrement avait un problème. Mais maintenant, tout va bien ! J'ai fait une version 2.0, et elle n'a plus aucun problème !")
    print("Pour que ce soit encore plus securisé, il y a desormais deux fois plus de random et deux fois plus de clés à rentrer.")
    print("Il n'y a desormais plus aucune chance que vous trouviez mon flag !\n")
    while True:
        # Je me ferais plus avoir avec ces histoires de clés faibles!
        blacklist=["0000000000000000","ffffffffffffffff","0101010101010101","FEFEFEFEFEFEFEFE","E0E0E0E0F1F1F1F1","1F1F1F1F0E0E0E0E","E1E1E1E1F0F0F0F0","1E1E1E1E0F0F0F0F"]
        blacklist=[bytes.fromhex(i) for i in blacklist]
        inp=input(b"Veuillez indiquer la premiere clé : ")
        try:
            key1=bytes.fromhex(inp.decode('ascii'))
            if key1 in blacklist:
                print("Les clés faibles ne sont pas autorisées ici !")
                continue
            des1 = DES.new(key1, DES.MODE_ECB)
        except:
            print("Gépakompri, merci de renvoyer une vraie clé DES")
            continue
        inp2=input("Et la deuxième: ")
        try:
            key2 = bytes.fromhex(inp2.decode('ascii'))
            if key2 in blacklist:
                print("Les clés faibles ne sont pas autorisées ici!")
                continue
            des2 = DES.new(key2, DES.MODE_ECB)
        except:
            print("Gépakompri, merci de renvoyer une vraie clé DES")
            continue

        flag=pad(flag,8)

        IV1=urandom(8)
        IV2=urandom(8) #Plus il y a d'aléatoire, plus c'est securisé!
        flag = xor(flag, IV1)
        for i in range(6):
            flag = xor(flag, IV2)
            cipher1=des1.encrypt(flag)

            cipher2=des2.encrypt(cipher1)

            flag=cipher2
            flag=xor(flag,IV2)

        flag=xor(IV1,flag)

        try:
            print("Voila le résultat: " + unpad(flag,8).hex())
        except:
            print("Voila le résultat: " + flag.hex())
        print("Vous pouvez réessayer, mais vous n'arriverez jamais à trouver mon flag!")



