# Call Packages
from datetime import datetime
from pymongo import MongoClient
import requests
from pytz import timezone

# Get Tehran Time Zone
IRST = timezone('Asia/Tehran')

# Set Headers and Urls
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36 Edg/95.0.1020.53'}
url = "https://cdn.tsetmc.com/api/Instrument/GetInstrumentOptionMarketWatch/1"

def crawler():
    #Start Crawl
    response        = requests.get(url, headers=headers)
    # instrumentOptMarketWatch is list
    shareholders    = response.json()['instrumentOptMarketWatch']
    connection_string = 'mongodb://admin:pass@localhost:27017'
    client = MongoClient(connection_string)

    # DB config
    db = client['options']
    collection = db['options_snap']
    data_to_store = shareholders # Replace with the actual data
    result =collection.insert_many(data_to_store)

    #Attach Time of insert
    collection.update_many(
        {"_id": {"$in": result.inserted_ids}},
        {"$set": {  "time": datetime.now(IRST).strftime("%Y-%m-%d"),
                    "date": datetime.now(IRST).strftime("%H:%M:%S")
                }
        }
    )
    
if __name__ == "__main__":
    crawler()