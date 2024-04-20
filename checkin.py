import init as INIT
import CONSTANTS as CONS
import util as UTIL
import sys


def checkin(item_id, password):
    pre_condition(item_id, password)
    
    UTIL.change_status_and_add_block(item_id, "CHECKEDIN")
    sys.exit(0)
    # Pre Condition Verified , Item Ready for Checkout


def pre_condition(item_id, password):
    last_block_pair_with_item_id = UTIL.get_last_block_with_item_id(item_id)

    if last_block_pair_with_item_id is None:
        print("Error: Item ID not found, CHECKOUT failed for Item ID: ", item_id)
        sys.exit(1)
    
    blockHead_with_item_id = last_block_pair_with_item_id[0]

    if blockHead_with_item_id.state != "CHECKEDOUT":
        print("Error: Item ID is not in CHECKEDIN state, CHECKOUT failed for Item ID: ", item_id)
        sys.exit(1)

    UTIL.check_password(password)



    
    

