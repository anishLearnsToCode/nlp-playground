# import nltk
# nltk.download('punkt')
from nltk.tokenize import word_tokenize


def n_grams(document: str, n=1):
    tokens = word_tokenize(document)
    # print(tokens)
    return [tokens[i: i + n] for i in range(0, len(tokens) - n + 1)]


doc = '/start this is a good day /end'
unigrams = n_grams(doc, 1)
print(unigrams)
bigrams = n_grams(doc, 2)
print(bigrams)
trigrams = n_grams(doc, 3)
print(trigrams)
