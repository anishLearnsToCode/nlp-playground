import pickle


# defining the similarity metric
def jaccard_similarity(v1, v2):
    s1 = set(v1)
    s2 = set(v2)
    return len(s1.intersection(s2)) / len(s1.union(s2))


# importing the Term Frequency Inverse Document Frequency (TF-IDF) Vectors computed from Resume
file = open('../bow/tf-idf.p', 'rb')
vectors = pickle.load(file)
file.close()


# defining the similarity method to find closest functions
def most_similar(word):
    closest_words = []
    closest_word_metric = 0
    word_vector = vectors[word]
    for token, vector in vectors.items():
        if token == word:
            continue
        similarity = jaccard_similarity(vector, word_vector)
        if similarity == closest_word_metric:
            closest_words.append(token)
        elif similarity > closest_word_metric:
            closest_word_metric = similarity
            closest_words = [token]
    return closest_words, closest_word_metric


print(most_similar('guitar'))
