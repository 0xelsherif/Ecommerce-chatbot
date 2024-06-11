import unittest
import torch
from src.chat import bot_name, model, all_words, tags
from src.preprocess import tokenize, bag_of_words

class TestChat(unittest.TestCase):
    def test_bot_response(self):
        sentence = "Hi"
        tokenized_sentence = tokenize(sentence)
        bag = bag_of_words(tokenized_sentence, all_words)
        X = bag.reshape(1, bag.shape[0])
        X = torch.from_numpy(X)
        
        output = model(X)
        _, predicted = torch.max(output, dim=1)
        tag = tags[predicted.item()]

        probs = torch.softmax(output, dim=1)
        prob = probs[0][predicted.item()]

        self.assertGreater(prob.item(), 0.75)
        self.assertIn(tag, ["greeting", "goodbye", "thanks", "payments"])

if __name__ == "__main__":
    unittest.main()
