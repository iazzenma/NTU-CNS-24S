import runpy
runpy.run_path('code6c_decrypt.py')

from code6b_lib import Packet, PublicKeyCipher
from data import pk, sk, next_hop, raw

packet = Packet(bytes.fromhex(raw))
while 1:
    if next_hop == 10:
        break
    next_hop, next_packet = packet.decrypt_server(sk[next_hop])
    packet = next_packet
message = packet.decrypt_client(sk[10])
print(message.decode("ascii"))

import os
if os.path.exists('data.py'):
    os.remove('data.py')