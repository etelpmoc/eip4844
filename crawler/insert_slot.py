import paths
from eip4844.setting import *
from pymongo import MongoClient

if __name__ == "__main__":
    start = int(sys.argv[1])
    end   = int(sys.argv[2])
    
    client = MongoClient(f'mongodb://{MONGODB_USER}:{MONGODB_PASSWORD}@localhost:27017/')
    r = requests.get(f"http://localhost:3500/eth/v2/beacon/blocks/8234586")
    db = client['ethereum']
    collection = db['slots']
    
    
    documents = []
    for slot in range(start, end):
        r = requests.get(f"http://localhost:{BEACON_PORT_NUM}/eth/v2/beacon/blocks/{slot}")
        message = json.loads(r.text)['data']['message']

        documents.append({'slot':slot,
                          'block':message['execution_payload']['block_number'],
                          'proposer_index':message['proposer_index'],
                          'attestation_length':len(message['body']['attestations']),
                          'fee_recipient':message['body']['execution_payload']['fee_recipient']
                          })
        
        if slot%1000==0 or slot == end-1:
            collection.insert_many(documents)
            documents = []
            print(slot)


