import nltk
import random


class ProcessLines:
    def __init__(self):
        super().__init__()
        self.idx = nltk.text.ContextIndex([word.lower() for word in nltk.corpus.brown.words()])

    @staticmethod
    def random_number():
        return random.uniform(0, 1)

    @staticmethod
    def rearrange_tokens(line):
        tokens = nltk.word_tokenize(line)
        rearranged_line = ''
        while len(tokens) > 0:
            random_token = random.randrange(len(tokens))
            rearranged_line += " " + tokens[random_token]
            del tokens[random_token]
        return rearranged_line.lstrip(' ')

    def generate_mixed(self, line):
        rearranged_line = ''
        for word in nltk.word_tokenize(line):
            if self.random_number() < 0.50:
                rearranged_line += " " + self.generate_ascii(word)
            else:
                rearranged_line += " " + self.similar_words(word)
        if self.random_number() < 0.50:
            rearranged_line = self.rearrange_tokens(rearranged_line)
        return rearranged_line.lstrip(' ')

    def generate_ascii(self, line):
        rearranged_line = ''
        for word in nltk.word_tokenize(line):
            if self.random_number() < 0.50:
                rearranged_line += " " + '%d' * len(word) % tuple(map(ord, word))
            else:
                rearranged_line += " " + word
        return rearranged_line.lstrip(' ')

    def similar_words(self, line):
        rearranged_line = ''
        for word in nltk.word_tokenize(line):
            try:
                rearranged_line += " " + self.idx.similar_words(word)[0]
            except IndexError:
                rearranged_line += " " + word
                pass
        return rearranged_line.lstrip(' ')

    def process_line(self, line):
        if self.random_number() < 0.50:
            choice = self.random_number()
            print(choice)
            if choice < 0.05:
                return self.rearrange_tokens(line)
            elif 0.05 < choice < 0.90:
                return self.similar_words(line)
            elif 0.90 < choice < 0.95:
                return self.generate_ascii(line)
            else:
                return self.generate_mixed(line)
        else:
            return line
