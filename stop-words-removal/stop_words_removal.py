import nltk
from nltk.corpus import stopwords

# loading the document into the program
document = open('../assets/resume.txt', 'r')
resume = document.read()
document.close()

# tokenizing the document
tokenizer = nltk.RegexpTokenizer(r'\w+')
tokens = tokenizer.tokenize(resume)
print('Number of tokens:', len(tokens))

# loading stop words
stopwords_en = set(stopwords.words('english'))

# removing the stop words from the tokens
tokens = [token for token in tokens if token not in stopwords_en]
print('Number of Tokens after removing stop words:', len(tokens))
