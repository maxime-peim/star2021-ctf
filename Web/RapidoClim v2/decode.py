from base64 import b32decode
import sys

def padding(data):
    if len(data) % 8 == 2:
        return "======"
    if len(data) % 8 == 4:
        return "===="
    if len(data) % 8 == 5:
        return "==="
    if len(data) % 8 == 7:
        return "=="
    return ""

if __name__ == "__main__":
    if len(sys.argv) < 2:
        quit()

    filename = sys.argv[1]
    extension = "txt" if len(sys.argv) <= 2 else sys.argv[2]
    with open(filename, "rb") as fin, open(filename + "." + extension, "wb") as fout:
        line32 = b"".join(line.strip() for line in fin.readlines())
        fout.write(b32decode(line32+padding(line32).encode()))
