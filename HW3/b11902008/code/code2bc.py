import hashlib
import ast
from utils import cns_decrypt, cns_encrypt

username = 'admin'
id = '6355c19cd0b04fd394796186a77a3944'
hased_pw = 'efb8a0cd6c2407b099cadde0d4e72bbd7884bf8aef764d44103c624ffaf84d11'

f = open("../common_roots.txt", "r")
while True:
    password = f.readline().strip()
    if hased_pw == hashlib.sha256(password.encode()).hexdigest():
        pw = password
        break
print('admin\'s password = ', pw)

from pwn import *

# 2. login
kdc = remote("cns.csie.org", 23471)
kdc.recvuntil(b'> ').decode()
kdc.sendline(b'2')
kdc.recvuntil(b': ').decode()
kdc.sendline(username.encode())
kdc.recvuntil(b': ').decode()
kdc.sendline(pw.encode())
data = kdc.recvuntil(b'> ').decode()
for line in data.split('\n'):
    if 'flag' in line:
        print(line)
        break

# 4. view log
kdc.sendline(b'4')
string_data = kdc.recvline(False).decode()
kdc.close()
data_list = ast.literal_eval(string_data)
for entry in data_list:
    if entry['userA'] == 'alice':
        keyAB_value = entry['keyAB']
        forward_message = entry['forward_message']
        break

keyAB = base64.b64decode(keyAB_value.strip())

bob = remote("cns.csie.org", 23472)
bob.recvuntil(b': ').decode()
bob.sendline(forward_message.encode())
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