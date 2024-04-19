#!/usr/bin/env python3
import struct

PASSWORD_MAP = {
    "P80P": "BCHOC_PASSWORD_POLICE",
    "L76L": "BCHOC_PASSWORD_LAWYER",
    "A65A": "BCHOC_PASSWORD_ANALYST",
    "E69E": "BCHOC_PASSWORD_EXECUTIVE",
    "C67C": "BCHOC_PASSWORD_CREATOR"
}

H_FORMAT = struct.Struct('32s d 32s 32s 12s 12s 12s I')
D_FORMAT = struct.Struct('14s')

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