
# E-commerce Customer Support Chatbot

## Overview

This project implements an intelligent chatbot for e-commerce customer support using Deep Learning and Natural Language Processing (NLP) techniques. The chatbot is built with PyTorch, utilizes fuzzy matching for better understanding of user queries, and stores chat history in a MySQL database.

## Features

- Responds to common customer queries about product information, orders, shipping, payments, and more.
- Handles typos and variations in user input using fuzzy matching.
- Stores chat history in a MySQL database for future reference.
- Trained on a comprehensive set of intents and patterns for robust performance.

## Project Structure

```
.
├── data
│   ├── intents.json          # JSON file containing training data for the chatbot
├── models
│   ├── chatbot_model.pth     # Trained model weights
├── src
│   ├── chat.py               # Main script to run the chatbot
│   ├── train.py              # Script to train the chatbot model
│   ├── preprocess.py         # Script for preprocessing text data
│   ├── database.py           # Script for database operations
├── tests
│   ├── test_chat.py          # Unit tests for chatbot
│   ├── test_train.py         # Unit tests for model training
├── requirements.txt          # Python dependencies
├── README.md                 # Project documentation
└── .gitignore                # Git ignore file
```

## Installation

### Prerequisites

- Python 3.7 or higher
- MySQL server

### Clone the Repository

```bash
git clone https://github.com/yourusername/ecommerce-chatbot.git
cd ecommerce-chatbot
```

### Install Python Dependencies

```bash
pip install -r requirements.txt
```

### Setup MySQL Database

1. **Start your MySQL server**.
2. **Create a new database**:

```sql
CREATE DATABASE ecommerce_db;
```

3. **Use the following SQL script to create necessary tables and insert sample data**:

```sql
USE ecommerce_db;

CREATE TABLE Customer (
    customer_id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(100) NOT NULL,
    address VARCHAR(100) NOT NULL,
    phone_number VARCHAR(100) NOT NULL
);

CREATE TABLE Chat_History (
    chat_id INT AUTO_INCREMENT PRIMARY KEY,
    customer_id INT,
    chat_text TEXT NOT NULL,
    response_text TEXT NOT NULL,
    chat_date DATETIME NOT NULL,
    FOREIGN KEY (customer_id) REFERENCES Customer(customer_id)
);

INSERT INTO Customer (first_name, last_name, email, password, address, phone_number)
VALUES
('John', 'Doe', 'john.doe@example.com', 'password123', '1234 Elm Street', '123-456-7890'),
('Jane', 'Smith', 'jane.smith@example.com', 'password456', '5678 Oak Street', '987-654-3210');
```

### Train the Model

1. **Ensure the `intents.json` file is properly formatted** in the `data` directory.
2. **Run the training script**:

```bash
python src/train.py
```

### Running the Chatbot

```bash
python src/chat.py
```

### Using the Chatbot

- **Start the script**: `python src/chat.py`
- **Interact with the chatbot**: Type your queries and the chatbot will respond based on the trained model and intents.
- **To exit**: Type `quit`

### Examples

```bash
You: Hello
E-commerceBot: Hello! How can I assist you today?
```

```bash
You: What laptops do you have?
E-commerceBot: Here are our laptops: [laptops link].
```

## Contributing

1. **Fork the repository**.
2. **Create a new branch** (`git checkout -b feature-branch`).
3. **Commit your changes** (`git commit -m 'Add some feature'`).
4. **Push to the branch** (`git push origin feature-branch`).
5. **Create a new Pull Request**.

## License

This project is licensed under the MIT License.

## Acknowledgements

- **fuzzywuzzy** for fuzzy matching of user inputs.
- **NLTK** for text preprocessing.
- **PyTorch** for model training and inference.
