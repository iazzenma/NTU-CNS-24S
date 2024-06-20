from pwn import *
import hashlib
import HashTools

conn = remote('cns.csie.org', 9010)

def shopping(collision1, collision2):
    # buy 2 stuff that collides
    conn.sendline(b"1")
    conn.recvuntil(b": ").decode() # product name
    conn.sendline(collision1)
    conn.recvuntil(b": ").decode() # amount
    conn.sendline(b"10")

    conn.recvuntil(b": ").decode() # your choice
    conn.sendline(b"1")
    conn.recvuntil(b": ").decode() # product name
    conn.sendline(collision2)
    conn.recvuntil(b": ").decode() # amount
    conn.sendline(b"10")

    # buy lottery 3 times
    conn.recvuntil(b": ").decode() # your choice
    conn.sendline(b"2")
    conn.recvuntil(b": ").decode() # your choice
    conn.sendline(b"2")
    conn.recvuntil(b": ").decode() # your choice
    conn.sendline(b"2")

    # buy flag
    conn.recvuntil(b": ").decode() # your choice
    conn.sendline(b"3")

def sha1(s) -> bytes:
    if isinstance(s, str):
        s = s.encode()
    h = hashlib.sha1()
    h.update(s)
    return h.digest()

def sha256(s) -> bytes:
    if isinstance(s, str):
        s = s.encode()
    h = hashlib.sha256()
    h.update(s)
    return h.digest()


prefix = "CNS2024"
suffix = 0
data = conn.recvuntil(b':').decode()
target = data.split()[-1][:-1]

while True:
    test = prefix + str(suffix)
    hash_value = hashlib.sha256(test.encode()).hexdigest()
    if target == hash_value[-6:]:
        print("Partial collision found! ", hash_value)
        break

    suffix += 1

conn.sendline(test.encode())
conn.recvuntil(b": ").decode() # your choice


# *stage 1
f1 = open("../shattered-1.pdf", "rb")
f2 = open("../shattered-2.pdf", "rb")

collision1 = f1.read() + b'CNS2024'
collision2 = f2.read() + b'CNS2024'

shopping(collision1, collision2)

# get flag & key
st2 = conn.recvuntil(b": ").decode()
print(st2)
lines = st2.split('\n') 
key = ""
for line in lines: 
    if "Your key is" in line:
        key = line.split()
        key = key[-1].strip(".")

# *stage 2 birthday attack
sha2plain = {}
new_prefix = prefix + str(key)
collision1 = ""
collision2 = ""

while True:
    test = new_prefix + str(suffix)
    hash_value = sha256(test)[-4:]
    if hash_value in sha2plain:
        print("Partial collision found! ", hash_value)
        collision1 = test.encode()
        collision2 = sha2plain[hash_value]
        break
    sha2plain[hash_value] = test.encode()
    suffix += 1

print(f"Going shopping for {collision1} and {collision2}")
shopping(collision1, collision2)

# get flag & ID
stg3 = conn.recvuntil(b": ").decode()
print(stg3)
lines = stg3.split('\n') 
ID = ""
for line in lines: 
    if "Your ID is" in line:
        ID = line.split()
        ID = ID[3].strip("!")

# TODO stage 3
for i in range(40, 51):
    magic = HashTools.new("sha256")
    new_data, new_sig = magic.extension(
        secret_length= i + len("key=&identity="), original_data=b"staff",
        append_data=b"admin", signature=ID
    )
    conn.sendline(b'1')
    conn.recvuntil(b': ').decode()# ID
    conn.sendline(new_sig.encode())
    conn.recvuntil(b': ').decode() # identity
    conn.sendline(new_data)
    result = conn.recvline().decode() # get result
    if "admin" in result:
        print(conn.recvline().decode()) # get flag
        break
    else:
        conn.recvuntil(b': ').decode() # ID

conn.close()