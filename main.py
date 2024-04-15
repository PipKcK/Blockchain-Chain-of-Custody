#!/usr/bin/env python

import argparse
from icecream import ic
import os
import struct
from datetime import datetime
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
import uuid
import sys


#Authors: ZebraCatPenguin: Ujjwal, Wejdan

#bchoc add -c case_id -i item_id [-i item_id ...] -c creator -p password(creator’s)
#bchoc checkout -i item_id -p password
#bchoc checkin -i item_id -p password
#bchoc show cases -p password
#bchoc show items -c case_id -p password
#bchoc show history [-c case_id] [-i item_id] [-n num_entries] [-r] -p password
#bchoc remove -i item_id -y reason -p password(creator’s)
#bchoc init
#bchoc verify

class BlockHead:
    def __init__(self, hash, timestamp, case_id, item_id, state, creator, owner, length):
        self.hash = hash
        self.timestamp = timestamp
        self.case_id = case_id
        self.item_id = item_id
        self.state = state
        self.creator = creator
        self.owner = owner
        self.length = length

class BlockData:
    def __init__(self, data):
        self.data = data

filePath = "/Users/sidpro/Desktop/CSE 469/Final Project/Blockchain-Chain-of-Custody/BlockChain.bin"
hFormat = struct.Struct('32s d 32s 32s 12s 12s 12s I')
dFormat = struct.Struct('14s')

blockHeadMap = {}
blockDataMap = {}
blockSequence = []


def main():

    init_load_blocks(filePath)
    print_block_info()

    parser = argparse.ArgumentParser(prog='main')
    subparsers = parser.add_subparsers(dest='command')

    #bchoc add -c case_id -i item_id [-i item_id ...] -c creator -p password(creator’s)
    parser_add = subparsers.add_parser('add')
    parser_add.add_argument('-c', '--case_id', required=True, help='Case ID')
    parser_add.add_argument('-i', '--item_id', action='append', required=True, help='Item ID')
    parser_add.add_argument('-g', '--creator', required=True, help='Creator')
    parser_add.add_argument('-p', '--password', required=True, help='Password')

    #bchoc checkout -i item_id -p password
    parser_checkout = subparsers.add_parser('checkout')
    parser_checkout.add_argument('-i', '--item_id', required=True, help='Item ID')
    parser_checkout.add_argument('-p', '--password', required=True, help='Password')

    #bchoc checkin -i item_id -p password
    parser_checkin = subparsers.add_parser('checkin')
    parser_checkin.add_argument('-i', '--item_id', required=True, help='Item ID')
    parser_checkin.add_argument('-p', '--password', required=True, help='Password')

    #bchoc show cases -p password
    #bchoc show items -c case_id -p password
    #bchoc show history [-c case_id] [-i item_id] [-n num_entries] [-r] -p password
    parser_show = subparsers.add_parser('show')
    show_subparsers = parser_show.add_subparsers(dest='show_command')

    #bchoc show cases -p password
    parser_show_cases = show_subparsers.add_parser('cases')
    parser_show_cases.add_argument('-p', '--password', required=True, help='Password')

    #bchoc show items -c case_id -p password
    parser_show_items = show_subparsers.add_parser('items')
    parser_show_items.add_argument('-c', '--case_id', required=True, help='Case ID')
    parser_show_items.add_argument('-p', '--password', required=True, help='Password')

    #bchoc show history [-c case_id] [-i item_id] [-n num_entries] [-r] -p password
    parser_show_history = show_subparsers.add_parser('history')
    parser_show_history.add_argument('-c', '--case_id', required=False, help='Case ID')
    parser_show_history.add_argument('-i', '--item_id', required=False, help='Item ID')
    parser_show_history.add_argument('-n', '--num_entries', required=False, help='Number of entries')
    parser_show_history.add_argument('-r', '--reverse', action='store_true', required=False, help='Reverse')
    parser_show_history.add_argument('-p', '--password', required=True, help='Password')

    #bchoc remove -i item_id -y reason -p password(creator’s)
    parser_remove = subparsers.add_parser('remove')
    parser_remove.add_argument('-i', '--item_id', required=True, help='Item ID')
    parser_remove.add_argument('-y', '--reason', required=True, help='Reason')
    parser_remove.add_argument('-p', '--password', required=True, help='Password')

    # bchoc init
    subparsers.add_parser('init')

    # bchoc verify
    subparsers.add_parser('verify')

    args = parser.parse_args()

    if args.command == 'add':
        ic(args.command)
        ic(args.case_id)
        ic(args.item_id)
        ic(args.creator)
        ic(args.password)
        add_function(args.case_id, args.item_id, args.creator, args.password , "NEW BLOCK", 9, True)
        print_block_info()


    if args.command == 'checkout':
        ic(args.command)
        ic(args.item_id)
        ic(args.password)
        # checkout_function()

    if args.command == 'checkin':
        ic(args.command)
        ic(args.item_id)
        ic(args.password)
        # checkin_function()

    if args.command == 'show':
        if args.show_command == 'cases':
            ic(args.show_command)
            ic(args.password)
            # show_cases_function()
        if args.show_command == 'items':
            ic(args.show_command)
            ic(args.case_id)
            ic(args.password)
            # show_items_function()
        if args.show_command == 'history': # Note: If optional args are not provided, they will be None
            ic(args.show_command)
            ic(args.case_id)
            ic(args.item_id)
            ic(args.num_entries)
            ic(args.reverse)
            ic(args.password)
            # show_history_function()
    
    if args.command == 'remove': # Note: If optional args are not provided, they will be None
        ic(args.command)
        ic(args.item_id)
        ic(args.reason)
        ic(args.password)
        # remove_function()

    if args.command == 'init':
        ic(args.command)
        init_function()

    if args.command == 'verify':
        ic(args.command)
        # verify_function()


