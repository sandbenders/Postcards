from Database import Database
import random
import nltk

'''
    gender:
    male = 0
    female = 1
'''
gender = 0

idx = nltk.text.ContextIndex([word.lower() for word in nltk.corpus.brown.words()])


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
        if choice < 0.05:
            return rearrange_tokens(line)
        elif 0.05 < choice < 0.90:
            return similar_words(line)
        elif 0.90 < choice < 0.95:
            return generate_ascii(line)
        else:
            return generate_mixed(line)
    else:
        return line


def main():
    global gender
    database = Database()
    database.gender = gender
    while True:
        line = database.get_line()
        line_processed = process_line(line)
        print(line)
        print(line_processed)
        if line != line_processed:
            database.insert_post(line_processed)


if __name__ == '__main__':
    main()
