from base64 import b32decode

def xor(a, b):
    return bytes([_a ^ _b for _a, _b in zip(a, b)])

xored = b32decode(b"LWBIHDDI3LK6BIVSV7CZXEM5SSBYXPIOLGWZWUZRQUCGYACMJBTS4ACAEVNFF4SNHMRRO===")
flag = b"HackademINT{"

key = xor(xored, flag)

for i in range(len(xored) - len(key)):
    print(xor(key, xored[len(key)+i:]))