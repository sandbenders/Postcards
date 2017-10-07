from pymongo import MongoClient
import random


def main():
    client = MongoClient()
    db = client.pilovers
    collection = db.elizabeth

    count = collection.count()
    line = collection.find({}, {"line": 1, "_id": 0})[random.randrange(count)]
    print(line["line"])


if __name__ == '__main__':
    main()
