import os
import random
import json
import torch
from preprocess import tokenize, stem, bag_of_words, load_intents, get_best_match
from train import NeuralNet
from database import create_connection, log_chat_history, execute_read_query

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

# Load the trained model
FILE = os.path.join(os.path.dirname(__file__), '..', 'models', 'chatbot_model.pth')
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
with open(os.path.join(os.path.dirname(__file__), '..', 'data', 'intents.json'), "r") as f:
    intents = json.load(f)

bot_name = "E-commerceBot"
connection = create_connection("localhost", "root", "", "computer_shop")

if connection is None:
    raise Exception("Failed to connect to the database. Please check your credentials.")

def get_response(tag, intents_json, connection, sentence):
    normalized_tag = tag.lower()

    # Identify if the tag is a category or brand
    is_category = False
    is_brand = False

    # Check if tag is a category
    category_query = f"SELECT id FROM categories WHERE LOWER(name) = '{normalized_tag}'"
    category_result = execute_read_query(connection, category_query)
    if category_result:
        is_category = True

    # Check if tag is a brand
    brand_query = f"SELECT id FROM brands WHERE LOWER(name) = '{normalized_tag}'"
    brand_result = execute_read_query(connection, brand_query)
    if brand_result:
        is_brand = True

    # If both category and brand are mentioned
    words = sentence.lower().split()
    category_id = None
    brand_id = None

    if is_category:
        category_id = category_result[0][0]
    if is_brand:
        brand_id = brand_result[0][0]

    # Check if both category and brand are present in the sentence
    if category_id and brand_id:
        query = f"""
        SELECT name, description, price 
        FROM products 
        WHERE category_id = {category_id} AND brand_id = {brand_id}
        AND stock_quantity > 0
        """
        products = execute_read_query(connection, query)
        if products:
            product_list = "\n".join([f"Product Name: {product[0]}\nDescription: {product[1]}\nPrice: ${product[2]:.2f}\n" for product in products])
            return f"Here are some {tag} {tag} we have available:\n\n{product_list}"
        else:
            return f"Sorry, we currently do not have any {tag} {tag} in stock."

    if is_category:
        query = f"""
        SELECT name, description, price 
        FROM products 
        WHERE category_id = {category_id}
        AND stock_quantity > 0
        """
        products = execute_read_query(connection, query)
        if products:
            product_list = "\n".join([f"Product Name: {product[0]}\nDescription: {product[1]}\nPrice: ${product[2]:.2f}\n" for product in products])
            return f"Here are some {tag} we have available:\n\n{product_list}"
        else:
            return f"Sorry, we currently do not have any {tag} in stock."
    
    if is_brand:
        query = f"""
        SELECT name, description, price 
        FROM products 
        WHERE brand_id = {brand_id}
        AND stock_quantity > 0
        """
        products = execute_read_query(connection, query)
        if products:
            product_list = "\n".join([f"Product Name: {product[0]}\nDescription: {product[1]}\nPrice: ${product[2]:.2f}\n" for product in products])
            return f"Here are some {tag} products we have available:\n\n{product_list}"
        else:
            return f"Sorry, we currently do not have any {tag} products in stock."

    # Default response for unknown tags
    for intent in intents_json["intents"]:
        if intent["tag"].lower() == tag:
            return random.choice(intent["responses"])
    return "I'm not sure I understand. Can you please clarify?"

def create_session_if_not_exists(connection, session_id):
    query = "SELECT id FROM chat_sessions WHERE id = %s"
    cursor = connection.cursor()
    cursor.execute(query, (session_id,))
    result = cursor.fetchone()
    
    if not result:
        query = "INSERT INTO chat_sessions (id) VALUES (%s)"
        cursor.execute(query, (session_id,))
        connection.commit()
    
    cursor.close()

def chat_with_bot(sentence, session_id):
    create_session_if_not_exists(connection, session_id)
    
    best_match = None
    for intent in intents["intents"]:
        match = get_best_match(sentence, intent["patterns"])
        if match:
            best_match = intent["tag"]
            break

    if not best_match:
        response = "I'm not sure I understand. Can you please clarify?"
    else:
        sentence_tokens = tokenize(sentence)
        X = bag_of_words(sentence_tokens, all_words)
        X = X.reshape(1, X.shape[0])
        X = torch.from_numpy(X).to(device)

        output = model(X)
        _, predicted = torch.max(output, dim=1)
        tag = tags[predicted.item()]

        probs = torch.softmax(output, dim=1)
        prob = probs[0][predicted.item()]

        confidence_threshold = 0.75
        if prob.item() > confidence_threshold:
            response = get_response(tag, intents, connection, sentence)
        else:
            response = "I'm not sure I understand. Can you please clarify?"

    log_chat_history(connection, session_id, sentence, response)
    return response

if __name__ == "__main__":
    print("Let's chat! (type 'quit' to exit)")
    session_id = 1  # This should be dynamically set based on your application logic
    while True:
        sentence = input("You: ")
        if sentence == "quit":
            break
        response = chat_with_bot(sentence, session_id)
        print(f"{bot_name}: {response}")
