from pymongo import MongoClient
import random

'''
    type:
    male = 0
    female = 1
'''
type = 0

client = MongoClient()
db = client.pilovers


def get_line():
    random_number = random.uniform(0, 1)
    if type == 0:
        if random_number < 0.5:
            collection = db.flaubert
        else:
            collection = db.robert
    else:
        if random_number < 0.5:
            collection = db.elizabeth
        else:
            collection = db.sand

    count = collection.count()
    line = collection.find({}, {"line": 1, "_id": 0})[random.randrange(count)]
    return line['line']


def main():
    print(get_line())


if __name__ == '__main__':
    main()
