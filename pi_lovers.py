from pymongo import MongoClient
import pprint

client = MongoClient()
db = client.pilovers
collection = db.elizabeth

pprint.pprint(collection.find_one())
