from pwn import *
import base64
import random
from utils import cns_decrypt, cns_encrypt

username = 'cnsStudent'
password = 'hellokdc'
kdc = remote("cns.csie.org", 23471)
kdc.recvuntil(b'> ').decode()

# 1. Register
kdc.sendline(b'1')
kdc.recvuntil(b': ').decode()
kdc.sendline(username.encode())
kdc.recvuntil(b': ').decode()
kdc.sendline(password.encode())
data = kdc.recvuntil(b'> ').decode()
for line in data.split('\n'):
    if "password" in line:
        hash_pw = line.split(": ")[1].strip()
    elif "id" in line:
        id = line.split(": ")[1].strip()
    elif "symmetric_key" in line:
        sk = base64.b64decode(line.split(": ")[1].strip())

# 2. Login
kdc.sendline(b'2')
kdc.recvuntil(b': ').decode()
kdc.sendline(username.encode())
kdc.recvuntil(b': ').decode()
kdc.sendline(password.encode())
kdc.recvuntil(b'> ').decode()

# 3. Request
nonce_A = random.randint(1, 1000000000)
line = f'{nonce_A}'
kdc.sendline(b'3')
kdc.recvuntil(b': ').decode()
kdc.sendline(b'bob')
kdc.recvuntil(b': ').decode()
kdc.sendline(line.encode())
data = kdc.recvuntil(b'> ').decode()
for line in data.split('\n'):
    if "Response" in line:
        re = line.split(": ")[1].strip()
        break
kdc.close()

# decrypt
message = cns_decrypt(sk, re.encode()).decode().split('||')
keyAB = base64.b64decode(message[1].strip())
m2bob = message[3]

bob = remote("cns.csie.org", 23472)
bob.recvuntil(b': ').decode()
bob.sendline(m2bob.encode())
response = bob.recvline(False).decode()
re = response.split(': ')[1]
bob.recvuntil(b': ').decode()


# decrypt again
nonce_B = cns_decrypt(keyAB, re.encode()).decode()
encrypted_response = cns_encrypt(keyAB, str(int(nonce_B) - 1).encode())
bob.sendline(encrypted_response.encode())
data = bob.recvline().decode()
for line in data.split('\n'):
    if "Message" in line:
        re = line.split(": ")[1].strip()
        break
print(cns_decrypt(keyAB, re.encode()).decode())