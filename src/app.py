from flask import Flask, request, jsonify, render_template
import json
import mysql.connector
from chat import get_response, extract_tags_from_sentence, create_session_if_not_exists, chat_with_bot

app = Flask(__name__)

# Load the intents JSON file
with open('data/intents.json') as json_file:
    intents_json = json.load(json_file)

# Database connection details (replace with your actual credentials)
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'computer_shop'
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message')
    if not user_message:
        return jsonify({"response": "Please say something..."})

    # Establish a new database connection for each request
    connection = mysql.connector.connect(**db_config)
    
    # Assuming session_id is handled in your logic; you may replace it with an actual session id logic
    session_id = 1

    # Process the user message and get a response
    response = chat_with_bot(user_message, session_id)
    
    connection.close()  # Ensure the connection is closed after use
    return jsonify({"response": response})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
