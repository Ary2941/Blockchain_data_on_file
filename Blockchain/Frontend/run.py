from flask import Flask, render_template, request
from Blockchain.Backend.Core.tx import Tx
from Blockchain.Client.SendBTC import SendBTC

app = Flask(__name__)

@app.route('/',methods = ["GET","POST"])
def wallet():
    message = ''
    if request.method == "POST":
        FromAddress = request.form.get("fromAddress")
        toAddress = request.form.get("toAddress")
        amount = request.form.get("amount", type=int)
        sendCoin = SendBTC(FromAddress, toAddress, amount, UTXOS)
        txObject = sendCoin.prepareTransaction()
        scriptPubkey = sendCoin.scriptPublicKey(FromAddress)
        print("f PUBLIC KEY {scriptPubkey}")

        verified = True
        
        if not txObject:
            message = "Transação inválida"

        if isinstance(txObject, Tx):
            for index, tx in enumerate(txObject.tx_ins):
                print(f'DEBUG: index {index}')
                if not txObject.verify_input(index,scriptPubkey):
                    verified = False
                if verified:
                    MEMPOOL[txObject.TxId] = txObject
                    message = f"Transaction {txObject} added in memory Pool"

    return render_template('wallet.html', message = message)


def main(utxos,MemPool):
    global UTXOS
    global MEMPOOL
    UTXOS = utxos
    MEMPOOL = MemPool #add transactions to MemPool
    app.run()