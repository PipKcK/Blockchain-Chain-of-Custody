#!/usr/bin/env python3

import CONSTANTS as CONS
import encryption as AES
import util as UTIL

import struct
import uuid
import sys
from datetime import datetime
import hashlib
import binascii


def pack_block(block_head, block_data):

    block_head_packed = CONS.H_FORMAT.pack(
        block_head.prevHash.ljust(32, b'\0'),  # Pad with null bytes
        block_head.timestamp,
        AES.aes_ecb_encrypt(uuid.UUID(block_head.case_id).int).encode('utf-8').ljust(32, b'\0'),  # Pad with null bytes
        AES.aes_ecb_encrypt(int(block_head.item_id)).encode('utf-8').ljust(32, b'\0'),  # Pad with null bytes
        block_head.state.encode('utf-8').ljust(12, b'\0'),  # Pad with null bytes
        block_head.creator.encode('utf-8').ljust(12, b'\0'),  # Pad with null bytes
        block_head.owner.encode('utf-8').ljust(12, b'\0'),  # Pad with null bytes
        block_head.length
    )

    dFormat = struct.Struct(f'{block_head.length}s')
    # Pack Block Data
    block_data_packed = dFormat.pack(block_data.data.encode('utf-8'))
    return block_head_packed, block_data_packed

def pack_and_write_block(block_head, block_data):
    
    block_head_packed, block_data_packed = pack_block(block_head, block_data)
    # Write to File
    with open(CONS.filePath, 'ab') as file:
        file.write(block_head_packed)
        file.write(block_data_packed)

def get_last_block_with_item_id(item_id):
    blocks_list = unpack_all_blockHead_blockData()
    # Iterate over the blocks_list in reverse order
    for block_head, block_data in reversed(blocks_list):
        if block_head.item_id == item_id:
            return block_head, block_data
    # Return None if no block with the given item_id is found
    return None

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
                    hash_val = hash_val.decode('utf-8').strip('\x00').encode('utf-8')
                    case_id = case_id.decode('utf-8').strip('\x00')
                    item_id = item_id.decode('utf-8').strip('\x00')
                    state = state.decode('utf-8').strip('\x00')
                    creator = creator.decode('utf-8').strip('\x00')
                    owner = owner.decode('utf-8').strip('\x00')
                except UnicodeDecodeError:
                    print("Decoding error occurred. Printing bytes as hexadecimal.")
                    sys.exit(1)

                try:
                    case_id = AES.aes_ecb_decrypt(case_id, False)
                    item_id = AES.aes_ecb_decrypt(item_id, True)
                except UnicodeDecodeError:
                    print("Failed to decrypt case_id or item_id. Exiting.")
                    sys.exit(1)

                # Check if we read enough data
                if len(dataContent) < length:
                    print(f"Expected {length} bytes, but got {len(dataContent)} bytes.")
                    sys.exit(1)
                    break

                # Creating Block Object
                blockData = CONS.BlockData(*dFormat.unpack(dataContent))
                blockData.data = blockData.data.decode('utf-8')

                currentBlockHead = CONS.BlockHead(hash_val, timestamp, case_id, item_id, state, creator, owner, length)
                blocks.append((currentBlockHead, blockData))
                # print_block_head(currentBlockHead)
                # print_block_data(blockData)
        
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


def check_password(password):
    if password not in CONS.PASSWORD_MAP:
        print("Error: Invalid password")
        sys.exit(1)

def change_status_and_add_block(item_id, new_state, owner):
    last_block_pair = get_last_block_with_item_id(item_id)
    last_block_head = last_block_pair[0]
    last_block_data = last_block_pair[1]

    #packed_last_block_head = CONS.H_FORMAT.pack(last_block_head.prevHash, last_block_head.timestamp, last_block_head.case_id, last_block_head.item_id, last_block_head.state, last_block_head.creator, last_block_head.owner, last_block_head.length)
    #packed_last_block_data = CONS.D_FORMAT.pack(last_block_data.data)

    packed_last_block_head , packed_last_block_data = pack_block(last_block_head, last_block_data)
    last_block_hex = hashlib.sha256(packed_last_block_head + packed_last_block_data).digest()
    
    new_block_head = CONS.BlockHead(
        last_block_hex,
        datetime.now().timestamp(),
        last_block_head.case_id,
        last_block_head.item_id,
        new_state,
        last_block_head.creator,
        owner,
        last_block_head.length
    )

    new_block_data = CONS.BlockData(last_block_data.data)

    UTIL.pack_and_write_block(new_block_head, new_block_data)


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


