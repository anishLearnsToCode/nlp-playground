from collections import Counter
import math
import random
import numpy as np
import pandas as pd
import nltk
import pprint

## loading the data
with open('../assets/en_US_twitter.txt', 'r') as f:
    data = f.read().lower()

# tokenizing the entire corpus and storing frequency of each word
tokenizer = nltk.RegexpTokenizer(r'\w+')
corpus_tokens = tokenizer.tokenize(data)
corpus_tokens = [token for token in corpus_tokens if token.isalpha()]
token_frequencies = Counter(corpus_tokens)


# we split data into sentences and tokenize each sentence
def split_to_sentences(data):
    sentences = data.split('\n')
    sentences = [sentence.strip() for sentence in sentences]
    sentences = [s for s in sentences if len(s) > 0]
    return sentences


def tokenize_sentences(sentences):
    tokenized_sentences = []
    for sentence in sentences:
        sentence = sentence.lower()
        tokenized = tokenizer.tokenize(sentence)
        tokenized = [token for token in tokenized if token.isalpha()]
        tokenized_sentences.append(tokenized)
    return tokenized_sentences


def get_tokenized_data(data):
    sentences = split_to_sentences(data)
    tokenized_sentences = tokenize_sentences(sentences)
    return tokenized_sentences


tokens = get_tokenized_data(data)

# creating frequency count of tokens in each sentence
frequencies = []
for sentence in tokens:
    frequencies.append(Counter(sentence))

# creating the vocabulary from the tokens if the token appears more than threshold times in the entire corpus
vocabulary = set()
threshold = 2
for sentence in tokens:
    for token in sentence:
        if token_frequencies.get(token, 0) >= threshold:
            vocabulary.add(token)


# print('Number of words in vocabulary:', len(vocabulary))
# print('first 20 words:', list(vocabulary)[0:20])


# going through every sentence and replacing out of vocabulary words (oovs) with <unk> symbol
def replace_oov_words_by_unk(tokenized_sentences, vocabulary, unknown_token='<unk>'):
    replaced_tokenized_sentences = []

    for sentence in tokenized_sentences:
        replaced_sentence = []
        for token in sentence:
            replaced_sentence.append(token if token in vocabulary else unknown_token)
        replaced_tokenized_sentences.append(replaced_sentence)
    return replaced_tokenized_sentences


tokenized_sentences_unk = replace_oov_words_by_unk(tokens, vocabulary)


# we now create the n Grams Language Model
def count_n_grams(data, n, start_token='<s>', end_token='<e>'):
    n_grams = {}
    for sentence in data:
        sentence = [start_token] * n + sentence + [end_token]
        sentence = tuple(sentence)
        for i in range(len(sentence) - n + 1):
            n_gram = sentence[i: i + n]
            n_grams[n_gram] = n_grams.get(n_gram, 0) + 1
    return n_grams


unigrams = count_n_grams(tokens, 1)
bigrams = count_n_grams(tokens, 2)
trigrams = count_n_grams(tokens, 3)


# print(unigrams)
# print(bigrams)
# print(trigrams)


# estimate probability of word given previous n-gram count
def estimate_probability(word, previous_n_gram,
                         n_gram_counts, n_plus1_gram_counts, vocabulary_size, k=1.0):
    previous_n_gram_count = n_gram_counts.get(previous_n_gram, 0)
    # print(previous_n_gram_count)

    # Calculate the denominator using the count of the previous n gram
    # and apply k-smoothing
    denominator = previous_n_gram_count + k * vocabulary_size

    # Define n plus 1 gram as the previous n-gram plus the current word as a tuple
    n_plus1_gram = previous_n_gram + (word,)

    # Set the count to the count in the dictionary,
    # otherwise 0 if not in the dictionary
    # use the dictionary that has counts for the n-gram plus current word
    n_plus1_gram_count = n_plus1_gram_counts.get(n_plus1_gram, 0)
    # print(n_plus1_gram_count)

    # Define the numerator use the count of the n-gram plus current word,
    # and apply smoothing
    numerator = n_plus1_gram_count + k

    # Calculate the probability as the numerator divided by denominator
    probability = numerator / denominator
    return probability


# print(estimate_probability('am', ('i', ), unigrams, bigrams, len(vocabulary)))


