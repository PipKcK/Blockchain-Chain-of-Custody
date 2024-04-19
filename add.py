#!/usr/bin/env python3

import sys
import os

from datetime import datetime

import init as INIT
import CONSTANTS as CONS
import util as UTIL

def add(case_id , item_ids, creator, password):

    for item_id in item_ids:
        add_new_block(case_id, item_id, creator, password)
    sys.exit(0)


def add_new_block(case_id , item_id, creator, password):
    pre_check(case_id, item_id, creator, password)

    if UTIL.get_last_block_with_item_id(item_id) != None:
        print("Error: Item ID already exists")
        sys.exit(1)

    # Create a New Block Head
    prevHash = b''
    timestamp = datetime.now().timestamp()
    state = b'CHECKEDIN'
    owner = b''
    length = 0
    
    block_head = CONS.BlockHead(prevHash, timestamp, case_id, item_id, state, creator, owner, length)
    block_data = CONS.BlockData(b'')
    UTIL.pack_and_write_block(block_head, block_data)


def pre_check(case_id , item_id, creator, password):
    input_validation(case_id, item_id, creator, password)
    INIT.init()
    check_password(password)


def check_password(password):
    if password not in CONS.PASSWORD_MAP:
        print("Error: Invalid password")
        sys.exit(1)





def input_validation(case_id, item_id, creator, password):
    if(case_id == None or item_id == None or creator == None or password == None):
        print("Error: Missing required arguments")
        sys.exit(1)