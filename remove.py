import init as INIT
import CONSTANTS as CONS
import util as UTIL
import sys


def remove(item_id, password, reason):
    owner = pre_condition(item_id, password, reason)
    UTIL.change_status_and_add_block(item_id, reason, owner)
    sys.exit(0)


def check_creator_password(item_id, password):
    if item_id not in CONS.ITEM_ID_TO_PASSWORD_MAP:
        print("Error: Item ID not found")
        sys.exit(1)

    if CONS.ITEM_ID_TO_PASSWORD_MAP[item_id] != password:
        print("Error: Invalid password")
        sys.exit(1)

def pre_condition(item_id, password, reason):

    if reason not in CONS.REMOVE_REASON_MAP:
        print("Error: Invalid reason")
        sys.exit(1)

    last_block_pair_with_item_id = UTIL.get_last_block_with_item_id(item_id)

    if last_block_pair_with_item_id is None:
        print("Error: Item ID not found, CHECKOUT failed for Item ID: ", item_id)
        sys.exit(1)
    
    blockHead_with_item_id = last_block_pair_with_item_id[0]

    if blockHead_with_item_id.state != "CHECKEDIN":
        print("Error: Item ID is not in CHECKEDIN state, CHECKOUT failed for Item ID: ", item_id)
        sys.exit(1)

    UTIL.check_password(password)

    return blockHead_with_item_id.owner







    
    

