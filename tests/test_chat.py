import sys
import os

# Add the src directory to the system path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

import unittest
from unittest.mock import patch
import torch
from chat import bot_name, model, all_words, tags, chat_with_bot
from preprocess import tokenize, bag_of_words
from database import create_connection

class TestChat(unittest.TestCase):
    def setUp(self):
        self.connection = create_connection("localhost", "root", "yourpassword", "ecommerce_db")

    @patch('builtins.input', side_effect=['hello', 'quit'])
    def test_greeting(self, mock_input):
        response = chat_with_bot("hello")
        self.assertIn(response, ["Hello! How can I assist you today?", "Hi there! How can I help?", "Greetings! How may I assist you?"])

    @patch('builtins.input', side_effect=['what laptops do you have', 'quit'])
    def test_laptops(self, mock_input):
        response = chat_with_bot("what laptops do you have")
        self.assertTrue("Here are some laptops" in response or "Sorry, we currently do not have any laptops in stock." in response)

if __name__ == "__main__":
    unittest.main()
