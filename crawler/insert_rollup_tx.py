import paths
from eip4844.setting import *
from pymongo import MongoClient

if __name__ == "__main__" :
    client = MongoClient(f'mongodb://{MONGODB_USER}:{MONGODB_PASSWORD}@localhost:27017/')
    db = client['ethereum']
    collection = db[f'transactions_rollup']

    sender_addresses = [
                        "0xC1b634853Cb333D3aD8663715b08f41A3Aec47cc", # Arbitrum
                        "0x6887246668a3b87F54DeB3b94Ba47a6f63F32985", # Optimism
                        "0x5050F69a9786F081509234F1a7F4684b5E5b76C9", # Base
                        "0x415c8893D514F9BC5211d36eEDA4183226b84AA7", # Blast
                        "0x3527439923a63F8C13CF72b8Fe80a77f6e572092", # zkSync Era - proveBatch , commit
                        "0x0D3250c3D5FAcb74Ac15834096397a3Ef790ec99", # zkSync Era -commmitBatch
                        "0x9228624C3185FCBcf24c1c9dB76D8Bef5f5DAd64", # Linea - finalize
                        "0xa9268341831eFa4937537bc3e9EB36DbecE83C7e", # Linea - submit Blob
                        "0x8129b737912e17212C8693B781928f5D0303390a", # dYdX - updatestate, verifyFRI , registerContinuous

                        "0x99199a22125034c808ff20f377d91187E8050F2E", # Mode
                        "0xcF2898225ED05Be911D3709d9417e86E0b4Cfc8f", # Scroll - commit batch
                        "0x356483dC32B004f32Ea0Ce58F7F88879886e9074", # Scroll - finalize batch
                        "0x22A82147A80747CFb1562e0f72F6be39F18B5F76", # Starknet - verifyFRI, register
                        "0x2C169DFe5fBbA12957Bdd0Ba47d9CEDbFE260CA7" # Starknet - updatestate KZGDA?
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



