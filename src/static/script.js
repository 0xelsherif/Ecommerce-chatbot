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

    // Fetch bot response from the server
    fetch("/chat", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ message: userInput.value })
    })
    .then(response => response.json())
    .then(data => {
        // Add bot's response
        const botMessage = document.createElement('div');
        botMessage.classList.add('message', 'bot');

        const botMessageContent = document.createElement('div');
        botMessageContent.classList.add('message-content');
        botMessageContent.textContent = data.response;

        botMessage.appendChild(botMessageContent);
        chatBox.appendChild(botMessage);

        // Scroll to the bottom of the chat box
        chatBox.scrollTop = chatBox.scrollHeight;
    })
    .catch(error => {
        console.error("Error:", error);
    });

    // Clear the input field
    userInput.value = '';
}