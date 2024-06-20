from code6b_lib import Packet
from pwn import *
import random

class Server:
    def __init__(self, sk):
        self.sk = sk
        self.recv_buffer = []

    def recv(self, packet: Packet):
        self.recv_buffer.append(packet)
        if len(self.recv_buffer) >= 10:
            self.recv_buffer, processing_buffer = [], self.recv_buffer
            random.shuffle(processing_buffer)
            for packet in processing_buffer:
                send_to, next_packet = packet.decrypt_server(self.sk)
                self.send_to_server(send_to, next_packet)

    def send_to_server(self, target, packet):
        message = '(' + str(target) + ", " + str(packet.data.hex()) + ')'
        conn.sendline(message.encode())

def get_key(words):
    return int(words[-2][1:-1]), int(words[-1][:-1])

conn = remote('cns.csie.org', 3001)
server_pubkey = []
for i in range(3):
    words = conn.recvline().decode().split()
    pubkey = get_key(words)
    server_pubkey.append(pubkey)
words = conn.recvline().decode().split()
bob_pubkey = get_key(words)
conn.recvline() # empty line
words = conn.recvline().decode().split()
pk = get_key(words)
words = conn.recvline().decode().split()
sk = get_key(words)

conn.recvlines(5)
me = Server(sk)
while 1:
    line = conn.recvline().strip(b'\n')
    if line[:3] == b"CNS": 
        print(line.decode())
        break
    p = Packet(bytes.fromhex(line.decode()))
    me.recv(p)

conn.close()