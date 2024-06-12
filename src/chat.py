import random
import json
import torch
from preprocess import tokenize, stem, bag_of_words, load_intents
from train import NeuralNet
from database import create_connection, log_chat_history, execute_read_query

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

# Load the trained model
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

def get_response(tag, intents_json, connection):
    if tag in ["laptops", "desktops", "tablets", "monitors", "accessories"]:
        query = f"""
        SELECT SKU, description, price 
        FROM product 
        WHERE category_id = (
            SELECT category_id 
            FROM category 
            WHERE LOWER(name) = '{tag}'
        )
        """
        products = execute_read_query(connection, query)
        if products:
            product_list = "\n".join([f"{product[0]}: {product[1]}, ${product[2]}" for product in products])
            return f"Here are some {tag} we have available:\n{product_list}"
        else:
            return f"Sorry, we currently do not have any {tag} in stock."
    else:
        for intent in intents_json["intents"]:
            if intent["tag"] == tag:
                return random.choice(intent["responses"])
    return "I'm not sure I understand. Can you please clarify?"

print("Let's chat! (type 'quit' to exit)")

while True:
    sentence = input("You: ")
    if sentence == "quit":
        break

    # Tokenize the sentence
    sentence_tokens = tokenize(sentence)
    X = bag_of_words(sentence_tokens, all_words)
    X = X.reshape(1, X.shape[0])
    X = torch.from_numpy(X).to(device)

    # Get model predictions
    output = model(X)
    _, predicted = torch.max(output, dim=1)
    tag = tags[predicted.item()]

    probs = torch.softmax(output, dim=1)
    prob = probs[0][predicted.item()]

    confidence_threshold = 0.75
    if prob.item() > confidence_threshold:
        response = get_response(tag, intents, connection)
    else:
        response = "I'm not sure I understand. Can you please clarify?"

    print(f"{bot_name}: {response}")
    log_chat_history(connection, 1, sentence, response)  # Assuming customer_id is 1 for this example
