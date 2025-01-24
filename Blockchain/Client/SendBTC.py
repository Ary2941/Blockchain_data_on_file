''' Smart contract '''

import time
from Blockchain.Backend.Core.Database.database import AccountDB
from Blockchain.Backend.Core.EllepticCurve.EllepticCurve import PrivateKey
from Blockchain.Backend.Core.script import Script
from Blockchain.Backend.Core.tx import Tx, TxIn, TxOut
from Blockchain.Backend.Util.util import decode_base58, hash160


class SendBTC:
    def __init__(self,fromAccount,toAccount,Amount,UTXOS):
        self.COIN = 100000000
        self.fromPublicAddress = fromAccount
        self.toAccount = toAccount
        self.Amount = Amount * self.COIN
        self.utxos = UTXOS

    def scriptPublicKey(self,PublicAddress):
        h160 = decode_base58(PublicAddress)
        script_pubKey = Script().p2pkh_script(h160)
        return script_pubKey

    def getPrivateKey(self):
        ACC = AccountDB()
        AllAccounts = ACC.read()
        for account in AllAccounts:
            if account['PublicAddress'] == self.fromPublicAddress:
                return account['privateKey']

    def prepareTxIn(self):
        TxIns = []
        self.Total = 0

        """Convert Public Address into Public Hash to find tx_outs that are locked to this hash"""
        print(f"DEBUG! {self.fromPublicAddress}")
        self.From_address_script_pubkey = self.scriptPublicKey(self.fromPublicAddress)
        self.fromPubKeyHash = self.From_address_script_pubkey.cmds[2]

        newutxos = {}

        try:
            while len(newutxos) < 1:
                newutxos = dict(self.utxos)
                time.sleep(2)
        except Exception as e:
            print(f"Error in converting the Managed Dict to Normal Dict")

        for Txbyte in newutxos:
            if self.Total < self.Amount:
                TxObj = newutxos[Txbyte]

                for index, txout in enumerate(TxObj.tx_outs):
                    if txout.script_pubkey.cmds[2] == self.fromPubKeyHash:
                        self.Total += txout.amount
                        prev_tx = bytes.fromhex(TxObj.id())
                        TxIns.append(TxIn(prev_tx, index))
            else:
                break
        self.isBalanceEnough = True
        if self.Total < self.Amount:
            self.isBalanceEnough = False

        return TxIns
        
    def prepareTxOut(self):
        TxOuts = []
        to_scriptPubKey = self.scriptPublicKey(self.toAccount)
        TxOuts.append(TxOut(self.Amount,to_scriptPubKey))

        '''Calculating fee
        
        
        total >> 1000 BTC
        amount >> gonna send 900
        fee >> service tax to the miner
        change >> gonna go back to me 
        
        '''
        self.fee = self.COIN
        self.changeAmount = self.Total - self.Amount - self.fee

        TxOuts.append(TxOut(self.changeAmount,self.From_address_script_pubkey)) #piking my change
        return TxOuts

    def signTx(self):
        secret = self.getPrivateKey()
        priv = PrivateKey(secret=secret)

        for index, input in enumerate(self.TxIns):
            self.TxObject.sign_input(index, priv, self.From_address_script_pubkey)

        #return True 

    def prepareTransaction(self):
        self.TxIns = self.prepareTxIn()
        if self.isBalanceEnough:
            self.TxOuts = self.prepareTxOut()
            self.TxObject = Tx(1,self.TxIns,self.TxOuts,0)
            self.TxObject.TxId = self.TxObject.id()
            self.signTx()
            return self.TxObject
        return self.isBalanceEnough
