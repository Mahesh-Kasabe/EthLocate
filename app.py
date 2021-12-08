import config , time , ccxt 

from flask import Flask , request, render_template

from web3 import Web3 

app = Flask(__name__)
w3 = Web3(Web3.HTTPProvider(config.INFURA_URL))

@app.route("/")
def home():
    binance = ccxt.binance()
    ethereum_price = binance.fetch_ticker('ETH/USDC')
    eth = w3.eth

    latest_blocks = []
    for block_number in range(eth.block_number, eth.block_number-10, -1):
        block = eth.get_block(block_number)
        latest_blocks.append(block)

    latest_transactions = []
    for tx in latest_blocks[-1]['transactions'][-10:]:
        transaction = eth.get_transaction(tx)
        latest_transactions.append(transaction)

    current_time = time.time()

    return render_template("index.html", 
        miners = config.MINERS,
        eth = eth,
        current_time=current_time, 
        ethereum_price=ethereum_price, 
        latest_blocks=latest_blocks, 
        latest_transactions=latest_transactions)


@app.route("/tx/<hash>")
def transaction(hash):
    tx = w3.eth.get_transaction(hash)
    value = w3.fromWei(tx.value , 'ether')
    receipt = w3.eth.get_transaction_receipt(hash)
    #ethereum_price = get_ethereum_price() 
    return render_template("transaction.html", hash=hash, tx=tx, value=value, 
        receipt=receipt)


@app.route("/address/")
def address():

    address = request.args.get('address')

    balance = w3.eth.get_balance(address)
    balance = w3.fromWei(balance, 'ether')

    return render_template("address.html", address=address, balance=balance)

@app.route("/block/<block_num>")
def block(block_num):
    block = w3.eth.get_block(int(block_num))
    return render_template("block.html", block=block)

if __name__ == '__main__':
    app.secret_key = 'secret123'
    app.run(debug=True)