def init_function():
    if os.path.exists(filePath) and check_initial_block(filePath):
        ic("File Exist and Initial Block is present")
        return True
    else: 
        Prev_hash = b''*32  # 32 bytes
        Timestamp = 0  # 08 bytes
        Case_id = b'0'*32      # 32 bytes (32 zero's)
        Evidence_id = b'0'*32  # 32 bytes (32 zero's)
        State = b'INITIAL\0\0\0\0\0'  # 12 bytes
        creator = b'\0'*12    # 12 bytes (12 null bytes)
        owner = b'\0'*12       # 12 bytes (12 null bytes)
        D_length = 14  # 04 bytes
        Data = b'Initial block\0'  # 14 bytes
                                  #   32s         d         32s      32s         12s     12s      12s     I
        packedHVals = hFormat.pack(Prev_hash, Timestamp, Case_id, Evidence_id, State, creator, owner, D_length)
        packedDataVals = dFormat.pack(Data)

        with open(filePath, 'wb') as file:
            file.write(packedHVals)
            file.write(packedDataVals)
            file.close()
        return True  

def init_load_blocks(filePath):
    if not os.path.exists(filePath) or not check_initial_block(filePath):
        ic("File not found or Initial block not found. Creating new file.")
        init_function()
        return

    try:
        with open(filePath, 'rb') as fp:
            while True:
                hContent = fp.read(hFormat.size)
                if not hContent:
                    break

                currentBlockHead = BlockHead(*hFormat.unpack(hContent))
                ic('BlockData Length', currentBlockHead.length)

                dFormat = struct.Struct(str(currentBlockHead.length) + 's')

                dataContent = fp.read(dFormat.size)
                currentBlockData = BlockData(*dFormat.unpack(dataContent))

                add_block_to_maps(currentBlockHead, currentBlockData)

    except Exception as e:
        print("An exception occurred:", e)
        sys.exit(1)

def add_block_to_maps(blockHead, blockData):
    case_id = blockHead.case_id
    item_id = blockHead.item_id

    if case_id not in blockHeadMap:
        blockHeadMap[case_id] = {}
    
    if item_id not in blockHeadMap[case_id]:
        blockHeadMap[case_id][item_id] = []
    
    blockHeadMap[case_id][item_id].append(blockHead)
    blockDataMap[blockHead] = blockData
    blockSequence.append(blockHead)

def check_initial_block(filePath):
    # Check if the file is large enough to contain both header and data
    if (hFormat.size + dFormat.size) > os.path.getsize(filePath):
        print("Blockchain file is too small.")
        return False

    with open(filePath, 'rb') as file:
        packedHVals = file.read(hFormat.size)
        packedDataVals = file.read(dFormat.size)

    actual_block_head = BlockHead(*hFormat.unpack(packedHVals))
    actual_block_data = BlockData(*dFormat.unpack(packedDataVals))
    
    # Expected values
    expected_block_head = BlockHead(
        b'\0'*32, 0.0 , b'0'*32, b'0'*32, b'INITIAL\0\0\0\0\0', b'\0'*12, b'\0'*12, 14
    )
    expected_block_data = BlockData(b'Initial block\0')
    
    if (
        actual_block_head.hash == expected_block_head.hash and
        actual_block_head.timestamp == expected_block_head.timestamp and
        actual_block_head.case_id == expected_block_head.case_id and
        actual_block_head.item_id == expected_block_head.item_id and
        actual_block_head.state == expected_block_head.state and
        actual_block_head.creator == expected_block_head.creator and
        actual_block_head.owner == expected_block_head.owner and
        actual_block_head.length == expected_block_head.length and
        actual_block_data.data == expected_block_data.data
    ):
        print("\nBlockchain file found with INITIAL block.")
        return True
    
    print("\nBlockchain file does not contain the expected INITIAL block.")
    return False