# Estimate Probabilities of all words
def estimate_probabilities(previous_n_gram, n_gram_counts, n_plus1_gram_counts, vocabulary, k=1.0):
    """
    Estimate the probabilities of next words using the n-gram counts with k-smoothing

    Args:
        previous_n_gram: A sequence of words of length n
        n_gram_counts: Dictionary of counts of n-grams
        n_plus1_gram_counts: Dictionary of counts of (n+1)-grams
        vocabulary: List of words
        k: positive constant, smoothing parameter

    Returns:
        A dictionary mapping from next words to the probability.
    """

    # convert list to tuple to use it as a dictionary key

    # add <e> <unk> to the vocabulary
    # <s> is not needed since it should not appear as the next word
    vocabulary.add('<e>')
    vocabulary.add('<unk>')
    vocabulary_size = len(vocabulary)

    probabilities = {}
    for word in vocabulary:
        probability = estimate_probability(word, previous_n_gram,
                                           n_gram_counts, n_plus1_gram_counts,
                                           vocabulary_size, k=k)
        probabilities[word] = probability

    return probabilities


# probabilities = estimate_probabilities(('i', 'will'), bigrams, trigrams, vocabulary, k=1)
# pprint.pprint(probabilities)

# Creating a probability Matrix
def make_count_matrix(n_plus1_gram_counts, vocabulary):
    # add <e> <unk> to the vocabulary
    # <s> is omitted since it should not appear as the next word
    vocabulary.add("<e>")
    vocabulary.add("<unk>")

    # obtain unique n-grams
    n_grams = []
    for n_plus1_gram in n_plus1_gram_counts.keys():
        n_gram = n_plus1_gram[0:-1]
        n_grams.append(n_gram)
    n_grams = list(set(n_grams))

    # mapping from n-gram to row
    row_index = {n_gram: i for i, n_gram in enumerate(n_grams)}
    # mapping from next word to column
    col_index = {word: j for j, word in enumerate(vocabulary)}

    nrow = len(n_grams)
    ncol = len(vocabulary)
    count_matrix = np.zeros((nrow, ncol))
    for n_plus1_gram, count in n_plus1_gram_counts.items():
        n_gram = n_plus1_gram[0:-1]
        word = n_plus1_gram[-1]
        if word not in vocabulary:
            continue
        i = row_index[n_gram]
        j = col_index[word]
        count_matrix[i, j] = count

    count_matrix = pd.DataFrame(count_matrix, index=n_grams, columns=vocabulary)
    return count_matrix


sentences = [['i', 'like', 'a', 'cat'],
             ['this', 'dog', 'is', 'like', 'a', 'cat']]
unique_words = set(sentences[0] + sentences[1])
bigram_counts = count_n_grams(sentences, 2)


# print('bigram counts')
# print(make_count_matrix(bigram_counts, unique_words))


# Making Probability Matrix
def make_probability_matrix(n_plus1_gram_counts, vocabulary, k):
    count_matrix = make_count_matrix(n_plus1_gram_counts, unique_words)
    count_matrix += k
    prob_matrix = count_matrix.div(count_matrix.sum(axis=1), axis=0)
    return prob_matrix


# sentences = [['i', 'like', 'a', 'cat'],
#              ['this', 'dog', 'is', 'like', 'a', 'cat']]
# unique_words = set(sentences[0] + sentences[1])
# bigram_counts = count_n_grams(sentences, 2)
# print("bigram probabilities")
# print(make_probability_matrix(bigram_counts, unique_words, k=1).to_string())


# We calculate Perplexity score
def calculate_perplexity(sentence, n_gram_counts, n_plus1_gram_counts, vocabulary_size, k=1.0):
    n = len(list(n_gram_counts.keys())[0])
    sentence = ["<s>"] * n + sentence + ["<e>"]
    sentence = tuple(sentence)
    N = len(sentence)

    product_pi = 1.0
    for t in range(n, N):
        n_gram = sentence[t - n: t]
        word = sentence[t]
        probability = estimate_probability(word, n_gram, n_gram_counts, n_plus1_gram_counts, len(unique_words), k=1)
        product_pi *= 1 / probability

    perplexity = product_pi ** (1 / N)
    return perplexity

