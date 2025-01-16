
from Blockchain.Backend.Core.script import Script

class Tx:
    def __init__(self,version, tx_ins, tx_outs, locktime):
        self.version  = version
        '''what are the transaction'''
        self.tx_ins   = tx_ins
        '''to who am i sending btc'''
        self.tx_outs  = tx_outs
        '''locktime of the transaction'''
        self.locktime = locktime 


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

class TxOut:
    def __init__(self,amount,script_pubkey):
        self.amount = amount
        self.script_pubkey = script_pubkey


'''
TxId = 123
bob -> 0 send 1 btc to codeallok
       1 send 3 btc to jason
'''