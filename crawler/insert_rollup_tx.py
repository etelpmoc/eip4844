import paths
from eip4844.setting import *
from pymongo import MongoClient

if __name__ == "__main__" :
    client = MongoClient(f'mongodb://{MONGODB_USER}:{MONGODB_PASSWORD}@localhost:27017/')
    db = client['ethereum']
    collection = db[f'transactions_rollup']

    sender_addresses = [
                "0xC1b634853Cb333D3aD8663715b08f41A3Aec47cc",
                "0x6887246668a3b87F54DeB3b94Ba47a6f63F32985",
                "0x5050F69a9786F081509234F1a7F4684b5E5b76C9",
                "0x3527439923a63F8C13CF72b8Fe80a77f6e572092",
                "0x8129b737912e17212C8693B781928f5D0303390a"
                        ]
    try:
        start_block = collection.find_one(sort=[("block", -1)])['block']+1
    except:
        start_block = 16500000
   
    print(f"Filtering rollup transactions from block #{start_block}")
    
    collection = db[f'transactions']
    # Aggregate query to filter transactions by sender address
    pipeline = [
                {"$match": {"sender": {"$in": sender_addresses},
                    "block": {"$gte": start_block}
                }}
                ]

    # Execute aggregation
    filtered_transactions = collection.aggregate(pipeline)

    # New collection to store filtered transactions
    transactions_rollup = db['transactions_rollup']

    # Batch size for inserting transactions
    batch_size = 1000

    # Insert filtered transactions into the new collection in batches
    batch = []
    for transaction in filtered_transactions:
        batch.append(transaction)
        if len(batch) == batch_size:
            transactions_rollup.insert_many(batch)
            batch = []

    # Insert any remaining transactions
    if batch:
        transactions_rollup.insert_many(batch)



