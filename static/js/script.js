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

        // Dynamic bot response based on time
        const botMsg = document.createElement('div');
        botMsg.className = 'message bot-message';
        const time = new Date();
        if (time.getHours() >= 17) {
            botMsg.textContent = `Good evening! It's 05:05 PM IST on October 13, 2025. ${messageText} - This is a sample response! How can I help you?`;
        } else {
            botMsg.textContent = `Good day! It's 05:05 PM IST on October 13, 2025. ${messageText} - This is a sample response! How can I help you?`;
        }
        chatBody.appendChild(botMsg);
        lastMessage = messageText;

        input.value = '';
        chatBody.scrollTop = chatBody.scrollHeight;
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

        // Dynamic bot response
        const botMsg = document.createElement('div');
        botMsg.className = 'message bot-message';
        if (messageText.toLowerCase().includes('forget')) {
            botMsg.textContent = 'If you want me to forget a chat, click the book icon beneath the message that references the chat and select it from the menu. Alternatively, you can disable memory in the "Data Controls" section of settings.';
        } else if (lastMessage && messageText.toLowerCase().includes(lastMessage.toLowerCase())) {
            botMsg.textContent = `You mentioned ${lastMessage} earlier. Here's a follow-up: This is a sample response! How can I assist?`;
        } else {
            botMsg.textContent = 'This is a sample response! How can I help you?';
        }
        chatBody.appendChild(botMsg);
        lastMessage = messageText;

        input.value = '';
        chatBody.scrollTop = chatBody.scrollHeight;
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