from Crypto.Cipher import AES
import base64

# Given AES key and ciphertext
AES_KEY = b"R0chLi4uLi4uLi4="
ciphertext = "0d3f42e43aa1062c56a7e92dc364ab40"

# Decode the base64-encoded AES key
aes_key_decoded = base64.b64decode(AES_KEY)

# Ensure the key is 16 bytes (128 bits) by padding or truncating
aes_key_decoded = aes_key_decoded.ljust(16, b'\0')[:16]

# Convert the ciphertext to bytes
ciphertext_bytes = bytes.fromhex(ciphertext)

# Initialize AES cipher in ECB mode with the decoded key
cipher = AES.new(aes_key_decoded, AES.MODE_ECB)

# Decrypt the ciphertext
plaintext_bytes = cipher.decrypt(ciphertext_bytes)

# Display the decrypted bytes, hexadecimal representation, and base64-encoded string
print("Decrypted bytes:", plaintext_bytes)
print("Hexadecimal representation:", plaintext_bytes.hex())
print("Base64 encoded string:", base64.b64encode(plaintext_bytes).decode('utf-8'))
