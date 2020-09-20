import pickle
import numpy as np


# defining the similary metric
def cosine_similarity(v1, v2):
    v1 = np.array(v1)
    v2 = np.array(v2)
    return v1.dot(v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))


# importing the vectors
file = open('../bow/one-hot-vector.p', 'rb')
vectors = pickle.load(file)
file.close()


# defining the similarity method
def most_similar(word):
    closest_words = []
    closest_word_metric = -1
    word_vector = vectors[word]
    for token, vector in vectors.items():
        if token == word:
            continue
        similarity = cosine_similarity(vector, word_vector)
        if similarity == closest_word_metric:
            closest_words.append(token)
        elif similarity > closest_word_metric:
            closest_word_metric = similarity
            closest_words = [token]
    return closest_words, closest_word_metric


print(most_similar('trinity'))
