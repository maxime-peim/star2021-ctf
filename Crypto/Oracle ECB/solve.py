from pwn import *
from string import printable

BLOCK_SIZE = 16

def print_state(state):
    padding = (BLOCK_SIZE - len(state) % BLOCK_SIZE) % BLOCK_SIZE
    state += '-' * padding
    print('|'.join(state[i:i+BLOCK_SIZE] for i in range(0, len(state), BLOCK_SIZE)))

def send_recv(conn, payload, block=None):

    conn.recvuntil(b"ou autre chose pour quitter: ")

    conn.sendline(payload)
    conn.recvuntil(b"pond:\n")

    answer = conn.recvline().rstrip().decode()

    return answer[2*BLOCK_SIZE*block:2*BLOCK_SIZE*(block+1)] if block else answer

def attack(conn):

    conn.recvuntil(b"[5] Quitter la demeure de l'oracle\n")
    conn.sendline(b"2")

    pre_length = 0
    for pre_length in range(BLOCK_SIZE):
        payload = b"ff"*pre_length + b"fe"*(BLOCK_SIZE*2)
        answer = send_recv(conn, payload)
        blocks = [answer[i:i+BLOCK_SIZE*2] for i in range(0, len(answer), BLOCK_SIZE*2)]

        if any(b1 == b2 for b1, b2 in zip(blocks, blocks[1:])):
            after_pad = [i for i, (b1, b2) in enumerate(zip(blocks, blocks[1:])) if b1 == b2][0]
            break


    padding = b"ff" * pre_length
    n_blocks_to_discover = len(send_recv(conn, padding)) // (BLOCK_SIZE*2) - after_pad

    print("[+] State:", end="")
    print_state('*' * (BLOCK_SIZE*(after_pad - 1) + BLOCK_SIZE - pre_length) + 'P' * pre_length + 'D' * (BLOCK_SIZE*n_blocks_to_discover))

    flag = b""
    
    block_pos = after_pad + n_blocks_to_discover - 1
    for pos in range(n_blocks_to_discover*BLOCK_SIZE-1, -1, -1):
        payload = padding + b"ff" * pos
        print("[+] To match:", end="")
        print_state('*' * (BLOCK_SIZE*(after_pad - 1) + BLOCK_SIZE - pre_length) + 'P' * pre_length + 'F' * pos + bytes.fromhex(flag.decode()).decode() + '$' + 'D' * pos)
        to_match = send_recv(conn, payload, block_pos)

        found = False

        for c in printable:
            encoded = "{:02x}".format(ord(c)).encode()
            payload = padding + b"ff" * pos + flag + encoded
            block = send_recv(conn, payload, block_pos)
            if block == to_match:
                flag += encoded
                print(f"block : {bytes.fromhex(flag.decode()).decode()}")
                found = True
                break
        
        if not found:
            print("Probleme")
            quit()
            
    return flag

conn = remote("157.159.191.53", 30007)

print(attack(conn))

conn.close()
# HackademINT{7h3_5_1n_3CB_574nd5_f0r_S3cur17y}