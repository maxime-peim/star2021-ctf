# décalage croissant

with open("flag.enc", "rb") as fin:
    b_in = fin.read()

with open("flag.jpg", "wb") as fout:
    decalage = 0
    for b in b_in:
        fout.write(bytes([(b - decalage)%0x100]))
        decalage += 1
        decalage %= 0x100

# HackademINT{V0u5_4v3z_7tr0uv3_l4_p0t10n_M4g1qu3!}