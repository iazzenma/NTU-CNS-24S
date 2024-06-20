from pwn import *
import binascii

# Establish a connection to the server
conn = remote('cns.csie.org', 1337)

def send_encrypted_message(conn, ciphertext):
    conn.recvuntil(b": ").decode()
    conn.sendline(b"3")  # Option to send an encrypted message
    conn.sendline(ciphertext)
    return conn.recvline()

def decrypt_byte_by_byte(conn, ciphertext):
    block_size = 16
    block_num = len(ciphertext) // 32
    plaintext = ""

    # Decrypt each block starting from the second one
    for block_index in range(block_num - 1, 0, -1):
        current_block = ciphertext[block_index * block_size * 2 : (block_index + 1) * block_size * 2]
        previous_block = ciphertext[(block_index - 1) * block_size * 2 : block_index * block_size * 2]
        decrypted_block = bytearray(block_size)

        # Decrypt each byte of the block
        for byte_index in range(15, -1, -1):
            padding_byte = block_size - byte_index + 8
            for guess in range(256):
                modified_previous_block = bytearray(block_size)

                # Modify the previous block based on our guess
                modified_previous_block[byte_index] = padding_byte ^ guess ^ int(previous_block[byte_index*2 : (byte_index + 1)*2].decode(), 16)

                # Modify the bytes we already know to produce correct padding
                for known_byte_index in range(byte_index + 1, block_size):
                    modified_previous_block[known_byte_index] = \
                        padding_byte ^ int(previous_block[known_byte_index*2 : (known_byte_index + 1)*2], 16) ^ decrypted_block[known_byte_index]

                # Send the modified blocks to the server
                modified_ciphertext = binascii.hexlify(modified_previous_block) + current_block
                response = send_encrypted_message(conn, bytes(modified_ciphertext))

                # If no padding error, we found the correct byte
                if b"Invalid message" not in response:
                    decrypted_block[byte_index] = guess
                    plaintext = chr(guess) + plaintext
                    break

    return plaintext

print(conn.recvuntil(b": ").decode())
conn.sendline(b"1") # Your choice
print(conn.recvline().decode().strip())
encrypted_message = conn.recvline().strip()
print(encrypted_message)


decrypted_message = decrypt_byte_by_byte(conn, encrypted_message)
print(decrypted_message)