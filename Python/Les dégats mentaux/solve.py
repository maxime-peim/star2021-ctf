from base64 import b64encode

def gene():
    a = 1
    while True:
        yield b64encode(bytes([a]))
        a += 1

G = gene()

end = [29301, 13367, 27041, 21384, 24446, 28723, 26045, 30124, 29701, 24375, 60056, 29855, 29247, 25887, 24478, 20633, 21819, 24375, 25487, 12299, 28047, 27915, 25999, 28171, 29839, 13067, 29327, 24331, 21903, 19979, 24463, 28683, 17808, 21772, 24464, 28684, 19600, 29964, 29584, 32012]

flag = "HackademINT{j_au**"
flag += ''.join(chr(c >> 8) for c in end)
# r4iS_peut_être_PU_c0mment3r_UN_pEU_pLus}

# guess: HackademINT{j_au**...

name = "pouetpouet_tut_tut"
# on récupère la liste du nom xoré avec le flag incorrect
xored_incorrect = [90, 69, 0, 4, 43, 26, 20, 33, 43, 61, 50, 17, 17, 21, 52, 23, 20, 60]
# et la liste incorrect en sortie
liste_incorrect = [29296, 13378, 27048, 21384, 24326, 28691, 26045, 30124, 29701, 24375, 60056, 29855, 29247, 25887, 24478, 20633, 21819, 24375, 25487, 12299, 28047, 27915, 25999, 28171, 29839, 13067, 29327, 24331, 21903, 19979, 24463, 28683, 17808, 21772, 24464, 28684, 19600, 29964, 29584, 32012]

# on peut maintenant trouver les positions où la liste incorrecte et le résultat souhaité
# ne correspondent pas, et calculer le caractère qu'il faut pour obtenir le bon résultat

flag = [c for c in flag]
for i in range(len(xored_incorrect)):
    if liste_incorrect[i] != end[i]:
        # on calcule la valeur du nombre xoré 
        # (int(str(next(G)[1]) + str(j.bit_length())))
        x = liste_incorrect[i] & 0xff ^ xored_incorrect[i]
        # on inverse le calcule à partir du résultat souhaité
        good_chr = chr(end[i] & 0xff ^ x ^ ord(name[i]))
        # la flag était lu à l'envers
        flag[17 - i] = good_chr

flag = ''.join(flag)
print(flag)