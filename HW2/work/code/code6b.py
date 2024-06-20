from code6b_lib import *
from pwn import *

def get_key(words):
    return int(words[-2][1:-1]), int(words[-1][:-1])

conn = remote('cns.csie.org', 3002)
server_pubkey = []
for _ in range(10):
    words = conn.recvline().decode().split()
    pubkey = get_key(words)
    server_pubkey.append(pubkey)
words = conn.recvline().decode().split()
bob_pubkey = get_key(words)

conn.recvlines(2)
words = conn.recvline().decode().split()
hops = []
for i in range(6):
    hops.append(int(words[7 + i].strip("[],")))

p = Packet.create(b"Give me flag, now!", 10, bob_pubkey)
for i in reversed(range(5)):
    p = p.add_next_hop(hops[i + 1], server_pubkey[hops[i]])

conn.sendline(p.data.hex().encode())
print(conn.recvuntil(b'}').decode())