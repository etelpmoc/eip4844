import paths
from eip4844.setting import *
from pymongo import MongoClient
import random
from lxml import html

if __name__ == "__main__" :
    el = Web3(Web3.HTTPProvider(f"""http://localhost:{PORT_NUM}"""))
    
    client = MongoClient(f'mongodb://{MONGODB_USER}:{MONGODB_PASSWORD}@localhost:27017/')
    db = client['ethereum']
    
    rollup_name = "starknet"
    
    documents1 = []
    error_times = 0
    
    collection_tx = db[f'{rollup_name}_tx']
    collection_l2delay = db[f'{rollup_name}_l2delay']    
    
    headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
                }
    
    
    max_l2_block = collection_l2delay.find_one(sort=[("l2_block", -1)])['l2_block']
     
    print(f"{rollup_name} start from {max_l2_block}")
    blocknum_set = set()
    for i in range(1,300):
        l2_blocks = requests.get(f"https://voyager.online/api/blocks?ps=100&p={i}").json()['items']
        documents1, documents2 = [], []
        for block in l2_blocks:
            l2_block = block['number']
            
            if l2_block in blocknum_set or l2_block <= max_l2_block:
                print(l2_block, max_l2_block)
                continue

            l2_timestamp = block['timestamp']
            l2_num_tx = block['txnCount']
            l1_tx_hash = block['l1VerificationTxHash']

            if not l1_tx_hash:
                continue

            blocknum_set.add(l2_block)

            l1_block = el.eth.getTransaction(l1_tx_hash)['blockNumber']
            l1_timestamp = el.eth.getBlock(l1_block)['timestamp']

            delay_sum = (l1_timestamp - l2_timestamp)*l2_num_tx

            documents1.append({'l2_block': l2_block,
                               'l2_timestamp': l2_timestamp,
                               'l2_num_tx': l2_num_tx,
                               'l1_block': l1_block,
                               'delay': l1_timestamp - l2_timestamp})
            documents2.append({'tx_hash': l1_tx_hash,
                               'l1_block': l1_block,
                               'l1_timestamp': l1_timestamp,
                               'l2_block': l2_block,
                               'l2_timestamp': l2_timestamp,
                               'l2_num_tx': l2_num_tx,
                               'delay_sum': delay_sum})
        
        if not documents2:
            print(f"Skipping page {i}")
            continue
        
        collection_tx.insert_many(documents1, ordered=False)
        collection_l2delay.insert_many(documents2, ordered=False)
        documents1, documents2 = [], []
        
        print(f"Page {i} ended")
        time.sleep(random.randint(6,25))




