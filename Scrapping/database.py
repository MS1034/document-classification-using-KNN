from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import pymongo


class Database:
    def __init__(self, db_name, collection_name, uri):
        self.client = MongoClient(uri, server_api=ServerApi('1'))
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]

    def insert_data(self, data):
        self.collection.insert_one(data)

    def get_all_data(self):
        return self.collection.find()

    def get_data(self, query):
        return self.collection.find(query)
