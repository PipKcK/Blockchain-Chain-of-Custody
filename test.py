from Crypto.Cipher import AES
import binascii
import uuid

def aes_ecb_encrypt(data_bytes, key):
    """
    Encrypts data using AES encryption in ECB mode and returns the result in ASCII hexadecimal format.
    
    Args:
    data_bytes (bytes): The data to encrypt in bytes.
    key (bytes): The AES key for encryption. Must be either 16, 24, or 32 bytes long.

    Returns:
    str: The encrypted data in ASCII hexadecimal format.
    """

    # Ensure the data is a multiple of AES block size
    block_size = AES.block_size
    pad_len = block_size - (len(data_bytes) % block_size)
    padding = bytes([pad_len] * pad_len)
    data_padded = data_bytes + padding

    # Create an AES cipher object using ECB mode
    cipher = AES.new(key, AES.MODE_ECB)

    # Encrypt the data
    encrypted_data = cipher.encrypt(data_padded)

    # Convert encrypted data to ASCII hexadecimal and return
    return binascii.hexlify(encrypted_data).decode('utf-8')[:32]



if __name__ == "__main__":
    input = uuid.UUID("119482d8-3fbf-4fa8-8948-d2f38d021ae4")
    intvalue = int("2139665479")
    bytesvalue = intvalue.to_bytes(16)
    key = b"R0chLi4uLi4uLi4="
    encrypted_hex = aes_ecb_encrypt(bytesvalue, key)
    print("Encrypted (ASCII hex):", encrypted_hex)

