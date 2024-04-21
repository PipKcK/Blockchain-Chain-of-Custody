import CONSTANTS as CONS
import sys
import util as UTIL
import encryption as AES
import uuid
import datetime

def show_cases():
    blocks_list = UTIL.unpack_all_blockHead_blockData()
    for block_head, block_data in blocks_list:
        if block_head.case_id != "08874cf3-a621-4662-f0bd-6eb7265c9970":
            CONS.CASES_MAP[block_head.case_id] = "TRUE"
    for key in CONS.CASES_MAP:
        print(key)
    sys.exit(0)

def show_items(case_id):
    blocks_list = UTIL.unpack_all_blockHead_blockData()
    CASE_TO_ITEM_MAP = {}
    CASE_TO_ITEM_MAP[case_id] = {}

    for block_head, block_data in blocks_list:
        if block_head.case_id == case_id:
            CASE_TO_ITEM_MAP[case_id][block_head.item_id] = "TRUE"

    for key in CASE_TO_ITEM_MAP[case_id]:
        print(key)

    sys.exit(0)

def show_history(case_id , item_id, num_entries, isReverse, password):

    canDecrypt = False
    if password is not None and password in CONS.PASSWORD_MAP:
        canDecrypt = True
    
    if num_entries is not None:
        num_entries = int(num_entries)

    if isReverse == True and case_id is None and item_id is None:
        blocks_list = UTIL.unpack_all_blockHead_blockData()
        blocks_list = blocks_list[::-1]
        if num_entries is not None and num_entries < len(blocks_list):
            block_list = block_list[:num_entries]
        print_block_list(blocks_list, canDecrypt)
    
    if item_id is not None:
        blocks_list = UTIL.get_block_list_for_item_id(item_id)
        if case_id is not None:
            for block_head, block_data in blocks_list:
                if block_head.case_id != case_id:
                    block_list.remove((block_head, block_data))
        if isReverse == True:
            blocks_list = blocks_list[::-1]
        if num_entries is not None and num_entries < len(blocks_list):
            block_list = block_list[:num_entries]
        print_block_list(blocks_list , canDecrypt)
    
    if case_id is not None:
        block_list = UTIL.get_block_list_for_case_id(case_id)
        if isReverse == True:
            block_list = block_list[::-1]
        if num_entries is not None and num_entries < len(block_list):
            block_list = block_list[:num_entries]
        print_block_list(block_list, canDecrypt)

    block_list = UTIL.unpack_all_blockHead_blockData()
    if isReverse == True:
            block_list = block_list[::-1]
    if num_entries is not None and num_entries < len(block_list):
        block_list = block_list[:num_entries]
    print_block_list(block_list, canDecrypt)
    

def print_block_list(block_list, canDecrypt):
    for block_head, block_data in block_list:
        get_map_object(block_head, canDecrypt)
        print()
    sys.exit(0)
    
def get_map_object(block_head, canDecrypt):
    if canDecrypt:
        if block_head.state == "INITIAL":
            case_id = '00000000-0000-0000-0000-000000000000'
            evidence_id = '0'
        else:
            case_id = block_head.case_id
            evidence_id = block_head.item_id
        print("Case:", case_id)
        print("Item:", evidence_id)
        print("Action:", block_head.state)
        print("Time:", convert_timestamp(block_head.timestamp))
    else:
        if block_head.state == "INITIAL":
            encrypted_case_id = '00000000-0000-0000-0000-000000000000'
            encrypted_item_id = '0'
        else:
            encrypted_case_id = AES.aes_ecb_encrypt(uuid.UUID(block_head.case_id).int) # Pad with null bytes
            encrypted_item_id = AES.aes_ecb_encrypt(int(block_head.item_id)) # Pad with null bytes
        print("Case:", encrypted_case_id)
        print("Item:", encrypted_item_id)
        print("Action:", block_head.state)
        print("Time:", convert_timestamp(block_head.timestamp))

def convert_timestamp(timestamp):
    if timestamp == 0:
        timestamp = datetime.datetime.now().timestamp() 
    dt_object = datetime.datetime.utcfromtimestamp(timestamp)
    formatted_time = dt_object.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
    return f'{formatted_time}'

