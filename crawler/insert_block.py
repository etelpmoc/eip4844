import paths
from eip4844.setting import *
from pymongo import MongoClient
def fake_exponential(factor, numerator, denominator):
    output = 0
    accum = factor * denominator

    i = 1
    while accum > 0:
        output += accum
        accum = (accum * numerator) // (denominator * i)
        i += 1
    return output // denominator

if __name__ == "__main__":
    
    client = MongoClient(f'mongodb://{MONGODB_USER}:{MONGODB_PASSWORD}@localhost:27017/')
    db = client['ethereum']
    collection = db[f'blocks']
    
    w3 = Web3(Web3.HTTPProvider(f"""http://localhost:{PORT_NUM}"""))
    
    start = collection.find_one(sort=[("block", -1)])['block']+1
    end = w3.eth.block_number
    
    print(f"Starting updates from Slot #{start} to #{end}")

    documents = []
    for block in range(start, end):
        x = w3.eth.getBlock(block)

        if block < 19426587:
            blobGasUsed = 0
            blobBaseFee = 0
            excessBlobGas = 0
        else:
            blobGasUsed = x['blobGasUsed']
            excessBlobGas = x['excessBlobGas']
            blobBaseFee = fake_exponential(1, int(excessBlobGas,16), 3338477)
        
        documents.append({'block':block, 'baseFeePerGas': x['baseFeePerGas'],
                          'gasUsed':x['gasUsed'], 'size':x['size'], 
                          'txNum': len(x['transactions']),
                          'blobGasUsed':blobGasUsed,
                          'blobBaseFee':blobBaseFee,
                          'excessBlobGas':excessBlobGas
                         })
                
        if block%1000==0 or block == end-1:
            collection.insert_many(documents)
            documents = []
            print(block)


