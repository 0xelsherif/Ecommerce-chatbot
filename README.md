# E-commerce Customer Support Chatbot
[![Tests](https://github.com/0xelsherif/Ecommerce-chatbot/actions/workflows/python-tests.yml/badge.svg)](https://github.com/0xelsherif/Ecommerce-chatbot/actions/workflows/python-tests.yml)


## Overview

This project implements an intelligent chatbot for e-commerce customer support using Deep Learning and Natural Language Processing (NLP) techniques. The chatbot is built with PyTorch, utilizes fuzzy matching for better understanding of user queries, and stores chat history in a MySQL database.

## Features

- Responds to common customer queries about product information, orders, shipping, payments, and more.
- Handles typos and variations in user input using fuzzy matching.
- Stores chat history in a MySQL database for future reference.
- Trained on a comprehensive set of intents and patterns for robust performance.

### 1. Core Functionalities

#### 1.1 Chatbot Interaction

- **Greeting Responses**
  - Detects and responds to various greetings (e.g., "Hi", "Hello", "Hey").
- **Goodbye Responses**
  - Recognizes and responds to farewell messages (e.g., "Bye", "Goodbye", "See you later").
- **Thank You Responses**
  - Handles expressions of gratitude and responds appropriately (e.g., "Thanks", "Thank you").
- **Product Information**
  - Provides information on available products and categories (e.g., "What kind of tablets do you offer?").
- **Order and Shipping Queries**
  - Answers queries related to orders and shipping status (e.g., "Where is my order?", "How do I track my shipment?").
- **Payments and Billing**
  - Informs users about payment methods and billing inquiries (e.g., "What payment methods do you accept?", "How do I view my billing history?").
- **Returns and Exchanges**
  - Provides information on return policies and processes (e.g., "What is your return policy?", "How do I initiate a return?").
- **Warranty and Repairs**
  - Answers questions regarding product warranties and repair services (e.g., "Do your products come with a warranty?", "Where can I get my device repaired?").

### 2. User Interactions

#### 2.1 Natural Language Processing (NLP)

- **Tokenization**
  - Splits user inputs into individual words or tokens for processing.
- **Stemming**
  - Reduces words to their base or root form to handle different word variations.
- **Bag-of-Words Model**
  - Converts text input into a fixed-size array of word frequencies for model input.
- **Fuzzy Matching**
  - Handles typos and similar words by matching user input to known patterns.

#### 2.2 User History and Feedback

- **Chat History Logging**
  - Stores chat conversations in the database for future reference and analysis.
- **User Feedback Mechanism**
  - Collects user feedback on responses to improve the chatbot’s performance.

### 3. Data Handling

#### 3.1 Database Management

- **Customer Information**
  - Manages customer data, including names, addresses, and contact information.
- **Order Details**
  - Stores and retrieves information about customer orders and their statuses.
- **Product Information**
  - Maintains a catalog of products, including descriptions, prices, and stock levels.
- **Shipment Tracking**
  - Records shipment details and tracks their statuses.
- **Payment Records**
  - Manages payment history and billing information.

### 4. Additional Enhancements

#### 4.1 User Experience Improvements

- **Personalized Responses**
  - Provides personalized responses based on user history and preferences.
- **Multi-language Support**
  - Supports multiple languages for a broader user base.
- **Interactive Elements**
  - Uses buttons and quick replies for common queries to enhance user experience.

#### 4.2 Performance and Scalability

- **Model Training and Optimization**
  - Uses deep learning techniques to improve response accuracy and reduce training time.
- **Scalable Architecture**
  - Ensures the system can handle increasing user loads and data volumes.

#### 4.3 Security and Privacy

- **Data Encryption**
  - Encrypts sensitive user data to protect privacy.
- **Access Controls**
  - Implements role-based access controls to restrict data access to authorized personnel.
- **Compliance**
  - Ensures compliance with data protection regulations (e.g., GDPR, CCPA).

### 5. Analytics and Reporting

#### 5.1 Usage Analytics

- **Chat Analytics**
  - Tracks usage patterns, common queries, and response times.
- **Customer Satisfaction**
  - Measures user satisfaction through feedback and interaction quality.

#### 5.2 Reporting Tools

- **Performance Reports**
  - Generates reports on chatbot performance and user engagement.
- **Business Insights**
  - Provides insights into customer behavior and preferences for business decision-making.
    """

## Project Structure

```
.
├── data
│   ├── intents.json          # JSON file containing training data for the chatbot
│   └── database.sql          # SQL script to set up the database schema and initial data
├── models
│   └── chatbot_model.pth     # Trained model weights
├── src
│   ├── chat.py               # Main script to run the chatbot
│   ├── train.py              # Script to train the chatbot model
│   ├── preprocess.py         # Script for preprocessing text data
│   └── database.py           # Script for database operations
├── tests
│   ├── test_chat.py          # Unit tests for chatbot
│   ├── test_preprocess.py    # Unit tests for preprocessing functions
│   └── test_train.py         # Unit tests for model training
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
