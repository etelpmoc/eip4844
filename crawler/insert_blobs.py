import paths
from eip4844.setting import *
from pymongo import MongoClient

def calculate_actual_size(string):
    actual_size = 0
    consecutive_zeros = 0
    for char in string:
        if char != '0':
            actual_size += 1
            consecutive_zeros = 0
        else:
            consecutive_zeros += 1
            if consecutive_zeros >= 10:
                break  # Stop counting if 10 consecutive zeros are encountered
    return int((actual_size-2)/2)

if __name__ == "__main__":
    client = MongoClient(f'mongodb://{MONGODB_USER}:{MONGODB_PASSWORD}@localhost:27017/')
    db = client['ethereum']
    blob_transactions = db[f'blob_transactions']
    blob_sidecars = db['blobs']

    documents = []
    temp = 0
    for doc in blob_transactions.find({}):
        if temp == doc['block']: 
            continue
        blobs = requests.get(f"http://localhost:{BEACON_PORT_NUM}/eth/v1/beacon/blob_sidecars/{doc['slot']}").json()['data']

        for blob in blobs:
            documents.append({'slot':doc['slot'],
                              'block':doc['block'],
                              'blob_idnex':blob['index'],
                              'blob':blob['blob'],
                              'kzg_commitment':blob['kzg_commitment'],
                              'size':calculate_actual_size(blob['blob'])
                              })

        blob_sidecars.insert_many(documents)
        documents = []
        print(doc['block'])
        temp = doc['block']
