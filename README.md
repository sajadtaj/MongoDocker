# Docker + Mongodb + TSETMC + Options

**Use Mongo DB for store Option Data from TSETMC**

---

### Overview:

This project aims to provide a Docker-based solution for crawling option data from Tsetmc, Iran's Securities and Exchange Organization. It utilizes MongoDB as the database and MongoDB Express for easy management and visualization of the data. The crawling process is automated using a Python script named `crawler.py`.

### Prerequisites:

- Docker installed on your system. You can download it from [here](https://www.docker.com/get-started).
- Basic understanding of Docker and Python.

### Installation:

1. Clone this repository to your local machine:

    ```bash
    git clone https://github.com/sajadtaj/MongoDocker
    ```

### Setup:

1. Start Docker containers for MongoDB and MongoDB Express:

    ```bash
    docker compose up
    ```



2. Once the containers are up and running, MongoDB Express can be accessed via `http://localhost:8081` in your web browser. Use the default MongoDB connection string: `mongodb://mongo:27017`.

3. Modify the `crawler.py` script according to your requirements. You might need to adjust the crawling logic, data processing, or database interaction based on your specific use case.

### Usage:

- Run the crawler script to start fetching option data from Tsetmc:

    ```bash
    python crawler.py
    ```

### Inside crawler.py

```python
# Call Packages
from datetime import datetime
from pymongo import MongoClient
import requests
import json
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
```
### Configuration:

- **MongoDB Connection:** Ensure that the MongoDB connection string in the `crawler.py` script matches the Docker configuration:

    ```python
    connection_string = 'mongodb://admin:pass@localhost:27017'
    client = MongoClient(connection_string)   

    ```

### Attach Time when insert new document

```python
    IRST = timezone('Asia/Tehran')
    collection.update_many(
    {"_id": {"$in": result.inserted_ids}},
    {"$set": {  "time": datetime.now(IRST).strftime("%Y-%m-%d"),
                "date": datetime.now(IRST).strftime("%H:%M:%S")
            }
    }
)
```
### Contributors:

- [sajadtaj](https://github.com/sajadtaj)

### License:

This project is licensed under the MIT License.

### Acknowledgements:

- Thanks to Tsetmc for providing the option data (Json).

### Note:

- This project is for educational and informational purposes only. Use the data obtained responsibly and in compliance with all relevant regulations and terms of service.
- For any issues or feature requests, feel free to create an issue on the GitHub repository.

---
