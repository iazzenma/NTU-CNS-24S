import socks

socks.set_default_proxy(socks.SOCKS5, "127.0.0.1", 9050, True)

host = 'cns24otgzs5zmn2oztxnmiff7bscpg7kp7p6wnkayjnvr5fzxbqzeuqd.onion'

for port in range(1, 65536):
    try:
        s = socks.socksocket()
        s.connect((host, port))
        
        print(f"Connected to {host}:{port}")
        data = s.recv(4096)
        print(f"Data received from port {port}: {data}")
        
        s.close()
        
        break
        
    except Exception as e:
        print(f"Error connecting to port {port}: {e}")
        continue