#!/usr/bin/env python3


import sys
import CONSTANTS as CONS
import os

def init():
    if os.path.exists(CONS.filePath) and check_initial_block(CONS.filePath):
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
        packedHVals = CONS.H_FORMAT.pack(Prev_hash, Timestamp, Case_id, Evidence_id, State, creator, owner, D_length)
        packedDataVals = CONS.D_FORMAT.pack(Data)

        with open(CONS.filePath, 'wb') as file:
            file.write(packedHVals)
            file.write(packedDataVals)
            file.close()
        return True  

def check_initial_block(filePath):
    # Check if the file is large enough to contain both header and data
    if (CONS.H_FORMAT.size + CONS.D_FORMAT.size) > os.path.getsize(filePath):
        sys.exit(1)
        return False

    with open(filePath, 'rb') as file:
        packedHVals = file.read(CONS.H_FORMAT.size)
        packedDataVals = file.read(CONS.D_FORMAT.size)

    actual_block_head = CONS.BlockHead(*CONS.H_FORMAT.unpack(packedHVals))
    actual_block_data = CONS.BlockData(*CONS.D_FORMAT.unpack(packedDataVals))
    
    # Expected values
    expected_block_head = CONS.BlockHead(
        b'\0'*32, 0.0 , b'0'*32, b'0'*32, b'INITIAL\0\0\0\0\0', b'\0'*12, b'\0'*12, 14
    )
    expected_block_data = CONS.BlockData(b'Initial block\0')
    
    if (
        actual_block_head.prevHash == expected_block_head.prevHash and
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
