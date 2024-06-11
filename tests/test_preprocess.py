import unittest
import sys
import os

# Add the src directory to the path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from preprocess import tokenize, stem, bag_of_words

class TestPreprocess(unittest.TestCase):
    def test_tokenize(self):
        self.assertEqual(tokenize("Hello, how are you?"), ["Hello", ",", "how", "are", "you", "?"])

    def test_stem(self):
        self.assertEqual(stem("running"), "run")
        self.assertEqual(stem("jumps"), "jump")

    def test_bag_of_words(self):
        sentence = ["hello", "how", "are", "you"]
        words = ["hi", "hello", "I", "you", "bye", "thank", "cool"]
        expected = [0, 1, 0, 1, 0, 0, 0]
        self.assertTrue((bag_of_words(sentence, words) == expected).all())

if __name__ == "__main__":
    unittest.main()
