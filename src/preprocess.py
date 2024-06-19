import os
import json
import nltk
from nltk.stem.porter import PorterStemmer
import numpy as np
from fuzzywuzzy import process

nltk.download('punkt')

stemmer = PorterStemmer()

def tokenize(sentence):
    return nltk.word_tokenize(sentence)

def stem(word):
    return stemmer.stem(word.lower())

def bag_of_words(tokenized_sentence, words):
    sentence_words = [stem(word) for word in tokenized_sentence]
    bag = np.zeros(len(words), dtype=np.float32)
    for idx, w in enumerate(words):
        if w in sentence_words:
            bag[idx] = 1.0
    return bag

def load_intents(file_path):
    file_path = os.path.join(os.path.dirname(__file__), '..', file_path)
    with open(file_path, 'r') as f:
        intents = json.load(f)
    return intents

def get_best_match(input_sentence, patterns):
    best_match, score = process.extractOne(input_sentence, patterns)
    return best_match if score >= 75 else None
