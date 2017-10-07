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


def random_number():
    return random.uniform(0, 1)


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
    choice = random_number()
    print(choice)
    if choice < 0.25:
        return rearrange_tokens(line)
    elif 0.25 < choice < 0.50:
        return similar_words(line)
    else:
        return line


def get_line():
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


if __name__ == '__main__':
    main()
