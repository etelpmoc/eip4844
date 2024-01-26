import paths
from eip4844.setting import *
from pymongo import MongoClient
import requests

if __name__ == "__main__":
    
    client = MongoClient(f'mongodb://{MONGODB_USER}:{MONGODB_PASSWORD}@localhost:27017/')
    db = client['ethereum']
    collection = db['slots']
    
    r = requests.get(f"http://localhost:{BEACON_PORT_NUM}/eth/v1/beacon/headers")
    
    start = collection.find_one(sort=[("slot", -1)])['slot']+1
    end   = int(json.loads(r.text)['data'][0]['header']['message']['slot'])
    
    print(f"Starting updates from Block #{start} to #{end}")
    
    documents = []
    for slot in range(start, end):
        r = requests.get(f"http://localhost:{BEACON_PORT_NUM}/eth/v2/beacon/blocks/{slot}")
        try:
            message = json.loads(r.text)['data']['message']
        except:
            continue            

        documents.append({'slot':slot,
                          'block':message['body']['execution_payload']['block_number'],
                          'proposer_index':message['proposer_index'],
                          'attestation_length':len(message['body']['attestations']),
                          'fee_recipient':message['body']['execution_payload']['fee_recipient']
                          })
        
        if slot%1000==0 or slot == end-1:
            collection.insert_many(documents)
            documents = []
            print(slot)


