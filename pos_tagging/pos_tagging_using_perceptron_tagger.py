import nltk
nltk.download('averaged_perceptron_tagger')

# loading in the resume
# file = open('../assets/resume.txt', 'r')
# document = file.read()
# file.close()

document = "to be or not to be, that is the question"

# tokenizing the document
tokenizer = nltk.RegexpTokenizer(r'\w+')
