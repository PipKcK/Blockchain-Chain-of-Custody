
import util as UTIL
import CONSTANTS as CONS

import sys
import hashlib

def verify():
    blocks_list = UTIL.unpack_all_blockHead_blockData()
    unique_item_ids = {}
    for block_head, block_data in blocks_list:
        unique_item_ids[block_head.item_id] = block_head , block_data
    
    for item_id in unique_item_ids:
        check_item_id(item_id)
    
    sys.exit(0)

def check_item_id(item_id):
    item_id_block_list = UTIL.get_block_list_for_item_id(item_id)
    prev = None

    for curr, block_data in item_id_block_list:

        if curr.state == "CHECKEDIN" and prev is not None and prev.state != "CHECKEDOUT":
            print("State of Block Chain : ERROR !")
            print_error_and_exit(curr , block_data)
            print("Error: Item ID is not in CHECKEDIN state, CHECKOUT failed for Item ID: ", item_id)
            sys.exit(1)

        elif curr.state == "CHECKEDOUT" and prev.state != "CHECKEDIN":
            print("State of Block Chain : ERROR !")
            print_error_and_exit(curr , block_data)
            print("Error: Item ID is not in CHECKEDOUT state, CHECKOUT failed for Item ID: ", item_id)
            sys.exit(1)
        
        elif curr.state in CONS.STATE_MAP and prev.state != "CHECKEDIN":
            print("State of Block Chain : ERROR !")
            print_error_and_exit(curr , block_data)
            print("Error: Invalid Remove Block, Prev Block Not Checked In")
            sys.exit(1)

def print_error_and_exit(block_head , block_data):
    packed_error_block_head , packed_error_block_data = UTIL.pack_block(block_head, block_data)
    bad_block_hash = hashlib.sha256(packed_error_block_head + packed_error_block_data).hexdigest()
    print("Bad Block : ", bad_block_hash)

