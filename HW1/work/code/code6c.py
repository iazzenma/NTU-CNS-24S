from pwn import *
from Crypto.Util.number import long_to_bytes
from gmpy2 import invert
from gmpy2 import iroot

def mul(lst):
    ret = 1
    for n in lst:
        ret *= n
    return ret

def crt(C, N):
    assert len(C) == len(N)

    total = 0
    modulo = mul(N)

    for n_i, c_i in zip(N, C):
        p = modulo // n_i
        total += c_i * invert(p, n_i) * p
    return total % modulo

def root(n):
    m, valid = iroot(n, e)
    if valid:
        print("Cleartext :", long_to_bytes(m))
    else:
        print("Unable to find the 7th root of :", n)

# get 7 pairs of e, c
n_list = []
c_list = []
for i in range(7):
    conn = remote('cns.csie.org', 44399)
    _ = conn.recvuntil(b">").decode()
    conn.sendline(b"1")
    database_info = conn.recvuntil(b">").decode()

    lines = database_info.split('\n')
    for i, line in enumerate(lines):
        if "Username                           : eve" in line:
            n_list.append(int(lines[i + 1].split(":")[1].strip()))
            e = int(lines[i + 2].split(":")[1].strip())
            break
    
    conn.sendline(b"4")
    eve_ciphertext = conn.recvline().decode()
    c_list.append(int(eve_ciphertext.split(":")[1].strip()))
    conn.close()

x = crt(c_list, n_list)
root(x)