let chatStarted = false;
let lastMessage = null;

function toggleTheme() {
    const body = document.body;
    const themeIcon = document.querySelector('.theme-icon');
    if (body.getAttribute('data-theme') === 'dark') {
        body.setAttribute('data-theme', 'light');
        themeIcon.textContent = '☀️';
    } else {
        body.setAttribute('data-theme', 'dark');
        themeIcon.textContent = '🌙';
    }
}

function newChat() {
    const startScreen = document.getElementById('start-screen');
    const chatBody = document.getElementById('chat-body');
    const chatFooter = document.getElementById('chat-footer');

    startScreen.style.display = 'flex';
    chatBody.style.display = 'none';
    chatFooter.style.display = 'none';
    chatBody.innerHTML = '';
    chatStarted = false;
    lastMessage = null;
}

function attachPhoto() {
    const input = document.createElement('input');
    input.type = 'file';
    input.accept = 'image/*';
    input.onchange = function(event) {
        const file = event.target.files[0];
        if (file) {
            const chatBody = document.getElementById('chat-body');
            const photoMsg = document.createElement('div');
            photoMsg.className = 'message user-message photo-message';
            photoMsg.innerHTML = `<img src="${URL.createObjectURL(file)}" alt="Attached photo" style="max-width: 200px; border-radius: 8px;">`;
            chatBody.appendChild(photoMsg);
            chatBody.scrollTop = chatBody.scrollHeight;

            // Simulate bot response for image
            setTimeout(() => {
                const botMsg = document.createElement('div');
                botMsg.className = 'message bot-message';
                botMsg.textContent = 'I received your photo! It looks interesting. How can I assist you further?';
                chatBody.appendChild(botMsg);
                chatBody.scrollTop = chatBody.scrollHeight;
            }, 500);
        }
    };
    input.click();
}

function sendInitialMessage() {
    const input = document.getElementById('search-input');
    const messageText = input.value.trim();
    const chatBody = document.getElementById('chat-body');
    const chatFooter = document.getElementById('chat-footer');
    const startScreen = document.getElementById('start-screen');

    if (messageText) {
        startScreen.style.display = 'none';
        chatBody.style.display = 'flex';
        chatFooter.style.display = 'flex';
        chatStarted = true;

        const userMsg = document.createElement('div');
        userMsg.className = 'message user-message';
        userMsg.textContent = messageText;
        chatBody.appendChild(userMsg);

        // Show loading indicator
        const loadingMsg = document.createElement('div');
        loadingMsg.className = 'message bot-message loading';
        loadingMsg.textContent = 'Thinking...';
        chatBody.appendChild(loadingMsg);
        chatBody.scrollTop = chatBody.scrollHeight;

        // Send message to backend
        fetch('/generate_response', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ message: messageText })
        })
        .then(response => response.json())
        .then(data => {
            // Remove loading message
            chatBody.removeChild(loadingMsg);

            const botMsg = document.createElement('div');
            botMsg.className = 'message bot-message';
            if (data.error) {
                botMsg.textContent = 'Sorry, I encountered an error: ' + data.error;
            } else {
                botMsg.textContent = data.response;
            }
            chatBody.appendChild(botMsg);
            chatBody.scrollTop = chatBody.scrollHeight;
        })
        .catch(error => {
            // Remove loading message
            chatBody.removeChild(loadingMsg);

            const botMsg = document.createElement('div');
            botMsg.className = 'message bot-message';
            botMsg.textContent = 'Sorry, I couldn\'t process your message. Please try again.';
            chatBody.appendChild(botMsg);
            chatBody.scrollTop = chatBody.scrollHeight;
        });

        lastMessage = messageText;
        input.value = '';
    }
}

function sendMessage() {
    const input = document.getElementById('user-input');
    const messageText = input.value.trim();
    const chatBody = document.getElementById('chat-body');
    const chatFooter = document.getElementById('chat-footer');
    const startScreen = document.getElementById('start-screen');

    if (messageText) {
        if (!chatStarted) {
            startScreen.style.display = 'none';
            chatBody.style.display = 'flex';
            chatFooter.style.display = 'flex';
            chatStarted = true;
        }

        const userMsg = document.createElement('div');
        userMsg.className = 'message user-message';
        userMsg.textContent = messageText;
        chatBody.appendChild(userMsg);

        // Show loading indicator
        const loadingMsg = document.createElement('div');
        loadingMsg.className = 'message bot-message loading';
        loadingMsg.textContent = 'Thinking...';
        chatBody.appendChild(loadingMsg);
        chatBody.scrollTop = chatBody.scrollHeight;

        // Send message to backend
        fetch('/generate_response', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ message: messageText })
        })
        .then(response => response.json())
        .then(data => {
            // Remove loading message
            chatBody.removeChild(loadingMsg);

            const botMsg = document.createElement('div');
            botMsg.className = 'message bot-message';
            if (data.error) {
                botMsg.textContent = 'Sorry, I encountered an error: ' + data.error;
            } else {
                botMsg.textContent = data.response;
            }
            chatBody.appendChild(botMsg);
            chatBody.scrollTop = chatBody.scrollHeight;
        })
        .catch(error => {
            // Remove loading message
            chatBody.removeChild(loadingMsg);

            const botMsg = document.createElement('div');
            botMsg.className = 'message bot-message';
            botMsg.textContent = 'Sorry, I couldn\'t process your message. Please try again.';
            chatBody.appendChild(botMsg);
            chatBody.scrollTop = chatBody.scrollHeight;
        });

        lastMessage = messageText;
        input.value = '';
    }
}

// Event listeners
document.getElementById('user-input').addEventListener('keypress', function(e) {
    if (e.key === 'Enter') {
        sendMessage();
    }
});

document.getElementById('search-input').addEventListener('keypress', function(e) {
    if (e.key === 'Enter') {
        sendInitialMessage();
    }
});

document.getElementById('search-input').addEventListener('paste', function(e) {
    setTimeout(() => {
        e.target.style.background = 'var(--input-bg)';
    }, 0);
});