from pymongo import MongoClient
import random


class Database:
    def __init__(self):
        super().__init__()
        self.client = MongoClient()
        self.db = self.client.pilovers
        self.collection = ''
        self.gender = 0

    def insert_post(self, line):
        post = {"line": line}
        post_id = self.collection.insert_one(post).inserted_id

    def get_line(self):
        choice = random.uniform(0, 1)
        if self.gender == 0:
            if choice < 0.5:
                self.collection = self.db.flaubert
            else:
                self.collection = self.db.robert
        else:
            if choice < 0.5:
                self.collection = self.db.elizabeth
            else:
                self.collection = self.db.sand

        count = self.collection.count()
        line = self.collection.find({}, {"line": 1, "_id": 0})[random.randrange(count)]
        return line['line']
