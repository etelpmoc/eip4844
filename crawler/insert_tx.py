import paths
from eip4844.setting import *
from pymongo import MongoClient

if __name__ == "__main__":
    start = int(sys.argv[1])
    end   = int(sys.argv[2])
    
    assert start // 1000000 == (end-1) // 1000000 # Transaction data should be stored in the same collection

    client = MongoClient(f'mongodb://{MONGODB_USER}:{MONGODB_PASSWORD}@localhost:27017/')
    
    db = client['ethereum']
    # collection = db[f'transactions_{start//1000000 * 100}_{start // 1000000 * 100 + 100}']
    collection = db[f'transactions_1600_1700']
    
    w3 = Web3(Web3.HTTPProvider(f"""http://localhost:{PORT_NUM}"""))
    
    documents = []
    for block in range(start, end):
        txs = w3.eth.getBlock(block, full_transactions=True)['transactions']
        
        for tx in txs:
            num_bytes = int((len(tx['input'])-2)/2)
            documents.append({'block':block,
                              'tx_hash':tx['hash'].hex(),
                              'sender':tx['from'],
                              'recipient':tx['to'],
                              'tx_index':tx['transactionIndex'],
                              'calldata_size':num_bytes
                              })
        
        if block%10==0 or block == end-1:
            collection.insert_many(documents)
            documents = []
            print(block)


