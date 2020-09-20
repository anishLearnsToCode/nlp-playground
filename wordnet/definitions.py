import nltk
from nltk.corpus import wordnet
from nltk.corpus import wordnet as wn

synsets = wordnet.synsets('bass')
print(synsets[0].definition())
print(synsets[0].examples())

print(wordnet.synset('dog.n.01').examples())

print(wn.synset('dog.n.01').lowest_common_hypernyms(wn.synset('cat.n.01')))
