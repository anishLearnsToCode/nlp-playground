# https://www.nltk.org/book/ch05.html

import nltk
from nltk.corpus import wordnet
# nltk.download('wordnet')
# nltk.download('averaged_perceptron_tagger')

# importing the document
# resume = open('../assets/resume.txt', 'r')
# docuemnt = resume.read()
# resume.close()

document = "this is a sample document"

# creating the tokens
tokenizer = nltk.RegexpTokenizer(r'\w+')
tokens = tokenizer.tokenize(document)

# creating the synset mapping for each token in our document
synset_mapping = {}

for token in tokens:
    synset_mapping[token] = wordnet.synsets(token)

# some tokens will not have any synset mapping and for those we do not find any pos tags
for word in synset_mapping:
    if len(synset_mapping[word]) != 0:
        synset_mapping[word] = synset_mapping[word][0].pos()

print(synset_mapping)
