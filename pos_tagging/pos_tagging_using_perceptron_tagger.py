# https://www.nltk.org/book/ch05.html

import nltk
# nltk.download('averaged_perceptron_tagger')
# nltk.download('tagsets')
# nltk.download('indian')

# loading in the resume
# file = open('../assets/resume.txt', 'r')
# document = file.read()
# file.close()

document = "to be or not to be, that is the question"

# tokenizing the document
tokenizer = nltk.RegexpTokenizer(r'\w+')
tokens = tokenizer.tokenize(document)
print(tokens)

# pos tagging the tokens using nltk
print(nltk.pos_tag(tokens))

# see documentation regarding a particular tag
tag = 'RB'
nltk.help.upenn_tagset(tag)

print(nltk.corpus.indian.tagged_words())
