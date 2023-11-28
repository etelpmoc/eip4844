import paths
from src.setting import *
from pymongo import MongoClient

if __name__ == "__main__":
    start = int(sys.argv[1])
    end   = int(sys.argv[2])

    client = MongoClient(f'mongodb://{MONGODB_USER}:{MONGODB_PASSWORD}@localhost:27017/')
    
    db = client['ethereum']
    collection = db['transactions']
    
    w3 = Web3(Web3.HTTPProvider(f"""http://localhost:{PORT_NUM+2}"""))
    
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
        
        collection.insert_many(documents)

        print(block)