# def add_function(case_id, item_ids, creator, password, blockData , blockLen , toWrite):
#     if  init_function():  
#                            # Check if the file is initialized              
#         if case_id not in blockHeadMap:
#                 blockHeadMap[case_id] = {}
#         for item_id in item_ids:
#             if item_id not in blockHeadMap[case_id]:
#                 timestamp = datetime.timestamp(datetime.now())
#                 newBlockData = BlockData(blockData)
#                 newBlock = BlockHead(None, timestamp , case_id, item_id, 'CHECKEDIN', creator, password, blockLen)

#                 blockSequence.append(newBlock)
#                 blockHeadMap[case_id][item_id] = []
#                 blockHeadMap[case_id][item_id].append(newBlock)
#                 blockDataMap[newBlock] = newBlockData
#                 if toWrite:
#                     pack_and_add_block(newBlock, newBlockData)
#                 print("The Block has been added")
#             else: 
#                 print("Item ID already exists" , item_id)     

def add_function(case_id, item_ids, creator, password, blockData, blockLen, toWrite):
    print("Inside add_function")
    if init_function() == True:
        print(f"File initialized: {filePath}")
        if case_id not in blockHeadMap:
            print(f"Case ID {case_id} does not exist in blockHeadMap")
            blockHeadMap[case_id] = {}
        for item_id in item_ids:
            if item_id not in blockHeadMap[case_id]:
                timestamp = datetime.timestamp(datetime.now())
                newBlockData = BlockData(blockData)
                newBlock = BlockHead(None, timestamp, case_id, item_id, 'CHECKEDIN', creator, password, blockLen)

                blockSequence.append(newBlock)
                blockHeadMap[case_id][item_id] = []
                blockHeadMap[case_id][item_id].append(newBlock)
                blockDataMap[newBlock] = newBlockData

                if toWrite:
                    print("Writing block to file")
                    pack_and_add_block(newBlock, newBlockData)
                
                print("The Block has been added")
            else:
                print("Item ID already exists", item_id)            
    else:
        print("File not initialized. Initiating new file.")
        add_function(case_id, item_ids, creator, password, blockData, blockLen, toWrite)

def encrpty_data(data, password):

    # First, hash the data using a secure hash function like SHA-256
    hash_object = SHA256.new()
    hash_object.update(data)
    hash_value = hash_object.digest()

    # Then, encrypt the hashed value using AES ECB mode
    key = b'yn2E\x8fp\xa9\xcb\x8a[\xff!\xe5\x8d\xf7\xc1'  # Key for AES encryption (should be 16, 24, or 32 bytes long)
    cipher = AES.new(key, AES.MODE_ECB)
    encrypted_hash = cipher.encrypt(hash_value)

    # Now, 'encrypted_hash' contains the hashed value of 'data' using AES ECB mode
    print(encrypted_hash)

    return encrypted_hash

def pack_and_add_block(blockhead, blockdata):

    timestamp = blockhead.timestamp
    hash_val = b'' if blockhead.hash is None else blockhead.hash
    case_id_val = str(blockhead.case_id).encode('utf-8')
    item_id_val = int(blockhead.item_id).to_bytes(4, byteorder='big')  # Assuming item_id is 4 bytes
    state_val = blockhead.state.encode('utf-8')
    creator_val = blockhead.creator.encode('utf-8')
    owner_val = blockhead.owner.encode('utf-8')
    length_val = blockhead.length
    data_vals = blockdata.data.encode('utf-8')

    # Define the format string
    #hFormat = struct.Struct('32s d 16s I 12s 12s 12s I')

    # Pack the values
    packedHVals = hFormat.pack(
        hash_val, timestamp, case_id_val, item_id_val, state_val, creator_val, owner_val, length_val
    )
    packedDataVals = data_vals  # No need to pack a single value

    with open(filePath, 'ab') as file:
        file.write(packedHVals)
        file.write(packedDataVals)

def print_block_info():
    print("blockHeadMap:")
    for case_id, item_ids in blockHeadMap.items():
        print(f"Case ID: {case_id}")
        for item_id, blocks in item_ids.items():
            print(f"\tItem ID: {item_id}")
            for block in blocks:
                print(f"\t\tBlock Head: {block}")
    
    print("\nblockDataMap:")
    for block, block_data in blockDataMap.items():
        print(f"Block Head: {block}")
        print(f"\tBlock Data: {block_data}")
    
    print("\nblockSequence:")
    for block in blockSequence:
        print(block)


if __name__ == "__main__":
    main()
