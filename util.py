#!/usr/bin/env python3

import CONSTANTS as CONS
import struct
from Crypto.Cipher import AES
from Crypto.Hash import SHA256

import base64

def pack_and_write_block(block_head, block_data):
    # Pack Block Head
    block_head_packed = CONS.H_FORMAT.pack(
        block_head.prevHash,
        block_head.timestamp,
        encrpty_data(block_head.case_id).encode('utf-8'),  # Changed encode to decode
        encrpty_data(block_head.item_id).encode('utf-8'),  # Changed encode to decode
        block_head.state,
        block_head.creator.encode('utf-8'),
        block_head.owner.encode('utf-8'),
        block_head.length
    )

    # Pack Block Data
    block_data_packed = CONS.D_FORMAT.pack(block_data.data)

    # Write to File
    with open(CONS.filePath, 'ab') as file:
        file.write(block_head_packed)
        file.write(block_data_packed)

def get_last_block_with_item_id(item_id):
    return None

def encrpty_data(data):
    # Encode the string data to bytes
    data_bytes = data.encode('utf-8')

    # Hash the data using SHA-256
    hash_object = SHA256.new()
    hash_object.update(data_bytes)
    hash_value = hash_object.digest()

    # Encrypt the hashed value using AES ECB mode
    key = b'R0chLi4uLi4uLi4='  # Key for AES encryption (should be 16, 24, or 32 bytes long)
    cipher = AES.new(key, AES.MODE_ECB)
    encrypted_hash = cipher.encrypt(hash_value)

    # Convert the encrypted bytes to a string using Base64 encoding
    encrypted_hash_str = base64.b64encode(encrypted_hash).decode('utf-8')

    return encrypted_hash_str
