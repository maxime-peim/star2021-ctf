def xor(a, b):
    return bytes([a_ ^ b_ for a_, b_ in zip(a, b)])

def xor_repeated(a, b):
    if len(a) < len(b):
        max_len = len(b)
        a = (max_len // len(a) + 1)*a
    else:
        max_len = len(a)
        b = (max_len // len(b) + 1)*b
    return bytes([a_ ^ b_ for a_, b_ in zip(a, b)])

flag = b"HackademINT{"
ciphered = open("xorpasclair.bin", "rb").read()

key = xor(flag, ciphered)[:9]
print(xor_repeated(key, ciphered))
# HackademINT{h0w_d1D_y0U_gu3ss_mY_sup3r_r4nd0m_k3y?}