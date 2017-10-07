from pymongo import MongoClient
import random
import nltk

'''
    type:
    male = 0
    female = 1
'''
type = 0

idx = nltk.text.ContextIndex([word.lower() for word in nltk.corpus.brown.words()])

client = MongoClient()
db = client.pilovers
collection = ''


def insert_post(line):
    global collection
    post = {"line": line}
    post_id = collection.insert_one(post).inserted_id


def random_number():
    return random.uniform(0, 1)


def generate_mixed(line):
    rearranged_line = ''
    for word in nltk.word_tokenize(line):
        if random_number() < 0.50:
            rearranged_line += " " + generate_ascii(word)
        else:
            rearranged_line += " " + similar_words(word)
    if random_number() < 0.50:
        rearranged_line = rearrange_tokens(rearranged_line)
    return rearranged_line.lstrip(' ')


def generate_ascii(line):
    rearranged_line = ''
    for word in nltk.word_tokenize(line):
        if random_number() < 0.50:
            rearranged_line += " " + '%d' * len(word) % tuple(map(ord, word))
        else:
            rearranged_line += " " + word
    return rearranged_line.lstrip(' ')


def similar_words(line):
    rearranged_line = ''
    for word in nltk.word_tokenize(line):
        try:
            rearranged_line += " " + idx.similar_words(word)[0]
        except IndexError:
            rearranged_line += " " + word
            pass
    return rearranged_line.lstrip(' ')


def rearrange_tokens(line):
    tokens = nltk.word_tokenize(line)
    rearranged_line = ''
    while len(tokens) > 0:
        random_token = random.randrange(len(tokens))
        rearranged_line += " " + tokens[random_token]
        del tokens[random_token]
    return rearranged_line.lstrip(' ')


def process_line(line):
    if random_number() < 0.50:
        choice = random_number()
        print(choice)
        if choice < 0.25:
            return rearrange_tokens(line)
        elif 0.25 < choice < 0.50:
            return similar_words(line)
        elif 0.50 < choice < 0.75:
            return generate_ascii(line)
        else:
            return generate_mixed(line)
    else:
        return line


def get_line():
    global collection
    choice = random_number()
    if type == 0:
        if choice < 0.5:
            collection = db.flaubert
        else:
            collection = db.robert
    else:
        if choice < 0.5:
            collection = db.elizabeth
        else:
            collection = db.sand

    count = collection.count()
    line = collection.find({}, {"line": 1, "_id": 0})[random.randrange(count)]
    return line['line']


def main():
    while True:
        line = get_line()
        line_processed = process_line(line)
        print(line)
        print(line_processed)
        if line != line_processed:
            insert_post(line_processed)


if __name__ == '__main__':
    main()
