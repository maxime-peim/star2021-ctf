from base64 import b64decode, b64encode

def xor(a, b):
    return bytes([_a ^ _b for _a, _b in zip(a, b)])

BLOCK_SIZE = 16
non_bloc = b64decode("nzmdPxCThhOkJ7EX41n0O/8Z5Waql3dQwYnFLJ6lXL8=")
iv = non_bloc[:BLOCK_SIZE]

mask = b"\x00" * 11 + b"non" + b"\x00" * 2
correction = b"\x00" * 11 + b"oui" + b"\x00" * 2
new_iv = xor(iv, xor(mask, correction))

oui_bloc = new_iv + non_bloc[BLOCK_SIZE:]
print(b64encode(oui_bloc).decode())

# HackdemINT{GG_h4x0r,_c'357_du_b0n_b0ul07OO}