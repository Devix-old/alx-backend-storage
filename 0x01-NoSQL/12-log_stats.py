#!/usr/bin/env python3
"""script that provides some stats about Nginx logs stored in MongoDB"""
from pymongo import MongoClient


if __name__ == "__main__":
    client = MongoClient('mongodb://127.0.0.1:27017')
    school_collection = client.logs.nginx
    doc_count = school_collection.count_documents({})
    print(f'{doc_count} logs')
    method = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    print('Methods:')
    for m in method:
        count = school_collection.count_documents({"method": m})
        print(f'    method {m}: {count}')
    status_check = school_collection.count_documents(
        {"method": "GET", "path": "/status"}
    )
    print(f'{status_check} status check')
