import paths
from eip4844.setting import *
from pymongo import MongoClient
import random
from lxml import html

def get_timestamp(block):
    html_content = requests.get(f"https://arbiscan.io/block/{block}", headers = {
                                                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
                                                'Referer': 'https://arbiscan.io/',
                                                }).text

    tree = html.fromstring(html_content)

    timestamp_elements = tree.xpath('normalize-space(//div[text()="Timestamp:"]/following-sibling::div)')

    timestamp_string = timestamp_elements.strip()

    timestamp_start_index = timestamp_string.find("(") + 1
    timestamp_end_index = timestamp_string.find("+")
    timestamp = timestamp_string[timestamp_start_index:timestamp_end_index].strip()

    timestamp_datetime = datetime.strptime(timestamp, "%b-%d-%Y %I:%M:%S %p")
    timestamp_number = int(timestamp_datetime.timestamp())+32400 # UTC+9
    return timestamp_number


if __name__ == "__main__" :
    el = Web3(Web3.HTTPProvider(f"""http://localhost:{PORT_NUM}"""))
    
    client = MongoClient(f'mongodb://{MONGODB_USER}:{MONGODB_PASSWORD}@localhost:27017/')
    db = client['ethereum']
    transactions_rollup = db['transactions_rollup']
    
    sender_dict = {'arbitrum' : "0xC1b634853Cb333D3aD8663715b08f41A3Aec47cc",
                  }
    
    rollup_name = "arbitrum"
    
    sender_address = sender_dict[rollup_name]
    
    documents1 = []

    error_times = 0
    
    collection_l2delay = db[f'{rollup_name}_l2delay']    
    
    try:
        start = collection_l2delay.find_one(sort=[("l1_block", -1)])['l1_block']+1
    except:
        start = 19400000
    start =19328041 
    print(f"{rollup_name} : from block {start}")
    
    for tx in transactions_rollup.find({'sender':sender_address, 'block':{'$gte':start , '$lte':19400000-1 }}):
        try:
            block = tx['block']
            tx_hash = tx['tx_hash']
            try:
                response = requests.get(f"https://d24ut439kqiny5.cloudfront.net/v1/transaction/rollup/batch/{tx_hash}", 
                                     headers = {
                                                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
                                                'Referer': 'https://www.ethernow.xyz/',
                                                'Origin': 'https://www.ethernow.xyz',
                                                'Accept': 'application/json',
                                                'Content-Type': 'application/json'
                                                }).json()['l2Batch']
                error_times = 0
                time.sleep(random.randint(1,2))
            except:
                error_times += 1
                print(tx)
                if error_times == 2:

                    break
                continue

            if isinstance(response, dict):
                if "error" in response and response["error"] == "failed to decode batches":
                    continue

            if response == None or len(response) == 0:
                continue
#             else:
#                 response = response[0]

            sequence = response['sequenceNumber']
            l2_first_block = response['firstBlock']
            l2_last_block = response['lastBlock']
            l2_num_tx = len(response['txs'])
            l1_timestamp = el.eth.getBlock(block)['timestamp']
            
            t1 = get_timestamp(l2_first_block)
            time.sleep(random.randint(1,2))
            t2 = get_timestamp(l2_last_block)
            delay_sum = (l1_timestamp-(t1+t2)/2)*l2_num_tx

            documents1.append({'tx_hash':tx_hash,
                               'sequence':sequence,
                               'l1_block':block,
                               'l1_timestamp':l1_timestamp,
                               'l2_num_tx':l2_num_tx,
                               'l2_num_block':l2_last_block-l2_first_block+1,
                               'delay_sum':delay_sum})

            collection_l2delay.insert_many(documents1, ordered=False)
            documents1 = []

            print(block, "complete")
            time.sleep(random.randint(1,4))

        except Exception as e:
            print(tx,block)
            print(e)
            break




