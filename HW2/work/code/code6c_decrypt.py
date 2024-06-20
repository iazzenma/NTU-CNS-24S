from pwn import *
import sage.all as sage

def get_sk(public_key):
    n, e = public_key    
    F = sage.factor(n)
    p, q = F[0][0], F[1][0]    
    phi_n = (p - 1) * (q - 1)    
    d = pow(e, -1, phi_n)
    return (n, d)

def get_key(words):
    return int(words[-2][1:-1]), int(words[-1][:-1])

conn = remote('cns.csie.org', 3003)
pk, sk = [], []
for _ in range(11):
    words = conn.recvline().decode().split()
    pubkey = get_key(words)
    pk.append(pubkey)
    secretk = get_sk(pubkey)
    sk.append(secretk)

lines = conn.recvlines(2)
line = lines[-1]
words = line.decode().split()
next_hop = int(words[-1].strip(':'))

raw = conn.recvline().decode().strip('\n')
conn.close()

with open('data.py', 'w') as f:
    f.write(f"pk = {pk}\n")
    f.write(f"sk = {sk}\n")
    f.write(f"next_hop = {next_hop}\n")
    f.write(f"raw = '{raw}'\n")

exec