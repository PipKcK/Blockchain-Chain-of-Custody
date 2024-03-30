import secrets

# Generate a random 16-byte (128-bit) key for AES encryption
key_aes_128 = secrets.token_bytes(16)  # 16 bytes = 128 bits

# Generate a random 24-byte (192-bit) key for AES encryption
key_aes_192 = secrets.token_bytes(24)  # 24 bytes = 192 bits

# Generate a random 32-byte (256-bit) key for AES encryption
key_aes_256 = secrets.token_bytes(32)  # 32 bytes = 256 bits

print("AES-128 Key:", key_aes_128)
print("AES-192 Key:", key_aes_192)
print("AES-256 Key:", key_aes_256)
