
import CONSTANTS as CONS
import sys
import util as UTIL
import encryption as AES
import uuid

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

def history_case_id(case_id , item_id, password, num_entries, isReverse):

    canDecrypt = False
    if password is not None and password in CONS.PASSWORD_MAP:
        canDecrypt = True
    
    blocks_list = UTIL.unpack_all_blockHead_blockData()
    result_blocks = []
    if isReverse is not None and case_id is None and item_id is None and num_entries is None:
        blocks_list = blocks_list[::-1]
        for block_head, block_data in blocks_list:
            if canDecrypt:
                result_blocks.append(get_map_object(block_head, canDecrypt))
            else:
                result_blocks.append(get_map_object(block_head, canDecrypt))
    
    print(result_blocks)
    
    sys.exit(0)


def get_map_object(block_head, canDecrypt):
    if canDecrypt:
        if block_head.state == "INITIAL":
            case_id = '00000000-0000-0000-0000-000000000000'
            evidence_id = '0'
        else:
            case_id = block_head.case_id
            evidence_id = block_head.item_id
        return {
            "case_id": case_id.encode('utf-8'),
            "evidence_id": evidence_id.encode('utf-8'),
            "state": block_head.state.encode('utf-8'),
            "timestamp": block_head.timestamp
        }
    else:
        if block_head.state == "INITIAL":
            encrypted_case_id = '00000000-0000-0000-0000-000000000000'
            encrypted_item_id = '0'
        else:
            encrypted_case_id = AES.aes_ecb_encrypt(uuid.UUID(block_head.case_id).int.to_bytes(16, 'big')).decode('utf-8') # Pad with null bytes
            encrypted_item_id = AES.aes_ecb_encrypt(int(block_head.item_id).to_bytes(8, 'big')).decode('utf-8') # Pad with null bytes
        return {
            "case_id": encrypted_case_id.encode('utf-8'),
            "evidence_id": encrypted_item_id.encode('utf-8'),
            "state": block_head.state.encode('utf-8'),
            "timestamp": block_head.timestamp
        }
