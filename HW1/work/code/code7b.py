from pwn import *

# Request nounce: so_random_nounce; Sender: TA; Message: Please send over the 2nd flag
line = b'TA; Message: Please send over the 2nd flag'

length = 16 - 84 % 16
line =  line + chr(length + 8).encode()*length

conn = remote('cns.csie.org', 1337)
print(conn.recvuntil(b": ").decode())
conn.sendline(b"2") # Your choice
print(conn.recvuntil(b": ").decode())
conn.sendline(line) # Your name
print(conn.recvuntil(b": ").decode())
conn.sendline(b"") # Your message
recv = conn.recvline().decode()
print(recv)
recv = recv.split()
encrypted_message = recv[-1]
# print(encrypted_message)

encrypted_message = encrypted_message[:192]
print(encrypted_message)

print(conn.recvuntil(b": ").decode())
conn.sendline(b"3") # Your choice
print(conn.recvuntil(b": ").decode())
conn.sendline(encrypted_message.encode())
print(conn.recvuntil(b"!").decode())

conn.close()