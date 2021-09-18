# https://dgl.cx/2014/10/vim-blowfish

def xor(a, b):
    return bytes([_a ^ _b for _a, _b in zip(a, b)])

magic = b"VimCrypt~02!"
start = b"HackademINT{"
BLOCK_SIZE = 8

with open("flag.txt", "rb") as fin:
    bts = fin.read()[len(magic)+2*BLOCK_SIZE:]

blocks = [bts[i:i+BLOCK_SIZE] for i in range(0, len(bts), BLOCK_SIZE)]
key = xor(start, blocks[0])

print(b''.join(xor(b, key) for b in blocks))
# HackademINT{Keystream_reuse=Pas_Fou}