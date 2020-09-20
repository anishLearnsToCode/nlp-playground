import pickle
import pprint
import numpy as np

# loading in Term Frequency (TF) Vectors calculated from the resume corpus
file = open('../bow/tf.p', 'rb')
vectors = pickle.load(file)
file.close()


# creating a function that will return the euclidean distance between 2 vectors
def euclidean_distance(v1, v2):
    v1 = np.array(v1)
    v2 = np.array(v2)
    return np.sqrt(((v1 - v2) ** 2).sum())


def most_similar(word):
    closest_words = []
    closest_word_metric = float('inf')
    word_vector = vectors[word]
    for token, vector in vectors.items():
        if token == word:
            continue
        distance = euclidean_distance(vector, word_vector)
        if distance == closest_word_metric:
            closest_words.append(token)
        elif distance < closest_word_metric:
            closest_word_metric = distance
            closest_words = [token]
    return closest_words, closest_word_metric


print(most_similar('and'))
