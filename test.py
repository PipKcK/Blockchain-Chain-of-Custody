from Crypto.Cipher import AES
import binascii
import uuid
import CONSTANTS as CONS

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
    pad_len = (len(data_bytes) % block_size)
    padding = bytes([pad_len] * pad_len)
    data_padded = data_bytes + padding

    # Create an AES cipher object using ECB mode
    cipher = AES.new(key, AES.MODE_ECB)

    # Encrypt the data
    encrypted_data = cipher.encrypt(data_bytes)

    # Convert encrypted data to ASCII hexadecimal and return
    return binascii.hexlify(encrypted_data).decode('utf-8')

# def aes_ecb_decrypt(encrypted_data_hex):
#     """
#     Decrypts data using AES decryption in ECB mode and returns the result in plain text.
    
#     Args:
#     encrypted_data_hex (str): The encrypted data in ASCII hexadecimal format.
    
#     Returns:
#     str: The decrypted data in plain text.
#     """
#     encrypted_data = binascii.unhexlify(encrypted_data_hex)

#     # Create an AES cipher object using ECB mode
#     cipher = AES.new(CONS.AES_KEY, AES.MODE_ECB)

#     # Decrypt the data
#     decrypted_data_padded = cipher.decrypt(encrypted_data)

#     # Remove the padding
#     pad_len = decrypted_data_padded[-1]
#     decrypted_data = decrypted_data_padded[:-pad_len]

#     # Convert decrypted data to UUID if length is 16 bytes, otherwise to integer
#     if len(decrypted_data) == 16:
#         return str(uuid.UUID(bytes=decrypted_data))
#     else:
#         return str(int.from_bytes(decrypted_data, byteorder='big'))


def aes_ecb_decrypt(encrypted_data_hex, isInt):
    """
    Decrypts data using AES decryption in ECB mode and returns the result in plain text.
    
    Args:
    encrypted_data_hex (str): The encrypted data in ASCII hexadecimal format.
    
    Returns:
    str: The decrypted data in plain text.
    """
    encrypted_data = binascii.unhexlify(encrypted_data_hex)

    # Create an AES cipher object using ECB mode
    cipher = AES.new(CONS.AES_KEY, AES.MODE_ECB)

    # Decrypt the data
    decrypted_data_padded = cipher.decrypt(encrypted_data)

    # Remove the padding
    # pad_len = decrypted_data_padded[-1]
    # decrypted_data = decrypted_data_padded[:-pad_len]

    if isInt:
        # Convert decrypted data to integer
        decrypted_value = int.from_bytes(decrypted_data_padded, byteorder='big')
        return str(decrypted_value)
    else:
        decrypted_uuid = uuid.UUID(bytes=decrypted_data_padded)
        return str(uuid.UUID(str(decrypted_uuid)))


if __name__ == "__main__":
    input = uuid.UUID("119482d8-3fbf-4fa8-8948-d2f38d021ae4")
    #input = 2139665479
    intvalue = input.int
    bytesvalue = intvalue.to_bytes(16)
    key = b"R0chLi4uLi4uLi4="
    encrypted_hex = aes_ecb_encrypt(bytesvalue, key)
    print("Non Encryoted (ASCII Value) : ", input)
    print("Encrypted (ASCII hex):", encrypted_hex, type(encrypted_hex), len(encrypted_hex[:32]))
    print("Original Value " , aes_ecb_decrypt(encrypted_hex , True)) 



