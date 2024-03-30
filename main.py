#!/usr/bin/env python

import argparse
from icecream import ic
import os
import struct
from datetime import datetime
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
import uuid


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
hFormat = struct.Struct('32s d 16s I 12s 32s 32s I')
dFormat = struct.Struct('14s')

blockHeadMap = {}
blockDataMap = {}
blockSequence = []


def main():

    parser = argparse.ArgumentParser(prog='main')

    subparsers = parser.add_subparsers(dest='command')

    #bchoc add -c case_id -i item_id [-i item_id ...] -c creator -p password(creator’s)
    parser_add = subparsers.add_parser('add')
    parser_add.add_argument('-c', '--case_id', required=True, help='Case ID')
    parser_add.add_argument('-i', '--item_id', action='append', required=True, help='Item ID')
    parser_add.add_argument('-C', '--creator', required=True, help='Creator')
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
        add_function(args.command, args.case_id, args.item_id, args.creator, args.password , "NEW BLOCK", 10)

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
        # File doesn't exist, create a block with initial information
        ic("File exist but Initial Block is not present")
        now = datetime.now()
        timestamp = datetime.timestamp(now)
        
        hash_val = b''
        case_id_val = b''
        item_id_val = 0
        state_val = str.encode("INITIAL")
        creator_val = b''
        owner_val = b''
        length_val = 14
        data_vals = str.encode("Initial block")

        packedHVals = hFormat.pack(hash_val, timestamp, case_id_val, item_id_val, state_val, creator_val, owner_val, length_val)
        packedDataVals = dFormat.pack(data_vals)

        # currentBlockHead = BlockHead(*hFormat.unpack(packedHVals))
        # currentBlockData = BlockData(*dFormat.unpack(packedDataVals))

        # Write block data to file
        with open(filePath, 'wb') as file:
            file.write(packedHVals)
            file.write(packedDataVals)
            file.close()  
    return False


def check_initial_block(filePath):
    with open(filePath, 'rb') as file:
        packedHVals = file.read(hFormat.size)
        packedDataVals = file.read(dFormat.size)

    actual_block_head = BlockHead(*hFormat.unpack(packedHVals))
    actual_block_data = BlockData(*dFormat.unpack(packedDataVals))

    if actual_block_head.state.decode().strip('\x00') == "INITIAL" and actual_block_data.data.decode().strip('\x00') == "Initial block":
        return True
    return False

def add_function(command, case_id, item_ids, creator, password, blockData , blockLen):
    if init_function():
        if case_id in blockHeadMap:
            for item_id in item_ids:
                if item_id not in blockHeadMap[case_id]:
                    
                    timestamp = datetime.timestamp(datetime.now())

                    newBlockData = BlockData(blockData)
                    newBlock = BlockHead(None, timestamp , case_id, item_id, 'CHECKEDIN', creator, password, blockLen)

                    blockSequence.append(newBlock)
                    blockHeadMap[case_id][item_id] = []
                    blockHeadMap[case_id][item_id].append(newBlock)
                    blockDataMap[newBlock] = newBlockData

                    pack_and_add_block(newBlock, newBlockData)
                    print("The Block has been added")
                else: 
                    print("Item ID already exists" , item_id)
        else:
            blockHeadMap[case_id] = {}
            add_function(command, case_id, item_ids, creator, password , blockData , blockLen)
    else:
        ic("Initiating New File")
        add_function(command, case_id, item_ids, creator, password, blockData , blockLen)

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

def pack_and_add_block(blockhead , blockdata):
    timestamp = blockhead.timestamp
    hash_val = b'' if blockhead.hash is None else blockhead.hash
    case_id_val = uuid.UUID(blockhead.case_id).bytes
    item_id_val = int(blockhead.item_id)
    state_val = str.encode(blockhead.state)
    creator_val = str.encode(blockhead.creator)
    owner_val = str.encode(blockhead.owner)
    length_val = blockhead.length
    data_vals = str.encode(blockdata.data)

    packedHVals = hFormat.pack(hash_val, timestamp, case_id_val, item_id_val, state_val, creator_val, owner_val, length_val)
    packedDataVals = dFormat.pack(data_vals)

    with open(filePath, 'ab') as file:
        file.write(packedHVals)
        file.write(packedDataVals)
        file.close()

if __name__ == "__main__":
    main()
