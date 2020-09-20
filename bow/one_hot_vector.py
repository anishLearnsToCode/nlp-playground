from collections import Counter

import nltk
import pandas
import pickle

# loading the document
resume = open('../assets/resume.txt', 'r')
document = resume.read().lower()
resume.close()

# tokenizing the document
tokenizer = nltk.RegexpTokenizer(r'\w+')
tokens = tokenizer.tokenize(document)

# divide the document into n parts
documents = []
n = 6
k = len(tokens) // n
for i in range(n):
    documents.append(tokens[k * i: len(tokens) if i == n - 1 else (i + 1) * k])

# extracting top m words from each document
m = 6

most_common = set()
for document in documents:
    frequency = Counter(document)
    for word, frequency in frequency.most_common(m):
        most_common.add(word)

# creating one hot vectors for each word in the most_common set
vectors = {}
for word in most_common:
    vector = [0] * n
    for index, document in enumerate(documents):
        vector[index] = int(word in document)
    vectors[word] = vector

# converting the vectors into a tabular format
table = pandas.DataFrame(vectors)
print(table.to_string())

# saving the output into text file
file = open('one-hot-vector.txt', 'w')
file.write(table.to_string())
file.close()

# saving the vectors so they can be used later on
file = open('one-hot-vector.p', 'wb')
pickle.dump(vectors, file)
file.close()
