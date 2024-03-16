import paths
from eip4844.setting import *
from pymongo import MongoClient

if __name__ == "__main__":
    
    client = MongoClient(f'mongodb://{MONGODB_USER}:{MONGODB_PASSWORD}@localhost:27017/')
    db = client['ethereum']
    blob_transactions = db[f'blob_transactions']
    slots = db['slots']
    blocks = db['blocks']
    
    w3 = Web3(Web3.HTTPProvider(f"""http://localhost:{PORT_NUM}"""))

    try:
        start = blob_transactions.find_one(sort=[("block", -1)])['block']+1
    except:
        start = 19426587 # Dencun start
    
    end = blocks.find_one(sort=[("block", -1)])['block']+1

    print(f"Starting updates from Block #{start} to #{end}")

    documents = []
    for block in range(start, end):
        txs = w3.eth.getBlock(block, full_transactions=True)['transactions']

        for tx in txs:
            if tx['type'] != '0x3': # Filter out blob trasnactions
                continue

            num_bytes = int((len(tx['input'])-2)/2)
            
            try:
                slot = slots.find_one({"block": block})['slot'] # Find corresponding slot number in slots table
            except:
                print("cannot find slot at block #", block)
                continue
            
            documents.append({'block':block,
                              'tx_hash':tx['hash'].hex(),
                              'sender':tx['from'],
                              'recipient':tx['to'],
                              'tx_index':tx['transactionIndex'],
                              'calldata_size':num_bytes,
                              'blobVersionedHashes' : tx['blobVersionedHashes'],
                              'slot':slot
                              })

        if block%100==0 or block == end-1:
            if documents:
                blob_transactions.insert_many(documents)
                documents = []
                print(block)


