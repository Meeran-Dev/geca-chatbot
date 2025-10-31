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

function markdownToHtml(markdown) {
            // 1. Handle code blocks (simple non-multiline for now)
            let html = markdown.replace(/`([^`]+)`/g, '<code>$1</code>');
            
            // 2. Convert bold (**text**)
            html = html.replace(/\*\*(.*?)\*\*/g, '<b>$1</b>');

            // 3. Convert bullet lists (* item)
            // Replace list items with <li>, preserving leading/trailing spaces for list grouping
            html = html.replace(/^(?:[\s]*?)[*-]\s+(.*)$/gm, '<li>$1</li>');
            
            // Group contiguous <li> elements into <ul> blocks
            html = html.replace(/(<li>.*?<\/li>)+/gs, '<ul>$&</ul>');
            
            // Remove redundant list wrappers (e.g., </ul><ul>)
            html = html.replace(/<\/ul>\n?<ul>/g, ''); 

            // 4. Convert double newlines to paragraph breaks, single newlines to <br>
            html = html.replace(/\n\s*\n/g, '</p><p>');
            html = html.replace(/\n/g, '<br>');
            
            // 5. Wrap the whole thing in a <p> tag if it doesn't already start with a block element
            if (!html.startsWith('<ul>') && !html.startsWith('<p>')) {
                 html = `<p>${html}</p>`;
            }

            return html;
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

function appendMessage(text, isUser, isError = false) {
            const chatBody = document.getElementById('chat-body');
            const messageWrapper = document.createElement('div');
            messageWrapper.className = `message ${isUser ? 'user-message' : 'bot-message'} ${isError ? 'error-message' : ''}`;
            
            if (isUser || isError) {
                // User messages and error messages are plain text
                messageWrapper.textContent = text;
            } else {
                // Bot responses are converted from Markdown to HTML
                messageWrapper.innerHTML = markdownToHtml(text);
            }

            chatBody.appendChild(messageWrapper);
            chatBody.scrollTop = chatBody.scrollHeight; // Auto-scroll to bottom
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
                appendMessage(data.response, false);
            }
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