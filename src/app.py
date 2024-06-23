from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.form['message']
    response = get_chatbot_response(user_message)
    return jsonify({'response': response})

def get_chatbot_response(message):
    # Placeholder for the chatbot response logic
    return "This is a response from the chatbot."

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
