import pickle
import os
import hashlib
import maya



#TODO Check if the block variables match the specifications met in the document
    #TODO Had issues with time in float. It shows 24 Bytes.
    #TODO Had issues with data length. It shows 28 Bytes.

#TODO Change genesis values
#TODO Add functionality from time_stamp.py to this file
#TODO Add owner? (It is not being used but the document specifies it)
#TODO Add additional details. Refer to Page 4/15 in the document.

class Block:
    def __init__(self, previous_hash, timestamp, case_id, item_ids, state, creator, data_length, data, password, nonce, hash):
        self.previous_hash = previous_hash
        self.timestamp = timestamp
        self.case_id = case_id
        self.item_ids = item_ids
        self.state = state
        self.creator = creator
        self.data_length = data_length
        self.data = data
        self.password = password
        self.nonce = nonce
        self.hash = hash

class Blockchain:
    def __init__(self):
        self.file_path = os.environ.get('BCHOC_FILE_PATH', 'blockchain.pkl')
        if os.path.exists(self.file_path):
            with open(self.file_path, 'rb') as input:
                self.blockchain = pickle.load(input)
        else:
            nonce = str(int.from_bytes(os.urandom(32), byteorder='big'))
            data = "Initial block"
            data_length = len(data)
            genhash = self.calculate_hash(None, self.get_utc_timestamp(), None, None, "INITIAL", None, data_length, data, "Genesis Password", nonce)
            self.genesis_block = Block(None, self.get_utc_timestamp(), None, None, "INITIAL", None, data_length, data, "Genesis Password", nonce, genhash)
            self.blockchain = [self.genesis_block]

    def get_utc_timestamp(self):
        utc_now = maya.now().datetime()
        return float(utc_now.timestamp())

    def timestamp_to_aztime(self, epoch, tz="US/Arizona"):
        #epoch = float(epoch)
        mayadt = maya.MayaDT(epoch)
        dt = mayadt.datetime(to_timezone=tz)
        return f'{dt.strftime("%Y-%m-%d %H:%M:%S")} ({dt.tzname()})'

    def calculate_hash(self, previous_hash, timestamp, case_id, item_ids, state, creator, data_length, data, password, nonce):
        value = str(previous_hash) + str(timestamp) + str(case_id) + ''.join(item_ids) + str(state) + str(creator) + str(data_length) + str(data) + str(password) + str(nonce)
        return hashlib.sha256(value.encode('utf-8')).digest()

    def add_block(self, case_id, item_ids, state, creator, data, password):
        nonce = str(int.from_bytes(os.urandom(32), byteorder='big'))
        timestamp = self.get_utc_timestamp()
        data_length = len(data)
        hash = self.calculate_hash(self.blockchain[-1].hash, timestamp, case_id, item_ids, state.upper(), creator, data_length, data, password, nonce)
        block = Block(self.blockchain[-1].hash, timestamp, case_id, item_ids, state.upper(), creator, data_length, data, password, nonce, hash)
        self.blockchain.append(block)

        with open(self.file_path, 'wb') as output:
            pickle.dump(self.blockchain, output, pickle.HIGHEST_PROTOCOL)

    def print_blockchain(self):
        i = 0
        for block in self.blockchain:
            print("Block", i)
            print("Previous Hash:", block.previous_hash)
            print("Timestamp:", self.timestamp_to_aztime(block.timestamp))
            print("Case ID:", block.case_id)
            print("Item IDs:", block.item_ids)
            print("State:", block.state)
            print("Creator:", block.creator)
            print("Data Length:", block.data_length)
            print("Data:", block.data)
            print("Password:", block.password)
            print("Nonce:", block.nonce)
            print("Hash:", block.hash)
            i += 1
            print("--------------------")

'''
def main():
    blockchain = Blockchain()
    case_id = input("Enter case ID: ")
    item_ids = input("Enter item IDs (comma separated): ").split(',')
    state = input("Enter state: ")
    creator = input("Enter creator: ")
    data = input("Enter data: ")
    password = input("Enter password: ")
    print("--------------------")
    blockchain.add_block(case_id, item_ids, state, creator, data, password)
    blockchain.print_blockchain()

if __name__ == "__main__":
    main()
'''