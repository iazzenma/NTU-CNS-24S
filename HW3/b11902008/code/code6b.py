from pwn import *
from extend_mt19937_predictor import ExtendMT19937Predictor

c = remote("cns.csie.org", 6001)

for _ in range(199):
    predictor = ExtendMT19937Predictor()
    c.recvuntil(b'choice: ').decode()
    c.sendline(b'1')
    data = c.recvuntil(b'your number: ').decode()
    numbers = data.split('\n')
    length = len(numbers) - 1
    my_id = length + 5
    if length < 624:
        c.sendline(b'7')
        continue

    sum = 0
    for i in range(length):
        num = int(numbers[i].split()[-1])
        predictor.setrandbits(num, 32)
        sum += num

    # following players
    for i in range(length + 6, 800):
        num = predictor.predict_getrandbits(32)
        sum += num
    # player 1-5
    _ = [predictor.backtrack_getrandbits(32) for _ in range(794)]
    for i in range(5):
        num = predictor.backtrack_getrandbits(32)
        sum += num

    my_num = (my_id - sum) % 800
    if my_num < 0:
        my_num += 800
    c.sendline(str(my_num).encode())

c.recvuntil(b'choice: ').decode()
c.sendline(b'2')
print(c.recvuntil(b'}').decode())
c.close()