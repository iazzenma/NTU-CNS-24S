from pwn import *

Carrol_Pub_Key = {
    'p': 152935368678367157405317178287373734093175246796781691729969576483125898828139447276413187754833118100330374611127958058135819938872368718152359240661176320069868252547073278933718970254912266807511531207665638680966473567203584135224561658074295134497737147848276884525490861006993057088080733260131645704987,
    'g': 13,
    'y': 146772156355252062500971022708324573741998422695251431194188045128446492160730833110982749640173413368206404431357458050210046096820326551621776204707702934224310394920109906063262864563184606472069439355954850098031057201281224496301884743230468556316892424078411323948744468187910905935664289911754021855586
}
Carrol_p, Carrol_g, Carrol_y = Carrol_Pub_Key['p'], Carrol_Pub_Key['g'], Carrol_Pub_Key['y']

rng_a = 0xc814b5bd7461e52483115b6fff1c020c96f1a90ce173a0877e7579acff457864eb5185531123b965f68286988b1e55d9c7b06915a8637f63294d661d44939aa7
rng_c = 0x6369d6d9eed8bda45c2764a559500a11a1e695a57554b5f5f904bea20377bd77df435169b8d2e0669fd1a3d4bc4776ef3849d4ae1e3b12e7c80ac23155435b8f

# Obtain c
conn = remote('cns.csie.org', 23462)
print(conn.recvuntil(b'> ').decode())
conn.sendline(b'Carrol')
print(conn.recvuntil(b'= ').decode()) # a
conn.sendline(b'1')
line = conn.recvline().decode()
print(line)
print(conn.recvuntil(b'= ').decode()) # w
conn.sendline(b'1')

# Calculation
c = line[4:-1]
prev_c = int(c)
next_c = (rng_a * prev_c + rng_c) % Carrol_p
tmp = pow(Carrol_y, next_c, Carrol_p)
a = pow(tmp, -1, Carrol_p)

# Attack
print(conn.recvuntil(b'> ').decode()) # w
conn.sendline(b'Carrol')
print(conn.recvuntil(b'= ').decode()) # a
conn.sendline(str(a).encode())
print(conn.recvline().decode())
print(conn.recvuntil(b'= ').decode()) # w
conn.sendline(b'0')
print(conn.recvuntil(b'> ').decode()) # w
conn.close()