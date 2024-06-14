import paths
from eip4844.setting import *
from pymongo import MongoClient, UpdateOne
import time

if __name__ == "__main__":
    w3 = Web3(Web3.HTTPProvider(f"""http://localhost:{PORT_NUM}"""))

    client = MongoClient(f'mongodb://{MONGODB_USER}:{MONGODB_PASSWORD}@localhost:27017/')
    
    db = client['ethereum']
    collection = db[f'transactions']
    
#     start = collection.find_one({"gas_used": {"$exists": True}}, sort=[("block", -1)])['block']+1
    start = collection.find_one(sort=[("block", 1)])['block']

    end = collection.find_one(sort=[("block", -1)])['block']
    #16000000 ~ 16062400 updated    
    print(f"Starting updates from Block #{start} to #{end}")
    
    batch = 100
    for block in range(start,end, batch):
        block_start = block
        block_end = block + batch

        if (end-block) // batch == 0:
            block_end = end
                
        query = {
                 'block': {'$gte': block_start, '$lte': block_end}
                }
        t1 = time.time()

        documents = collection.find(query)
        t2 = time.time()

        update_operations = []
        for doc in documents:
            tx = w3.eth.getTransaction(doc['tx_hash'])
            if tx['type'] == '0x0' or tx['type'] == '0x1':
                maxFeePerGas = tx['gasPrice']
                maxPriorityFeePerGas = tx['gasPrice']
            else:
                maxFeePerGas = tx['maxFeePerGas']
                maxPriorityFeePerGas = tx['maxPriorityFeePerGas']
                
            update_op = UpdateOne({'_id' : doc['_id']}, {'$set' : {'max_fee_per_gas' : maxFeePerGas, 'max_priority_fee_per_gas' : maxPriorityFeePerGas}})
            update_operations.append(update_op)
            
#             receipt = w3.eth.getTransactionReceipt(doc['tx_hash'])
#             update_op = UpdateOne({'_id' : doc['_id']}, {'$set' : {'gas_used' : receipt['gasUsed'], 'effective_gas_price' : receipt['effectiveGasPrice']}})
#             update_operations.append(update_op)
        t3 = time.time()

        result = collection.bulk_write(update_operations)
        
        t4 = time.time()
        print(f"""Load time : {t2-t1} \n Receipt : {t3-t2}, Write : {t4-t3}""")
        print(f"""{block_start} ~ {block_end} updated""")
