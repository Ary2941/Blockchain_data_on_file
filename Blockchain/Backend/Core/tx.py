
from Blockchain.Backend.Core.script import Script
from Blockchain.Backend.Util.util import bytes_needed, decode_base58, encode_variant, hash256, int_to_little_endian, little_endian_to_int

class Tx:
    def __init__(self,version, tx_ins, tx_outs, locktime):
        self.version  = version
        '''what are the transaction'''
        self.tx_ins   = tx_ins
        '''to who am i sending btc'''
        self.tx_outs  = tx_outs
        '''locktime of the transaction'''
        self.locktime = locktime

    def serialize(self):
        result = int_to_little_endian(self.version,4)
        result += encode_variant(len(self.tx_ins))
        
        for transaction in self.tx_ins:
            result += transaction.serialize() #convert all the transaction input and add concatenated value

        result += encode_variant(len(self.tx_outs))

        for transaction in self.tx_outs:
            result += transaction.serialize() #convert all the transaction output and add concatenated value

        result += int_to_little_endian(self.locktime, 4)

        return result

    def id(self):
        '''Human-readable TxId'''
        return self.hash().hex()

    def hash(self):
        '''Binary Hash of serialization '''
        return hash256(self.serialize())[::-1]


    def is_coinbase(self):
        # all coinbase transactions have exactly one input, that first input has prev_tx is b'\x00'*32 and the first input prev_index is 0xffffffff
        if len(self.tx_ins) != 1:
            return False
        first_input = self.tx_ins[0]
        
        if first_input.prev_tx != b'\x00' *32:
            return False
        
        if first_input.prev_index != 0xffffffff:
            return False
        
        return True

    def to_dict(self):
        # convert coinbase transaction to dict, prev_tx blockheight in hex
        if self.is_coinbase():
            self.tx_ins[0].prev_tx = self.tx_ins[0].prev_tx.hex()
            self.tx_ins[0].script_sig.cmds[0] = little_endian_to_int(self.tx_ins[0].script_sig.cmds[0])
            self.tx_ins[0].script_sig = self.tx_ins[0].script_sig.__dict__
        
        self.tx_ins[0] = self.tx_ins[0].__dict__
        
        self.tx_outs[0].script_pubkey.cmds[2] = self.tx_outs[0].script_pubkey.cmds[2].hex()
        self.tx_outs[0].script_pubkey = self.tx_outs[0].script_pubkey.__dict__
        self.tx_outs[0] = self.tx_outs[0].__dict__

        return self.__dict__



'''the signature proves de ownership'''
class TxIn:
    def __init__(self,prev_tx,prev_index,script_sig = None, sequence = 0xffffffff):
        self.prev_tx = prev_tx
        self.prev_index = prev_index

        if script_sig == None:
            self.script_sig = Script()
        else:
            self.script_sig = script_sig
        self.sequence = sequence 

    def serialize (self):
        result = self.prev_tx[::-1]
        result += int_to_little_endian(self.prev_index, 4)
        result += self.script_sig.serialize()
        result += int_to_little_endian(self.sequence, 4)
        return result


class TxOut:
    def __init__(self,amount,script_pubkey):
        self.amount = amount
        self.script_pubkey = script_pubkey

    def serialize(self):
        result = int_to_little_endian(self.amount, 8)
        result += self.script_pubkey.serialize()
        return result


'''transaction created by a miner
creating a new block
'''
ZERO_HASH = b'\0' * 32
REWARD = 50

PRIVATE_KEY = '76106471728427465796187510860355568160254207807680397589831754374945066693457'
MINER_ADDRESS = '1LYgXwYXw16GJXgDwHV7aCNijnQWYEdc1C'

class CoinBaseTx:
    def __init__(self,BlockHeight):
        self.BlockHeightInLittleEndian = int_to_little_endian(BlockHeight,bytes_needed(BlockHeight))

    def CoinbaseTransaction(self):
        prev_tx = ZERO_HASH
        prev_index = 0xffffffff
        tx_ins = []
        tx_outs = []

        tx_ins.append(TxIn(prev_tx,prev_index))

        tx_ins[0].script_sig.cmds.append(self.BlockHeightInLittleEndian)
        
        target_amount = REWARD*100000000
        target_h160 = decode_base58(MINER_ADDRESS)
        target_script = Script.p2pkh_script(target_h160)
        tx_outs.append(TxOut(amount=target_amount,script_pubkey=target_script))

        coinBaseTx =  Tx(1,tx_ins,tx_outs,0)
        coinBaseTx.TxId = coinBaseTx.id()

        return coinBaseTx


'''
TxId = 123
bob -> 0 send 1 btc to codeallok
       1 send 3 btc to jason
'''