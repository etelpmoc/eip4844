import paths
from eip4844.setting import *
from pymongo import MongoClient
import random
from lxml import html

if __name__ == "__main__" :
    el = Web3(Web3.HTTPProvider(f"""http://localhost:{PORT_NUM}"""))
    
    client = MongoClient(f'mongodb://{MONGODB_USER}:{MONGODB_PASSWORD}@localhost:27017/')
    db = client['ethereum']
    
    rollup_name = "linea"
    
    documents1 = []
    error_times = 0
    
    collection_l2delay = db[f'{rollup_name}_l2delay']    
    
    print(f"{rollup_name} start")
    
    
    batchnum_set = set()
    documents1 = []
    
    for page in range(1,110):
        html_content = requests.get(f"https://lineascan.build/batches?p={page}",
                                 headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36','referer': 'https://lineascan.build/batches'}).text
        time.sleep(random.randint(3,5))
        tree = html.fromstring(html_content)
        
        rows_xpath = "//tbody/tr"

        # Iterate over each row to extract the desired information
        for row in tree.xpath(rows_xpath):
            batch = int(row.xpath(".//td[1]/a/text()")[0])
            if batch in batchnum_set:
                continue
            batchnum_set.add(batch)

            l1_block = int(row.xpath(".//td[3]/a/text()")[0])
            tx_hash = row.xpath(".//td[4]/a/@title")[0]
            l1_timestamp = int(el.eth.getBlock(l1_block)['timestamp'])

            l2_num_block = int(row.xpath(".//td[7]/a/text()")[0])
            l2_num_tx = int(row.xpath(".//td[8]/a/text()")[0])

            html_content = requests.get(f"https://lineascan.build/blocks?batch={batch}", headers={
                   'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
                    }).text
            time.sleep(random.randint(1,3))
            tree = html.fromstring(html_content)

            l2_last_block = int(tree.xpath("//tbody/tr[1]/td[1]/a/text()")[0])
            l2_first_block = l2_last_block - l2_num_block + 1

            timestamp = tree.xpath("//tbody/tr[1]/td[2]/span/text()")[0]
            last_timestamp = int(datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S').timestamp()+32400)        

            html_content = requests.get(f"https://lineascan.build/block/{l2_first_block}", headers = {
                   'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
                    }).text
            time.sleep(random.randint(1,3))

            tree = html.fromstring(html_content)

            # Find the element containing the timestamp
            timestamp_element = tree.xpath('//div[contains(@class, "col-md-9")]')[1]

            # Extract the text containing the timestamp
            timestamp_text = timestamp_element.text_content()

            # Extract the timestamp part from the text (e.g., "Mar-31-2024 03:10:54 PM")
            timestamp_str = timestamp_text.split('(')[1].split(' +UTC)')[0]

            # Parse the timestamp string into a datetime object
            timestamp_datetime = datetime.strptime(timestamp_str, '%b-%d-%Y %I:%M:%S %p')

            # Convert datetime object to timestamp
            first_timestamp = int(timestamp_datetime.timestamp()+32400)

            delay_sum = (l1_timestamp-(first_timestamp+last_timestamp)/2)*l2_num_tx

            documents1.append({'batch':batch,
                               'tx_hash':tx_hash,
                               'l1_block':l1_block,
                               'l1_timestamp':l1_timestamp,
                               'l2_num_block':l2_num_block,
                               'l2_num_tx':l2_num_tx,
                               'l2_first_block':l2_first_block,
                               'l2_last_block':l2_last_block,
                               'delay_sum':delay_sum})

            collection_l2delay.insert_many(documents1, ordered=False)
            documents1 = []
            
        
        print(f"Page {page} ended")
        time.sleep(random.randint(3,13))




