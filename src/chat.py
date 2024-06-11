import random
import json
import torch
from preprocess import tokenize, stem, bag_of_words, load_intents, get_best_match
from train import NeuralNet
from database import create_connection, log_chat_history

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

FILE = "models/chatbot_model.pth"
model_data = torch.load(FILE, map_location=device)

input_size = model_data["input_size"]
hidden_size = model_data["hidden_size"]
output_size = model_data["output_size"]
all_words = model_data["all_words"]
tags = model_data["tags"]
model_state = model_data["model_state"]

model = NeuralNet(input_size, hidden_size, output_size).to(device)
model.load_state_dict(model_state)
model.eval()

# Load intents file
with open("data/intents.json", "r") as f:
    intents = json.load(f)

bot_name = "E-commerceBot"
connection = create_connection("localhost", "root", "", "ecommerce_db")

if connection is None:
    print("Failed to connect to the database. Please check your credentials.")
    exit()

def get_response(tag, intents_json):
    for intent in intents_json["intents"]:
        if intent["tag"] == tag:
            return random.choice(intent["responses"])

print("Let's chat! (type 'quit' to exit)")

while True:
    sentence = input("You: ")
    if sentence == "quit":
        break

    # Use fuzzy matching to handle typos and variations in user input
    all_patterns = [pattern for intent in intents["intents"] for pattern in intent["patterns"]]
    best_match = get_best_match(sentence, all_patterns)

    if best_match:
        for intent in intents["intents"]:
            if best_match in intent["patterns"]:
                tag = intent["tag"]
                break

        tokenized_sentence = tokenize(sentence)
        X = bag_of_words(tokenized_sentence, all_words)
        X = X.reshape(1, X.shape[0])
        X = torch.from_numpy(X).to(device)

        output = model(X)
        _, predicted = torch.max(output, dim=1)
        tag = tags[predicted.item()]

        probs = torch.softmax(output, dim=1)
        prob = probs[0][predicted.item()]

        confidence_threshold = 0.75  # Set the confidence threshold
        if prob.item() > confidence_threshold:
            response = get_response(tag, intents)
        else:
            response = "I do not understand..."
    else:
        response = "I do not understand..."
    
    print(f"{bot_name}: {response}")
    log_chat_history(connection, 1, sentence, response)  # Using a valid customer_id, e.g., 1
