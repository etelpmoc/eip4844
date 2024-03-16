import paths
from eip4844.setting import *
from pymongo import MongoClient

if __name__ == "__main__":
    
    client = MongoClient(f'mongodb://{MONGODB_USER}:{MONGODB_PASSWORD}@localhost:27017/')
    db = client['ethereum']
    transactions = db[f'transactions']
    blocks = db['blocks']
    
    w3 = Web3(Web3.HTTPProvider(f"""http://localhost:{PORT_NUM}"""))
    
    start = transactions.find_one(sort=[("block", -1)])['block']+1
    end = blocks.find_one(sort=[("block", -1)])['block']+1
    
    print(f"Starting updates from Block #{start} to #{end}")

    documents = []
    for block in range(start, end):
        txs = w3.eth.getBlock(block, full_transactions=True)['transactions']
        
        for tx in txs:
            tx_hash = tx['hash'].hex()
            receipt = w3.eth.getTransactionReceipt(tx_hash)

            num_bytes = int((len(tx['input'])-2)/2)
            documents.append({'block':block,
                              'tx_hash':tx_hash,
                              'sender':tx['from'],
                              'recipient':tx['to'],
                              'tx_index':tx['transactionIndex'],
                              'calldata_size':num_bytes,
                              'gas_used':receipt['gasUsed'],
                              'effective_gas_price':receipt['effectiveGasPrice']
                              })
        
        if block%10==0 or block == end-1:
            transactions.insert_many(documents)
            documents = []
            print(block)


