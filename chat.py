import random
import json
import torch
import pymysql
from model import NeuralNet
from nltk_utils import bag_of_words, tokenize

# Load intents file
with open('intents.json', 'r') as json_data:
    intents = json.load(json_data)

# Load trained model
FILE = "data.pth"
data = torch.load(FILE)

input_size = data["input_size"]
hidden_size = data["hidden_size"]
num_layers = data["num_layers"]
output_size = data["output_size"]
all_words = data["all_words"]
tags = data["tags"]
model_state = data["model_state"]

model = NeuralNet(input_size, hidden_size, num_layers, output_size)
model.load_state_dict(model_state)
model.eval()

bot_name = "EcommerceBot"

def connect_to_db():
    return pymysql.connect(host='localhost', user='root', password='', db='ecommerce')

def get_order_status(order_id):
    db = connect_to_db()
    cursor = db.cursor()
    query = "SELECT status FROM orders WHERE order_id = %s"
    cursor.execute(query, (order_id,))
    result = cursor.fetchone()
    db.close()
    if result:
        return result[0]
    else:
        return "Order ID not found."

def get_response(msg):
    sentence = tokenize(msg)
    X = bag_of_words(sentence, all_words)
    X = X.reshape(1, 1, X.shape[0])  # Reshape to [batch_size, seq_length, input_size]
    X = torch.from_numpy(X).float()

    output = model(X)
    _, predicted = torch.max(output, dim=1)
    tag = tags[predicted.item()]

    probs = torch.softmax(output, dim=1)
    prob = probs[0][predicted.item()]

    if prob.item() > 0.75:
        for intent in intents["intents"]:
            if tag == intent["tag"]:
                return random.choice(intent["responses"])

    return "I do not understand..."

def chat():
    print("Let's chat! (type 'quit' to exit)")
    first_name = ""
    last_name = ""
    while True:
        sentence = input("You: ")
        if sentence == "quit":
            break

        response = get_response(sentence)

        if "{first_name}" in response:
            response = response.replace("{first_name}", first_name)
        if "{last_name}" in response:
            response = response.replace("{last_name}", last_name)

        if "What's your first name?" in response:
            first_name = input("Please enter your first name: ")
        elif "What's your last name?" in response:
            last_name = input("Please enter your last name: ")
        elif "Please provide your order tracking ID." in response:
            order_id = input("Order ID: ")
            status = get_order_status(order_id)
            response = f"Your order status is: {status}"

        print(f"{bot_name}: {response}")

if __name__ == "__main__":
    chat()
