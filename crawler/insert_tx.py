import paths
from eip4844.setting import *
from pymongo import MongoClient

if __name__ == "__main__":
    
    client = MongoClient(f'mongodb://{MONGODB_USER}:{MONGODB_PASSWORD}@localhost:27017/')
    db = client['ethereum']
    collection = db[f'transactions']
    
    w3 = Web3(Web3.HTTPProvider(f"""http://localhost:{PORT_NUM}"""))
    
    start = collection.find_one(sort=[("block", -1)])['block']+1
    end = w3.eth.block_number
    
    print(f"Starting updates from Slot #{start} to #{end}")

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


