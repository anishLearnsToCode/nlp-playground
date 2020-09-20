# Term Frequency Inverse Document Frequency Bag of Words Representation

import math
import pickle
from collections import Counter

import nltk
import pandas

# loading the document
resume = open('../assets/resume.txt', 'r')
document = resume.read().lower()
resume.close()

# tokenizing the document
tokenizer = nltk.RegexpTokenizer(r'\w+')
tokens = tokenizer.tokenize(document)

# divide the document into n parts
documents = []
N_t = 6
k = len(tokens) // N_t
for i in range(N_t):
    documents.append(tokens[k * i: len(tokens) if i == N_t - 1 else (i + 1) * k])

# extracting top m words from each document
m = 6
most_common = set()
frequencies = []

for document in documents:
    frequency = Counter(document)
    frequencies.append(frequency)
    for word, frequency in frequency.most_common(m):
        most_common.add(word)


# calculating the count of word appearing in number of documents
N_w = {}
for word in most_common:
    count = 0
    for index, document in enumerate(documents):
        count += word in frequencies[index]
    N_w[word] = count

# creating TF-IDF vectors for each word in the most_common set
vectors = {}
for word in most_common:
    vector = [0] * N_t
    idf = math.log(N_t / N_w[word])
    for index, document in enumerate(documents):
        vector[index] = frequencies[index].get(word, 0) * idf
    vectors[word] = vector

# converting the vectors into a tabular format
table = pandas.DataFrame(vectors)
print(table.to_string())

# saving the output into text file
file = open('tf-idf.txt', 'w')
file.write(table.to_string())
file.close()

# saving the vectors in pickle file
file = open('tf-idf.p', 'wb')
pickle.dump(vectors, file)
file.close()
