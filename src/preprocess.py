# import nltk
# from nltk.stem.porter import PorterStemmer
# import numpy as np
# import json

# nltk.download('punkt')

# stemmer = PorterStemmer()

# def tokenize(sentence):
#     return nltk.word_tokenize(sentence)

# def stem(word):
#     return stemmer.stem(word.lower())

# def bag_of_words(tokenized_sentence, words):
#     sentence_words = [stem(word) for word in tokenized_sentence]
#     bag = np.zeros(len(words), dtype=np.float32)
#     for idx, w in enumerate(words):
#         if w in sentence_words:
#             bag[idx] = 1.0
#     return bag

# def load_intents(file_path):
#     with open(file_path, 'r') as f:
#         intents = json.load(f)
#     return intents

# if __name__ == "__main__":
#     intents = load_intents('data/intents.json')
#     all_words = []
#     tags = []
#     xy = []
#     for intent in intents['intents']:
#         tag = intent['tag']
#         tags.append(tag)
#         for pattern in intent['patterns']:
#             w = tokenize(pattern)
#             all_words.extend(w)
#             xy.append((w, tag))
#     ignore_words = ['?', '!', '.', ',']
#     all_words = [stem(w) for w in all_words if w not in ignore_words]
#     all_words = sorted(set(all_words))
#     tags = sorted(set(tags))

#     print(all_words)
#     print(tags)
from fuzzywuzzy import process
import nltk
from nltk.stem.porter import PorterStemmer
import numpy as np
import json

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
    with open(file_path, 'r') as f:
        intents = json.load(f)
    return intents

def get_best_match(input_sentence, patterns):
    best_match, score = process.extractOne(input_sentence, patterns)
    return best_match if score >= 75 else None  # 75 is the confidence threshold
