#!/usr/bin/env python3
import struct

PASSWORD_MAP = {
    "P80P": "POLICE",
    "L76L": "LAWYER",
    "A65A": "ANALYST",
    "E69E": "EXECUTIVE",
    "C67C": "CREATOR"
}

REMOVE_REASON_MAP = { "DESTROYED" ,"DISPOSED", "RELEASED" }

CASES_MAP = {}

H_FORMAT = struct.Struct('32s d 32s 32s 12s 12s 12s I')

D_FORMAT = struct.Struct('14s')

filePath = "~/Documents/BlockChain.bin"

AES_KEY = b'R0chLi4uLi4uLi4='

ITEM_ID_TO_PASSWORD_MAP = {}

class BlockHead:
    def __init__(self, prevHash, timestamp, case_id, item_id, state, creator, owner, length):
        self.prevHash = prevHash
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