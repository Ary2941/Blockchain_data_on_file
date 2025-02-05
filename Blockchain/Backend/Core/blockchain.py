import sys, time
from multiprocessing import Process, Manager #our frontend will be in a second process

sys.path.append("C:/Users/Ary/dev/PyBlockChain")

from Blockchain.Backend.Core.EllepticCurve.op import OP_CODE_FUNCTION
from Blockchain.Backend.Core.tx import CoinBaseTx

from Blockchain.Backend.Core.block import Block
from Blockchain.Backend.Core.blockheader import BlockHeader
from Blockchain.Backend.Util.util import hash256
from Blockchain.Backend.Core.Database.database import BlockchainDB

from Blockchain.Frontend.run import main



ZERO_HASH = b'\0' * 32
VERSION = 1

class Blockchain:
    def __init__(self,utxos, MemPool):
        self.utxos = utxos
        self.MemPool = MemPool

    def store_utxos_in_cache(self):
        for transaction in self.addTransactionsInBlock:
            print(f'Transaction {transaction.TxId} added to UTXOS')
            self.utxos[transaction.TxId] = transaction

    def remove_spent_transactions(self):
        for txId_index in self.removeSpentTransactions:
            '''if previous transaction in self.utxos'''

            if txId_index[0].hex() in self.utxos:

                if len(self.utxos[txId_index[0].hex()].tx_outs) < 2:
                    print(f'Spent Transaction {txId_index[0].hex()} removed from UTXOS')
                    del self.utxos[txId_index[0].hex()]
                else:
                    prev_trans = self.utxos[txId_index[0].hex()]
                    self.utxos[txId_index [0].hex()] = prev_trans.tx_outs.pop(txId_index[1])


    ''' read Transactions from memory pool'''
    def read_transaction_from_memorypool(self):
        self.TxIds = []
        self.addTransactionsInBlock = []
        self.removeSpentTransactions = []

        for tx in self.MemPool:
            self.TxIds.append(tx)
            self.addTransactionsInBlock.append(self.MemPool[tx])

            for spent in self.MemPool[tx].tx_ins:
                self.removeSpentTransactions.append([spent.prev_tx, spent.prev_index]) # we will remove based on this

    def remove_transaction_from_memorypool(self):
        for tx in self.TxIds:
            if tx in self.MemPool:
                del self.MemPool[tx]

    def write_on_disk(self,block):
        blockchaindb = BlockchainDB()
        #print(f"block{block}")
        blockchaindb.write(block)
    
    def fetch_last_block(self):
        blockchaindb = BlockchainDB()
        return blockchaindb.lastBlock()

    def GenesisBlock(self):
        BlockHeight = 0
        previousBlockHash = ZERO_HASH
        self.addBlock(BlockHeight, previousBlockHash)
    
    def convert_to_JSON(self):
        self.TxJson = []
        for tx in self.addTransactionsInBlock:
            self.TxJson.append(tx.to_dict())

    def addBlock(self,BlockHeight, previousBlockHash): 
        self.read_transaction_from_memorypool()
        timestamp = int(time.time())
        #Transaction = f"Codies Alert sent {BlockHeight} bitcoins to Joe"
        cbInstance = CoinBaseTx(BlockHeight)
        '''Tx = transaction'''

        Tx = cbInstance.CoinbaseTransaction()

        self.TxIds.insert(0, Tx.TxId)
        self.addTransactionsInBlock.insert(0, Tx)

        merkleRoot = Tx.TxId  #combined hash of all the transactions
        bits = 'ffff001f'
        blockHeader = BlockHeader(VERSION,previousBlockHash,merkleRoot,timestamp,bits)
        blockHeader.mine()
        self.remove_spent_transactions()
        self.remove_transaction_from_memorypool()
        self.store_utxos_in_cache()
        self.convert_to_JSON()
        print(f"\nBlock {BlockHeight} mined succesfully with Nonce value of {blockHeader.nonce}")
        for transactionJson in self.TxJson:
            print(f"    Transaction {transactionJson["TxId"]}")
        print('\n')
        self.write_on_disk([Block(BlockHeight, 1, blockHeader.__dict__, 1 , self.TxJson).__dict__])


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

    def evaluate(self, z):
        cmds = self.cmds[:]
        stack = []

        while len(cmds) > 0:
            cmd = cmds.pop(0)

            if type(cmd) == int:
                operation = OP_CODE_FUNCTION[cmd]

                if cmd == 172 or cmd == 136:  # Handle both signature verification commands
                    if not operation(stack, z):
                        print(f"Error in Signature Verification with command {cmd} and stack {stack}")
                        return False

                elif not operation(stack):
                    print(f"Error in Signature Verification with command {cmd} and stack {stack}")
                    return False
            else:
                stack.append(cmd)
        return True

if __name__ == '__main__':
    with Manager() as manager:
        utxos = manager.dict()
        MemPool = manager.dict()


        webapp = Process(target=main, args=(utxos,MemPool))

        webapp.start()

        blockchain = Blockchain(utxos, MemPool)
        blockchain.main()

