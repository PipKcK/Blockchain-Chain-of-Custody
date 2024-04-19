#!/usr/bin/env python3

import CONSTANTS as CONS
import struct
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
import binascii
import base64
import uuid
import sys

def pack_and_write_block(block_head, block_data):

    block_head_packed = CONS.H_FORMAT.pack(
        block_head.prevHash.ljust(32, b'\0'),  # Pad with null bytes
        block_head.timestamp,
        aes_ecb_encrypt(uuid.UUID(block_head.case_id).int).encode('utf-8').ljust(32, b'\0'),  # Pad with null bytes
        aes_ecb_encrypt(int(block_head.item_id)).encode('utf-8').ljust(32, b'\0'),  # Pad with null bytes
        block_head.state.ljust(12, b'\0'),  # Pad with null bytes
        block_head.creator.encode('utf-8').ljust(12, b'\0'),  # Pad with null bytes
        block_head.owner.ljust(12, b'\0'),  # Pad with null bytes
        block_head.length
    )
    dFormat = struct.Struct(f'{block_head.length}s')
    # Pack Block Data
    block_data_packed = dFormat.pack(block_data.data)

    # Write to File
    with open(CONS.filePath, 'ab') as file:
        file.write(block_head_packed)
        file.write(block_data_packed)

def get_last_block_with_item_id(item_id):
    blocks_list = unpack_all_blockHead_blockData()
    # Iterate over the blocks_list in reverse order
    for block_head, block_data in reversed(blocks_list):
        if block_head.item_id == aes_ecb_encrypt(int(item_id)):
            return block_head, block_data
    
    # Return None if no block with the given item_id is found
    return None


def aes_ecb_encrypt(data_bytes):
    """
    Encrypts data using AES encryption in ECB mode and returns the result in ASCII hexadecimal format.
    
    Args:
    data_bytes (bytes): The data to encrypt in bytes.
    key (bytes): The AES key for encryption. Must be either 16, 24, or 32 bytes long.

    Returns:
    str: The encrypted data in ASCII hexadecimal format.
    """
    data_bytes = data_bytes.to_bytes(16, byteorder='big')

    # Ensure the data is a multiple of AES block size
    block_size = AES.block_size
    pad_len = block_size - (len(data_bytes) % block_size)
    padding = bytes([pad_len] * pad_len)
    data_padded = data_bytes + padding

    # Create an AES cipher object using ECB mode
    cipher = AES.new(CONS.AES_KEY, AES.MODE_ECB)

    # Encrypt the data
    encrypted_data = cipher.encrypt(data_padded)

    # Convert encrypted data to ASCII hexadecimal and return
    return binascii.hexlify(encrypted_data).decode('utf-8')[:32]

def unpack_all_blockHead_blockData():
    blocks = []
    try:
        with open(CONS.filePath, 'rb') as fp:
            while True:
                hContent = fp.read(CONS.H_FORMAT.size)
                if not hContent:
                    break

                hash_val, timestamp, case_id, item_id, state, creator, owner, length = CONS.H_FORMAT.unpack(hContent)
                # Read data based on the length from the block head
                dFormat = struct.Struct(f'{length}s')
                dataContent = fp.read(length)

                try:
                    hash_val = hash_val.decode('utf-8').strip('\x00')
                    case_id = case_id.decode('utf-8').strip('\x00')
                    item_id = item_id.decode('utf-8').strip('\x00')
                    state = state.decode('utf-8').strip('\x00')
                    creator = creator.decode('utf-8').strip('\x00')
                    owner = owner.decode('utf-8').strip('\x00')
                except UnicodeDecodeError:
                    print("Decoding error occurred. Printing bytes as hexadecimal.")
                    sys.exit(1)
                
                # Check if we read enough data
                if len(dataContent) < length:
                    print(f"Expected {length} bytes, but got {len(dataContent)} bytes.")
                    sys.exit(1)
                    break

                # Creating Block Object
                blockData = CONS.BlockData(*dFormat.unpack(dataContent))
                currentBlockHead = CONS.BlockHead(hash_val, timestamp, case_id, item_id, state, creator, owner, length)
                blocks.append((currentBlockHead, blockData))
                #print_block_head(currentBlockHead)
                #print_block_data(blockData)
        
        return blocks

    except FileNotFoundError:
        print(f"File not found: {CONS.filePath}")
        sys.exit(1)
    except struct.error as se:
        print(f"Error unpacking struct: {se}")
        sys.exit(1)
    except Exception as e:
        print(f"An exception occurred: {e}")
        sys.exit(1)

def print_block_head(blockHead):
    print("Block Head:")
    print(f"  Hash: {blockHead.prevHash}")
    print(f"  Timestamp: {blockHead.timestamp}")
    print(f"  Case ID: {blockHead.case_id}")
    print(f"  Item ID: {blockHead.item_id}")
    print(f"  State: {blockHead.state}")
    print(f"  Creator: {blockHead.creator}")
    print(f"  Owner: {blockHead.owner}")
    print(f"  Length: {blockHead.length}")

def print_block_data(blockData):
    print("Block Data:")
    print(f"  Data: {blockData.data.decode('utf-8')}")
