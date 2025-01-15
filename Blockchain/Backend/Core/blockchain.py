import sys
import time

sys.path.append("C:/Users/Ary/dev/PyBlockChain")

from Blockchain.Backend.Core.block import Block
from Blockchain.Backend.Core.blockheader import BlockHeader
from Blockchain.Backend.Util.util import hash256
from Blockchain.Backend.Core.Database.database import BlockchainDB

ZERO_HASH = '0' * 64
VERSION = 1

class Blockchain:
    def __init__(self):
        self.GenesisBlock()

    def write_on_disk(self,block):
        blockchaindb = BlockchainDB()
        blockchaindb.write(block)
    
    def fetch_last_block(self):
        blockchaindb = BlockchainDB()
        return blockchaindb.lastBlock()

    def GenesisBlock(self):
        BlockHeight = 0
        previousBlockHash = ZERO_HASH
        self.addBlock(BlockHeight, previousBlockHash)

    def addBlock(self,BlockHeight, previousBlockHash): 
        timestamp = int(time.time())
        Transaction = f"Codies Alert sent {BlockHeight} bitcoins to Joe"
        merkleRoot = hash256(Transaction.encode()).hex()  #combined hash of all the transactions
        bits = 'ffff001f'
        blockHeader = BlockHeader(VERSION,previousBlockHash,merkleRoot,timestamp,bits)
        blockHeader.mine()
        self.write_on_disk([Block(BlockHeight, 1, blockHeader.__dict__, 1 , Transaction).__dict__])

    def main(self):
        while True:
            lastBlock = self.fetch_last_block()
            BlockHeight = lastBlock['Height'] + 1
            previousBlockHash = lastBlock['BlockHeader']['BlockHash']
            self.addBlock(BlockHeight,previousBlockHash)

if __name__ == '__main__':
    blockchain = Blockchain()