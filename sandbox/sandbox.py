import nltk
import nltk.text
import nltk.corpus

idx = nltk.text.ContextIndex([word.lower() for word in nltk.corpus.brown.words()])
save = []
rearranged_line = ''
for word in nltk.word_tokenize("i want to solve this problem"):
    save.append(idx.similar_words(word))
    rearranged_line += " " + idx.similar_words(word)[0]
print(rearranged_line)
