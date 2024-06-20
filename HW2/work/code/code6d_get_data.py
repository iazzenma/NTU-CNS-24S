import socks
import re

socks.set_default_proxy(socks.SOCKS5, "127.0.0.1", 9050, True)

host = 'cns24otgzs5zmn2oztxnmiff7bscpg7kp7p6wnkayjnvr5fzxbqzeuqd.onion'
port = 11729

p_list = []
a_list = []
b_list = []
P_list = []
Q_list = []

for i in range(15):
    s = socks.socksocket()
    s.connect((host, port))
    
    print(f"Connected to {host}:{port}:")
    data = s.recv(4096).decode()
    print(data)
    s.close()

    # Extracting values using regular expressions
    match = re.search(r'y\^2 = x\^3 \+ (\d+)x \+ (\d+) mod (\d+)', data)
    a = int(match.group(1))
    b = int(match.group(2))
    p = int(match.group(3))
    a_list.append(a)
    b_list.append(b)
    p_list.append(p)

    match = re.search(r'P = \((\d+), (\d+)\), flag \* P = \((\d+), (\d+)\)', data)
    P = (int(match.group(1)), int(match.group(2)))
    Q = (int(match.group(3)), int(match.group(4)))
    P_list.append(P)
    Q_list.append(Q)

with open('data.py', 'w') as f:
    f.write(f"a_list = {a_list}\n")
    f.write(f"b_list = {b_list}\n")
    f.write(f"p_list = {p_list}\n")
    f.write(f"P_list = {P_list}\n")
    f.write(f"Q_list = {Q_list}\n")