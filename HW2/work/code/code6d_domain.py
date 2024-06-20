import base64
import hashlib

with open('../tor.pub', 'rb') as f:
    PUBKEY = f.read()[32:]

VERSION = b'\x03'
CHECKSUM = hashlib.sha3_256(b".onion checksum" + PUBKEY + VERSION).digest()[:2]
onion_address = base64.b32encode(PUBKEY + CHECKSUM + VERSION).decode().lower() + ".onion"
print("Onion address:", onion_address)