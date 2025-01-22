from flask import Flask, render_template, request
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

        if not (sendCoin.prepareTransaction()):
            message = "Insufficient values"

    return render_template('wallet.html', message = message)


def main(utxos):
    global UTXOS
    UTXOS = utxos
    app.run()