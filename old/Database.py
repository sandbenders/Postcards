import random

from pymongo import MongoClient
from old.ProcessLines import ProcessLines


class Database:
    def __init__(self):
        super().__init__()
        self.client = MongoClient()
        self.db = self.client.pilovers
        self.collection = ''
        self.gender = 0
        self.process_lines = ProcessLines()

    def insert_post(self, line):
        post = {"line": line}
        post_id = self.collection.insert_one(post).inserted_id

    def get_line(self):
        self.gender = random.randrange(0, 2)
        print("GENDER: ", self.gender)
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
        print(line['line'])
        line_processed = self.process_lines.process_line(line['line'])
        if line['line'] != line_processed:
            print(line_processed)
            self.insert_post(line_processed)
        return line_processed
