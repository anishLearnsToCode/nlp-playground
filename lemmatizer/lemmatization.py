import nltk
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet


# importing the resume
# resume = open('../assets/resume.txt', 'r')
# document = resume.read()
# resume.close()

document = "rocks are better than a vague corpora"

# Tokenizing the document
tokenizer = nltk.RegexpTokenizer(r'\w+')
tokens = tokenizer.tokenize(document)
print(tokens[:15])

# lemmatizing the tokens
lemmatizer = WordNetLemmatizer()
# for token in tokens:
#     print(token, lemmatizer.lemmatize(token))

# extracting pos tags of the tokens
pos_tags = {}
for token in tokens:
    synsets = wordnet.synsets(token)
    if len(synsets) > 0:
        pos_tags[token] = synsets[0].pos()

print(pos_tags)

# examples (by default pos is assumed 'n': noun)
print(lemmatizer.lemmatize('rocks'))
print(lemmatizer.lemmatize('corpora'))
print(lemmatizer.lemmatize('better'))
print(lemmatizer.lemmatize('better', pos='a'))
