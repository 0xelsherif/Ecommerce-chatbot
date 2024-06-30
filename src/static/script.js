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
        const botMessage = document.createElement('div');
        botMessage.classList.add('message', 'bot');
        
        if (Array.isArray(data.response)) {
            const slider = document.createElement('div');
            slider.classList.add('slider');
            
            data.response.forEach(item => {
                const productDiv = document.createElement('div');
                productDiv.classList.add('product');

                if (item.name && item.description && item.price) {
                    const productName = document.createElement('h3');
                    productName.textContent = item.name;
                    productDiv.appendChild(productName);

                    const productDescription = document.createElement('p');
                    productDescription.textContent = item.description;
                    productDiv.appendChild(productDescription);

                    const productPrice = document.createElement('p');
                    productPrice.textContent = `Price: ${item.price}`;
                    productDiv.appendChild(productPrice);

                    const productImage = document.createElement('img');
                    productImage.src = 'path/to/your/image.jpg'; // Update this with actual product image path
                    productImage.alt = item.name;
                    productDiv.appendChild(productImage);

                    const orderButton = document.createElement('button');
                    orderButton.textContent = 'Order now';
                    orderButton.classList.add('order-button');
                    productDiv.appendChild(orderButton);

                    const showMoreButton = document.createElement('button');
                    showMoreButton.textContent = 'Show more';
                    showMoreButton.classList.add('show-more-button');
                    productDiv.appendChild(showMoreButton);
                } else {
                    const messageContent = document.createElement('div');
                    messageContent.classList.add('message-content');
                    messageContent.textContent = item.message;
                    productDiv.appendChild(messageContent);
                }

                slider.appendChild(productDiv);
            });

            botMessage.appendChild(slider);
        } else {
            const botMessageContent = document.createElement('div');
            botMessageContent.classList.add('message-content');
            botMessageContent.textContent = data.response.message;
            botMessage.appendChild(botMessageContent);
        }

        chatBox.appendChild(botMessage);
        chatBox.scrollTop = chatBox.scrollHeight;

        if (data.response.length > 1) {
            initializeSlider();
        }
    })
    .catch(error => {
        console.error("Error:", error);
    });

    userInput.value = '';
}

function initializeSlider() {
    const sliders = document.querySelectorAll('.slider');
    sliders.forEach(slider => {
        let isDown = false;
        let startX;
        let scrollLeft;

        slider.addEventListener('mousedown', (e) => {
            isDown = true;
            slider.classList.add('active');
            startX = e.pageX - slider.offsetLeft;
            scrollLeft = slider.scrollLeft;
        });

        slider.addEventListener('mouseleave', () => {
            isDown = false;
            slider.classList.remove('active');
        });

        slider.addEventListener('mouseup', () => {
            isDown = false;
            slider.classList.remove('active');
        });

        slider.addEventListener('mousemove', (e) => {
            if (!isDown) return;
            e.preventDefault();
            const x = e.pageX - slider.offsetLeft;
            const walk = (x - startX) * 3;
            slider.scrollLeft = scrollLeft - walk;
        });
    });
}
