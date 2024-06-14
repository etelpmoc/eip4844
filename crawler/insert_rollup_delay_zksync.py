import paths
from eip4844.setting import *
from pymongo import MongoClient
import random
from lxml import html

if __name__ == "__main__" :
    el = Web3(Web3.HTTPProvider(f"""http://localhost:{PORT_NUM}"""))
    
    client = MongoClient(f'mongodb://{MONGODB_USER}:{MONGODB_PASSWORD}@localhost:27017/')
    db = client['ethereum']
    
    rollup_name = "zksync"
    
    documents1 = []
    error_times = 0
    
    collection_l2delay = db[f'{rollup_name}_l2delay']    
    
    headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
                'Referer': 'https://explorer.zksync.io/',
                'Origin': 'https://explorer.zksync.io',
                'Accept': 'application/json',
                'Content-Type': 'application/json'
                }
    try:
        start = collection_l2delay.find_one(sort=[("batch", -1)])['batch']+1
    except:
        start = 458714 # zkSync start batch corresponding to Ethereum block 19400000
    
    print(f"{rollup_name} : from batch {start}")

    for batch in range(start, 471000):
        try:
            r = requests.get(f"https://block-explorer-api.mainnet.zksync.io/batches/{batch}",
                         headers = headers).json()
        except:
            time.sleep(68)
            r = requests.get(f"https://block-explorer-api.mainnet.zksync.io/batches/{batch}",
                         headers = headers).json()
        time.sleep(random.randint(1,2))
        
        l2_num_tx = r['l2TxCount']
        tx_hash = r['commitTxHash']
        l1_block = el.eth.getTransaction(tx_hash)['blockNumber']
        l1_timestamp = el.eth.getBlock(l1_block)['timestamp']
        prove_tx_hash = r['proveTxHash']
        execute_tx_hash = r['executeTxHash']
        start_timestamp = int(datetime.fromisoformat(r['timestamp'].replace('Z', '+00:00')).timestamp())
        
        try:
            r = requests.get(f"https://block-explorer-api.mainnet.zksync.io/transactions?l1BatchNumber={batch}&pageSize=10&page=1&toDate=2024-04-11T08%3A23%3A05.342Z"                              ,headers=headers).json()
        except:
            time.sleep(68)

            r = requests.get(f"https://block-explorer-api.mainnet.zksync.io/transactions?l1BatchNumber={batch}&pageSize=10&page=1&toDate=2024-04-11T08%3A23%3A05.342Z"                              ,headers=headers).json()
        end_timestamp = int(datetime.fromisoformat(r['items'][0]['receivedAt'].replace('Z', '+00:00')).timestamp())
        l2_num_block = end_timestamp - start_timestamp
        delay_sum = l2_num_tx*(l1_timestamp-(start_timestamp + end_timestamp)/2)
        
        documents1.append({'batch':batch,
                           'l2_num_tx':l2_num_tx,
                           'l1_block':l1_block,
                           'tx_hash':tx_hash,
                           'l1_timestamp':l1_timestamp,
                           'prove_tx_hash':prove_tx_hash,
                           'execute_tx_hash':execute_tx_hash,
                           'l2_num_block':l2_num_block,
                           'delay_sum':delay_sum})
        
        collection_l2delay.insert_many(documents1, ordered=False)
        documents1 = []

        print(batch, "complete")
        time.sleep(random.randint(2,11))




