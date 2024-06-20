from pwn import *
from math import gcd
from itertools import permutations
import sys
import base64

conn = remote('cns.csie.org', 44398)
print(conn.recvuntil(b">").decode())

# Database
conn.sendline(b"1")
database_info = conn.recvuntil(b">").decode()
print(database_info)

hidden = []
hint = []
for line in database_info.split('\n'):
    if "Encrypted Passphrase (Hex-encoded)" in line:
        hidden.append(line.split(":")[1].strip())
    elif "Hint" in line and hint == []:
        hint = line.split('"')[1].strip()

def hex_to_ascii(sequence):
    result = []
    for i in range(0, len(sequence), 2):
        result.append(int(sequence[i:i+2], 16))
    return result

if len(sys.argv) != 2:
    conn.interactive()
    sys.exit()

command = sys.argv[1]

# Affine's Secret
if command == "affine": 
    passphrase = hex_to_ascii(str(hidden[0]))

    def affine_decoder(a: int, b: int, enc):
        size = 256
        ret = ""
        for a_inv in range(1, size):
            if (a * a_inv) % size == 1:
                break
        for i in enc:
            val = a_inv * (i - b) % size
            ret += chr(val)

        return ret

    def solve_linear(letters, digits):
        x1 = ord(letters[0])
        y1 = digits[0]
        x2 = ord(letters[1])
        y2 = digits[1]
        for a in range(256):
            if gcd(a, 256) != 1: continue
            for b in range(256):
                if (y1 == (a*x1 + b) % 256) and (y2 == (a*x2 + b) % 256):
                    return a, b
        assert False

    a, b = solve_linear(hint, passphrase)
    affine_passphrase = affine_decoder(a, b, passphrase)

    conn.sendline(b"2")
    print(conn.recvuntil(b": ").decode())
    conn.sendline(affine_passphrase.encode())
    print(conn.recvline().decode())

# Bob's Secret
elif command == "bob":
    passphrase = hex_to_ascii(str(hidden[1]))
    for i in passphrase:
        print(chr(i), end="")
    print("")
    # Decrypt with online tools and some trial & error
    conn.interactive()

# Eve's Secret
elif command == "eve": 
    passphrase = hex_to_ascii(str(hidden[2]))
    input_string = ""
    print(passphrase)
    for i in passphrase:
        input_string += chr(i)
    

    def decode_polybuis(ciphertext):
        polybius_square = [
            ['A', 'B', 'C', 'D', 'E'],
            ['F', 'G', 'H', 'I', 'K'],
            ['L', 'M', 'N', 'O', 'P'],
            ['Q', 'R', 'S', 'T', 'U'],
            ['V', 'W', 'X', 'Y', 'Z']
        ]
        
        decoded = ""
        i = 0
        while i < len(ciphertext):
            if ciphertext[i] == ' ':
                decoded += ' '
                i += 1
            else: 
                row = int(ciphertext[i]) - 1
                col = int(ciphertext[i + 1]) - 1
                decoded += polybius_square[row][col] 
                i += 2

        return decoded

    def assign_number(string):
        unique_letters = sorted(set(string.replace(" ", "")))  
        letter_to_number = {letter: str(i % 5 + 1) for i, letter in enumerate(unique_letters)}
        print(letter_to_number)
        replaced_strings = []
        for perm in permutations("12345"):  # Generate all permutations of numbers 1-5
            translation_table = str.maketrans({k: v for k, v in zip(unique_letters, perm)})
            replaced_string = string.translate(translation_table)
            replaced_strings.append(replaced_string)

        return replaced_strings

    output_strings = assign_number(input_string)
    with open("eve.txt", "w") as f:
        for idx, string in enumerate(output_strings):
            decoded = decode_polybuis(str(string))
            print(f"{idx + 1}:", decoded, file=f)
    
    # Find readable decoded string w/ human labour
    conn.interactive()

# Admin's Secret
elif command == "admin":
    passphrase = hex_to_ascii(str(hidden[3]))
    encoded = ""
    for i in passphrase:
        encoded += chr(i)
    admin_passphrase = base64.b64decode(encoded).decode('utf-8')
    conn.sendline(b"5")
    print(conn.recvuntil(b": ").decode())
    conn.sendline(admin_passphrase.encode())

    secret = conn.recvuntil(b'>').decode()
    print(secret)
    lines = secret.split('\n')
    for i, line in enumerate(lines):
        if "Please select your action:" in line:
            hex_line = lines[i - 1].strip('"') 
            break
    encrypted = hex_to_ascii(hex_line)

    plain_part = [ord(c) for c in "CNS{"]
    keys = []
    for i in range(len(encrypted) - len(plain_part) + 1):
        key = [encrypted[j] ^ plain_part[j - i] for j in range(i, i + len(plain_part))]
        keys.append(key)

    def output_decrypted(key):
        decrypted = ""
        for i in range(len(encrypted)):
            asc = encrypted[i] ^ key[i % 6]
            if 32 <= asc < 127:  # Check if the ascii code is printable
                decrypted += chr(asc)
            else:
                if i % 6 == 4 or i % 6 == 5:
                    # If the non-printable character is at the end of the key, print what we have and reset
                    decrypted = ""
                    break
                else:
                    # If the non-printable character is not at the end, this key is invalid
                    return "NEXT"
        return decrypted

    tail = list(permutations(range(256), 2))
    with open("admin.txt", "w") as f:
        for key in keys:
            for t in tail:
                full_key = key + list(t)
                decrypted = output_decrypted(full_key)
                if decrypted == "NEXT":
                    break
                elif decrypted:
                    print(decrypted, file=f)