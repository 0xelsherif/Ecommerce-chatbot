document.getElementById('chat-toggle').addEventListener('click', function() {
    const chatWidget = document.getElementById('chat-widget');
    if (chatWidget.style.display === 'none' || chatWidget.style.display === '') {
        chatWidget.style.display = 'flex';
    } else {
        chatWidget.style.display = 'none';
    }
});

document.getElementById('user-input').addEventListener('keydown', function(event) {
    if (event.key === 'Enter') {
        event.preventDefault();  // Prevent default action (adding a newline)
        sendMessage();
    }
});

function sendMessage() {
    const userInput = document.getElementById('user-input');
    const chatBox = document.getElementById('chat-box');

    if (userInput.value.trim() === '') {
        return;
    }

    // Add user's message
    const userMessage = document.createElement('div');
    userMessage.classList.add('message', 'user');

    const messageContent = document.createElement('div');
    messageContent.classList.add('message-content');
    messageContent.textContent = userInput.value;

    userMessage.appendChild(messageContent);

    chatBox.appendChild(userMessage);

    // Simulate bot response
    const botMessage = document.createElement('div');
    botMessage.classList.add('message', 'bot');

    const botMessageContent = document.createElement('div');
    botMessageContent.classList.add('message-content');
    botMessageContent.textContent = getBotResponse(userInput.value);

    botMessage.appendChild(botMessageContent);

    chatBox.appendChild(botMessage);

    // Scroll to the bottom of the chat box
    chatBox.scrollTop = chatBox.scrollHeight;

    // Clear the input field
    userInput.value = '';
}

function getBotResponse(userInput) {
    // Basic responses, can be enhanced with NLP or other logic
    const responses = {
        'hello': 'Hi there! How can I help you today?',
        'hi': 'Hello! How can I assist you?',
        'how are you': 'I am just a bot, but I am here to help you!',
        'bye': 'Goodbye! Have a great day!',
        '': 'Please say something...'
    };

    const defaultResponse = 'Sorry, I didn\'t understand that. Can you please rephrase?';

    return responses[userInput.toLowerCase()] || defaultResponse;
}
