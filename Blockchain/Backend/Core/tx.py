
from Blockchain.Backend.Core.script import Script
from Blockchain.Backend.Util.util import bytes_needed, decode_base58, encode_varint, hash256, int_to_little_endian, little_endian_to_int

class Tx:
    def __init__(self,version, tx_ins, tx_outs, locktime):
        self.TxId = None

        self.version  = version
        '''what are the transaction'''
        self.tx_ins   = tx_ins
        '''to who am i sending btc'''
        self.tx_outs  = tx_outs
        '''locktime of the transaction'''
        self.locktime = locktime
    
    def __repr__(self):
        return f"Tx {self.TxId}"

    def serialize(self):
        result = int_to_little_endian(self.version, 4)
        result += encode_varint(len(self.tx_ins))

        for tx_in in self.tx_ins:
            result += tx_in.serialize()

        result += encode_varint(len(self.tx_outs))

        for tx_out in self.tx_outs:
            result += tx_out.serialize()

        result += int_to_little_endian(self.locktime, 4)
        return result
  
    '''Generating signature hash'''
    def sigh_hash(self, input_index, script_pubkey):
        '''byte representation of version'''
        s = int_to_little_endian(self.version, 4)
        '''byte representation of number of inputs'''
        s += encode_varint(len(self.tx_ins))
        '''every input in the transaction is appended to the byte representation'''
        for i, tx_in in enumerate(self.tx_ins):
            if i == input_index:
                s += TxIn(tx_in.prev_tx, tx_in.prev_index, script_pubkey).serialize()
            else:
                s += TxIn(tx_in.prev_tx, tx_in.prev_index).serialize()

        s += encode_varint(len(self.tx_outs))

        for tx_out in self.tx_outs:
            s += tx_out.serialize()

        s += int_to_little_endian(self.locktime, 4)
        s += int_to_little_endian(SIGHASH_ALL, 4)
        h256 = hash256(s)
        print(f"debug {h256}")
        return int.from_bytes(h256, "big")
       
    def sign_input(self, input_index, private_key, script_pubkey):
        '''z is the signature hash'''
        z = self.sigh_hash(input_index, script_pubkey)
        der = private_key.sign(z).der()
        sig = der + SIGHASH_ALL.to_bytes(1, "big")
        sec = private_key.point.sec()
        self.tx_ins[input_index].script_sig = Script([sig, sec])

    def verify_input(self, input_index, script_pubkey):
        tx_in = self.tx_ins[input_index]
        z = self.sigh_hash(input_index,script_pubkey)
        '''
            em combined temos a transaction id em 0
            temos  a assinatura em 1
            tempos a chave esperada em 4
        '''
        combined = tx_in.script_sig + script_pubkey
        return combined.evaluate(z) #z is the main part to verify the transaction
    #
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
    def __init__(self,prev_tx,prev_index,script_sig = None, sequence = 0xFFFFFFFF):
        self.prev_tx = prev_tx
        self.prev_index = prev_index

        if script_sig == None:
            self.script_sig = Script()
        else:
            self.script_sig = script_sig
        self.sequence = sequence
    
    def __repr__(self):
        return f"{self.prev_tx}:{self.prev_index}"

    def serialize (self):
        result = self.prev_tx[::-1]
        result += int_to_little_endian(self.prev_index, 4)
        result += self.script_sig.serialize()
        #
        result += int_to_little_endian(self.sequence, 4)
        #
        print(f"Serialized TxIn {result}")
        return result


class TxOut:
    def __init__(self,amount,script_pubkey):
        self.amount = amount
        self.script_pubkey = script_pubkey
    
    def __repr__(self):
        return f"{self.amount}:{self.script_pubkey}"

    def serialize(self):
        result = int_to_little_endian(self.amount, 8)
        result += self.script_pubkey.serialize()
        print(f"Serialized TxOut {result}")
        return result


'''transaction created by a miner
creating a new block
'''
ZERO_HASH = b'\0' * 32
REWARD = 50

PRIVATE_KEY = '17120605802709174992541332032003431152280600713281778263040132838812085114730'
MINER_ADDRESS = '1D7BUEj3ogWEkZXVsaqbLMZ3yg9jqdXt8S'
SIGHASH_ALL = 1

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

        coinBaseTx = Tx(1,tx_ins,tx_outs,0)
        coinBaseTx.TxId = coinBaseTx.id()

        return coinBaseTx


'''
TxId = 123
bob -> 0 send 1 btc to codeallok
       1 send 3 btc to jason
'''