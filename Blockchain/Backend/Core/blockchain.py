import sys
import time
sys.path.append("C:/Users/Ary/dev/PyBlockChain")

from Blockchain.Backend.Core.tx import CoinBaseTx


from Blockchain.Backend.Core.block import Block
from Blockchain.Backend.Core.blockheader import BlockHeader
from Blockchain.Backend.Util.util import hash256
from Blockchain.Backend.Core.Database.database import BlockchainDB

ZERO_HASH = b'\0' * 32
VERSION = 1

class Blockchain:
    def __init__(self):
        pass

    def write_on_disk(self,block):
        blockchaindb = BlockchainDB()
        print(f"block{block}")
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
        #Transaction = f"Codies Alert sent {BlockHeight} bitcoins to Joe"
        cbInstance = CoinBaseTx(BlockHeight)
        '''Tx = transaction'''

        Tx = cbInstance.CoinbaseTransaction()
        merkleRoot = Tx.TxId  #combined hash of all the transactions
        bits = 'ffff001f'
        blockHeader = BlockHeader(VERSION,previousBlockHash,merkleRoot,timestamp,bits)
        blockHeader.mine()
        print(f"Block {BlockHeight} mined succesfully with Nonce value of {blockHeader.nonce}")

        self.write_on_disk([Block(BlockHeight, 1, blockHeader.__dict__, 1 , Tx.to_dict()).__dict__])

    def main(self):
        lastBlock = self.fetch_last_block()
        print(f"lastBlock {lastBlock}")
        if lastBlock is None:
            self.GenesisBlock()


        while True:
            lastBlock = self.fetch_last_block()
            BlockHeight = lastBlock['Height'] + 1
            previousBlockHash = lastBlock['BlockHeader']['BlockHash']
            self.addBlock(BlockHeight,previousBlockHash)

if __name__ == '__main__':
    blockchain = Blockchain()
    blockchain.main()