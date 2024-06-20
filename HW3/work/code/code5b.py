from pwn import *
import random

s = remote("cns.csie.org", 44444)
s.sendlineafter(b')', b'2').decode()
s.recvlines(3, False)

for _ in range(32):
    data = s.recvuntil(b'?').decode().split('\n')
    mu_0 = list(map(int, data[1].split(', ')))
    mu_1 = list(map(int, data[3].split(', ')))

    for k in range(1024):
        if mu_1[k] != mu_0[k]:
            j = k
            break
    s.sendline(str(j).encode())
    s.recvline()
print(s.recvline(False).decode())