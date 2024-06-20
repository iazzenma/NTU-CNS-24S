from pwn import *
import random

s = remote("cns.csie.org", 44444)
s.sendlineafter(b')', b'1').decode()
s.recvlines(6, False)

for _ in range(32):
    line = s.recvline(False).decode()
    i = int(line.split()[-2].strip('(,'))
    j = int(line.split()[-1].strip(')'))

    # Generate a list of 10 random items, each item is either 0 or 1
    mu_0 = [random.randint(0, 1) for _ in range(1024)]
    hatj = [0] * 1024
    hatj[j] = 1
    mu_1 = [mu_0[k] + hatj[k] for k in range(1024)]

    mu_0_string = ','.join(map(str,mu_0))
    mu_1_string = ','.join(map(str,mu_1))
    s.sendlineafter(delim=b'mu_0', data=mu_0_string.encode())
    data = s.recvlines(3, False)
    Xmu_0 = list(map(int, data[2].decode().split(',')))
    s.sendlineafter(delim=b'mu_1', data=mu_1_string.encode())
    data = s.recvlines(3, False)
    Xmu_1 = list(map(int, data[2].decode().split(',')))

    Xj = [Xmu_0[k] + Xmu_1[k] for k in range(1024)]
    tmp = Xj[i]

    s.sendlineafter(delim=b'?', data=str(tmp).encode())
    s.recvline()
print(s.recvline(False).decode())
s.close()