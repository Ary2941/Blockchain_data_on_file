import sys, time
from multiprocessing import Process, Manager #our frontend will be in a second process

sys.path.append("C:/Users/Ary/dev/PyBlockChain")

from Blockchain.Backend.Core.EllepticCurve.op import OP_CODE_FUNCTION
from Blockchain.Backend.Core.tx import CoinBaseTx

from Blockchain.Backend.Core.block import Block
from Blockchain.Backend.Core.blockheader import BlockHeader
from Blockchain.Backend.Util.util import hash256, merkle_root
from Blockchain.Backend.Core.Database.database import BlockchainDB

from Blockchain.Frontend.run import main



ZERO_HASH = b'\0' * 32
VERSION = 1



class Blockchain:
    def __init__(self,utxos, MemPool):
        self.utxos = utxos
        self.MemPool = MemPool

    ''' quick retrieval in memorty'''
    def store_utxos_in_cache(self):
        for transaction in self.addTransactionsInBlock:
            print(f"transaction {transaction} aded")
            self.utxos[transaction.TxId] = transaction
        
    def remove_spent_Transactions(self):
        for TxId_index in self.remove_spent_transactions:
            if TxId_index[0].hex() in self.utxos:
                if len(self.utxos[TxId_index[0].hex()].tx_outs) < 2:
                    print(f"transaction{TxId_index[0].hex()} removed from UTXO")
                    
                    del self.utxos[TxId_index[0].hex()]
                else:
                    prev_trans = self.utxos[TxId_index[0].hex()]
                    self.utxos[TxId_index[0].hex()] = prev_trans.tx_outs.pop(TxIn_index[1])
    
    ''' read Transactions from memory pool'''
    def read_transaction_from_memorypool(self):
        self.TxIds = []
        self.addTransactionsInBlock = []
        self.remove_spent_transactions = []

        for tx in self.MemPool:
            self.TxIds.append(bytes.fromhex(tx))
            self.addTransactionsInBlock.append(self.MemPool[tx])
            
            for spent in self.MemPool[tx].tx_ins:
                self.remove_spent_transactions.append([spent.prev_tx, spent.prev_index])

    def remove_transactions_from_memorypool(self):
        for tx in self.TxIds:
            if tx.hex() in self.MemPool:
                del self.MemPool[tx.hex()]

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

    def calculate_fee(self):
        self.input_amount = 0
        self.output_amount = 0

        '''input amount'''
        for txId_index in self.remove_spent_transactions:
            if txId_index[0].hex() in self.utxos:
                self.input_amount += self.utxos[txId_index[0].hex()].tx_outs[txId_index[1]].amount

        for tx in self.addTransactionsInBlock:
            for tx_out in tx.tx_outs:
                self.output_amount += tx_out.amount

        self.fee = self.input_amount - self.output_amount
    


    def addBlock(self,BlockHeight, previousBlockHash): 
        self.read_transaction_from_memorypool()
        self.calculate_fee()
        
        timestamp = int(time.time())

        cbInstance = CoinBaseTx(BlockHeight)
        '''Tx = transaction'''

        Tx = cbInstance.CoinbaseTransaction()
        
        Tx.tx_outs[0].amount += self.fee #update fee

        self.TxIds.insert(0, bytes.fromhex(Tx.id()) )
        self.addTransactionsInBlock.insert(0, Tx)

        merkleRoot = merkle_root(self.TxIds)[::-1].hex()  #combined hash of all the transactions
        bits = 'ffff001f'
        blockHeader = BlockHeader(VERSION,previousBlockHash,merkleRoot,timestamp,bits)
        blockHeader.mine()
        self.remove_spent_Transactions()
        self.read_transaction_from_memorypool()
        self.store_utxos_in_cache()
        self.convert_to_JSON()
        print(f"Block {BlockHeight} mined succesfully with Nonce value of {blockHeader.nonce}")

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

