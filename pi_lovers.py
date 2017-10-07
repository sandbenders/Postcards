from pymongo import MongoClient
import pprint
import random


def main():
    client = MongoClient()
    db = client.pilovers
    collection = db.elizabeth

    count = collection.count()
    pprint.pprint(collection.find()[random.randrange(count)])


if __name__ == '__main__':
    main()
