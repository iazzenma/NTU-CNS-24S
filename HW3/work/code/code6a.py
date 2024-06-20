from pwn import *

c = remote("cns.csie.org", 6000)

my_id = 799
for _ in range(25):
    c.recvuntil(b'choice: ').decode()
    c.sendline(b'1')
    sum = 0
    for i in range(799):
        line = c.recvline(False).decode()
        number = int(line.split()[-1])
        sum += number

    my_num = (my_id - sum) % 800
    if my_num < 0:
        my_num += 800
    c.recvuntil(b': ').decode()
    c.sendline(str(my_num).encode())

c.recvuntil(b'choice: ').decode()
c.sendline(b'2')
print(c.recvuntil(b'}').decode())