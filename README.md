The key/value store project is developed based on Flask in Python. It provides four RESTful APIs: `get`, `set`, `get_all`, `clear`. It uses lock to handle multiple clients setting and getting the same key simultaneously. It stores the data to a json file for persistent storage. It also provides unit tests for all the interfaces. 

Simply type python app.py to run the server after installing the dependency in requirements.txt and run the curl.py script and test_app.py to test the interfaces.

Things that can be improved:
* I chose json file to store the data out of simplicity. In reality it should be persisted to a database.
* I used lock to synchronize the multi_thread but it'll have performance issues in real production. Since the read operation happens more frequently than the write in key-value store, we can use read_write lock to improve the performance, but it's still blocked in some way when we perform the write operation. We can scale our key value store to a cluster using master-slave architecture and have master node do the write operation, but this might have a single point of failure issue. We can also use commit log to guarantee concurrency like modern databases do, having a seperate program to run the commit log and update the data asynchronously.
* Eviction policy and expiration time on keys and values. We can use LRU algorithm to evict the least recently used data, because the data is more likely to be accessed again if it's recently accessed.
* Scale our key value store. We can choose the round robin algorithm to request a server or even consistent hashing for dealing with adding more machines or server-crashes.

```
Set key "field1": http://localhost:8080/set/name?value=Gideon
{
    "name": {
        "value": "Gideon",
        "time": 1521510748.194219
    }
}

Get key "name": http://localhost:8080/get/name
{
    "value": "Gideon",
    "time": 1521510748.194219
}

Get all : http://localhost:8080/get
{
    "data": {
        "name": {
            "value": "Gideon",
            "time": 1521510748.194219
        },
        "address": {
            "value": "80 xxx Ave",
            "time": 1521511234.783954
        },
        "phone": {
            "value": "631-526-3415",
            "time": 1521895671.873445
        }
    }
}

Clear all : http://localhost:8080/clear
{
    "data": {
    }
}
```
