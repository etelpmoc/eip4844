import paths
from eip4844.setting import *
from pymongo import MongoClient
import random

if __name__ == "__main__" :
    el = Web3(Web3.HTTPProvider(f"""http://localhost:{PORT_NUM}"""))
    
    client = MongoClient(f'mongodb://{MONGODB_USER}:{MONGODB_PASSWORD}@localhost:27017/')
    db = client['ethereum']
    transactions_rollup = db['transactions_rollup']
    
    sender_dict = {'optimism' : "0x6887246668a3b87F54DeB3b94Ba47a6f63F32985",
                   'base' : "0x5050F69a9786F081509234F1a7F4684b5E5b76C9",
                  }
    
    genesis_timestamp_dict = {'optimism': 1686068903, 
                              'base'    : 1686789347, 
                             }
    

    
    rollup_name = sys.argv[1]
    
    sender_address = sender_dict[rollup_name]
    genesis_time = genesis_timestamp_dict[rollup_name]
    
    documents1 = []
    documents2 = []

    error_times = 0
    
#     collection_blocks = db[f'{rollup_name}_blocks']
    collection_l2delay = db[f'{rollup_name}_l2delay']
        
    try:
        start = collection_l2delay.find_one(sort=[("l1_block", -1)])['l1_block']+1
    except:
        start = 19400000
    
    start = 19567332 
    print(f"{rollup_name} : from block {start}")
    
    for tx in transactions_rollup.find({'sender':sender_address, 'block':{'$gte':start, '$lte':19600000-1}}):
        try:
            block = tx['block']
            tx_hash = tx['tx_hash']
            try:                
                url = f"https://api.ethernow.xyz/v1/transaction/rollup/batch/{tx_hash}?p=0"
#                 url = f"https://d24ut439kqiny5.cloudfront.net/v1/transaction/rollup/batch/{tx_hash}"

                response = requests.get(url, 
                                     headers = {
                                                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
                                                'Referer': 'https://www.ethernow.xyz/',
                                                'Origin': 'https://www.ethernow.xyz',
                                                'Accept': 'application/json',
                                                'Content-Type': 'application/json'
                                                }).json()['l2Batch']
                error_times = 0
            except:
                error_times += 1
                print(tx)
                if error_times == 2:

                    break
                continue

            if isinstance(response, dict):
                if response["error"] == "failed to decode batches":
                    continue

            if response == None or len(response) == 0:
                continue
            else:
                response = response[0]

    #         if response['batchType'] == 0:
    #             batches = response['batches']

    #             l1timestamp = el.eth.getBlock(block)['timestamp']
    #             delay_sum = 0
    #             l2_num_tx = 0
    #             for batch in batches:
    #                 batchdata = batch['batch']

    #                 l2timestamp = batchdata['Timestamp']
    #                 delay = l1timestamp - l2timestamp
    #                 num_tx = len(batchdata['Txs'])
    #                 l2_num_tx += num_tx

    #                 delay_sum += delay*num_tx

    #             l2_num_block = len(batches)


            if response['batchType'] == 1:
                batches = response['batches']
                l1timestamp = el.eth.getBlock(block)['timestamp']
                delay_sum = 0
                l2_num_tx = 0
                l2_num_block = 0
                
                l2timestamp = batches[0]['batch']['relTimestamp'] + genesis_time # l2 genesis
                
                
                l2_num_block = response['blocksCount']
                l2_num_tx    = response['txsCount']
                
                delay_sum = (l1timestamp - l2timestamp - (l2_num_block-1) ) * l2_num_tx
                
                
#                 for idx, batch in enumerate(batches[0]['batch']['txs']):
#                     delay = l1timestamp - l2timestamp
#                     num_tx = len(batch)
#                     l2_num_tx += num_tx
#                     delay_sum += delay*num_tx
#                     l2timestamp += 2
#                     l2_num_block += 1
                    
#                     documents1.append({'l2_timestamp':l2timestamp,
#                                        'l2_num_tx':num_tx,
#                                        'l1_block':block,
#                                        'delay':delay})

#                 collection_blocks.insert_many(documents1)
#                 documents1 = []


            documents2.append({'l1_tx_hash':tx_hash,
                               'l1_block':block,
                               'l1_timestamp':l1timestamp,
                               'l2_num_tx':l2_num_tx,
                               'l2_num_block':l2_num_block,
                               'delay_sum':delay_sum})

            collection_l2delay.insert_many(documents2, ordered=False)
            documents2 = []

            print(block, "complete")
            time.sleep(random.randint(3,10))

        except Exception as e:
            print(tx,block)
            print(e)
            break




