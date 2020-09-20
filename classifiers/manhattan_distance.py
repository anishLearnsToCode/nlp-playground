import pickle
import numpy as np
import pprint

# Loading one hot vector representation of words trained from the resume Corpus
file = open('../bow/one-hot-vector.p', 'rb')
vectors = pickle.load(file)
file.close()


# pprint.pprint(vectors)


# Find the Manhattan Distance between any 2 given vectors
def manhattan_distance(v1, v2):
    v1 = np.array(v1)
    v2 = np.array(v2)
    return np.abs(v1 - v2).sum()


# print(manhattan_distance(vectors['java'], vectors['data']))
# print(manhattan_distance(vectors['java'], vectors['structures']))
# print(manhattan_distance(vectors['java'], vectors['trinity']))


# creating a function to return the word that is most similar to a given word
def most_similar(word):
    closest_words = []
    closest_word_metric = float('inf')
    word_vector = vectors[word]
    for token, vector in vectors.items():
        if token == word:
            continue
        distance = manhattan_distance(vector, word_vector)
        if distance == closest_word_metric:
            closest_words.append(token)
        elif distance < closest_word_metric:
            closest_word_metric = distance
            closest_words = [token]
    return closest_words, closest_word_metric


print(most_similar('data'))
