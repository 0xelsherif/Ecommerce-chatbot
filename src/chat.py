import os
import random
import json
import torch
import string
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

def clean_word(word):
    return word.strip(string.punctuation).lower()

def extract_tags_from_sentence(sentence, connection):
    words = [clean_word(word) for word in sentence.split()]
    category_id = None
    brand_id = None
    category_name = None
    brand_name = None

    print(f"Processing words: {words}")

    for word in words:
        category_query = f"SELECT id, name FROM categories WHERE LOWER(name) = '{word}'"
        brand_query = f"SELECT id, name FROM brands WHERE LOWER(name) = '{word}'"

        category_result = execute_read_query(connection, category_query)
        brand_result = execute_read_query(connection, brand_query)

        print(f"Checking word '{word}':")
        print(f"  Category query: {category_query}")
        print(f"  Category result: {category_result}")
        print(f"  Brand query: {brand_query}")
        print(f"  Brand result: {brand_result}")

        if category_result and not category_id:
            category_id = category_result[0][0]
            category_name = category_result[0][1]
        if brand_result and not brand_id:
            brand_id = brand_result[0][0]
            brand_name = brand_result[0][1]

    return category_id, brand_id, category_name, brand_name

def get_response(tag, intents_json, connection, sentence):
    category_id, brand_id, category_name, brand_name = extract_tags_from_sentence(sentence, connection)
    print(f"Extracted Category ID: {category_id}")
    print(f"Extracted Brand ID: {brand_id}")

    if brand_id and category_id:
        query = f"""
        SELECT name, description, price 
        FROM products 
        WHERE brand_id = {brand_id} AND category_id = {category_id}
        AND stock_quantity > 0
        """
        products = execute_read_query(connection, query)
        print(f"Combined query: {query}")
        print(f"Products fetched: {products}")
        if products:
            product_list = "\n".join([f"Product Name: {product[0]}\nDescription: {product[1]}\nPrice: ${product[2]:.2f}\n" for product in products])
            return f"Here are some {brand_name} products in the {category_name} category we have available:\n\n{product_list}"
        else:
            return f"Sorry, we currently do not have any {brand_name} products in the {category_name} category in stock."

    if brand_id:
        query = f"""
        SELECT name, description, price 
        FROM products 
        WHERE brand_id = {brand_id}
        AND stock_quantity > 0
        """
        products = execute_read_query(connection, query)
        print(f"Brand query: {query}")
        print(f"Products fetched: {products}")
        if products:
            product_list = "\n".join([f"Product Name: {product[0]}\nDescription: {product[1]}\nPrice: ${product[2]:.2f}\n" for product in products])
            return f"Here are some {brand_name} products we have available:\n\n{product_list}"
        else:
            return f"Sorry, we currently do not have any {brand_name} products in stock."

    if category_id:
        query = f"""
        SELECT name, description, price 
        FROM products 
        WHERE category_id = {category_id}
        AND stock_quantity > 0
        """
        products = execute_read_query(connection, query)
        print(f"Category query: {query}")
        print(f"Products fetched: {products}")
        if products:
            product_list = "\n".join([f"Product Name: {product[0]}\nDescription: {product[1]}\nPrice: ${product[2]:.2f}\n" for product in products])
            return f"Here are some products we have available in the {category_name} category:\n\n{product_list}"
        else:
            return f"Sorry, we currently do not have any products in the {category_name} category in stock."

    # Default response for unknown tags
    for intent in intents_json["intents"]:
        if intent["tag"].lower() == tag:
            responses = [response.replace("{category}", category_name if category_name else "category")
                         .replace("{brand}", brand_name if brand_name else "brand") for response in intent["responses"]]
            return random.choice(responses)
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
