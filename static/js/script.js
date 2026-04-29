document.addEventListener('DOMContentLoaded', () => {
    // DOM Elements
    const chatContainer = document.getElementById('chatContainer');
    const messagesWrapper = document.getElementById('messagesWrapper');
    const messageInput = document.getElementById('messageInput');
    const sendButton = document.getElementById('sendButton');
    const typingIndicator = document.getElementById('typingIndicator');
    const themeToggle = document.getElementById('themeToggle');
    const clearChat = document.getElementById('clearChat');

    // Theme Management
    const currentTheme = localStorage.getItem('theme') || 'dark';
    document.documentElement.setAttribute('data-theme', currentTheme);
    updateThemeIcon(currentTheme);

    themeToggle.addEventListener('click', () => {
        const newTheme = document.documentElement.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
        document.documentElement.setAttribute('data-theme', newTheme);
        localStorage.setItem('theme', newTheme);
        updateThemeIcon(newTheme);
    });

    function updateThemeIcon(theme) {
        const icon = themeToggle.querySelector('i');
        icon.className = theme === 'dark' ? 'fas fa-moon' : 'fas fa-sun';
    }

    // Clear Chat
    clearChat.addEventListener('click', () => {
        const messages = messagesWrapper.querySelectorAll('.message');
        messages.forEach((msg, index) => {
            if (index > 0) msg.remove();
        });
        typingIndicator.classList.remove('active');
    });

    // Auto-resize Textarea
    messageInput.addEventListener('input', () => {
        messageInput.style.height = 'auto';
        messageInput.style.height = `${messageInput.scrollHeight}px`;
    });

    // Send Message
    const sendMessage = async () => {
        const message = messageInput.value.trim();
        if (!message) return;

        // Add user message
        addMessage(message, 'user');
        messageInput.value = '';
        messageInput.style.height = 'auto';

        // Show typing indicator
        typingIndicator.classList.add('active');
        scrollToBottom();

        try {
            const response = await fetch('/generate_response', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message })
            });

            const data = await response.json();
            const botResponse = data.response || data.error || 'Sorry, something went wrong.';

            // Add bot message
            addMessage(botResponse, 'bot');
        } catch (error) {
            addMessage('Error: Could not connect to the server. Please try again.', 'bot');
        } finally {
            typingIndicator.classList.remove('active');
            scrollToBottom();
        }
    };

    // Add Message to Chat
    const addMessage = (text, sender) => {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${sender}-message`;

        const time = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });

        if (sender === 'bot') {
            messageDiv.innerHTML = `
                <div class="avatar bot-avatar">
                    <img src="/static/icons/logoacsn.png" alt="Bot Avatar">
                </div>
                <div class="message-content">
                    <div class="message-bubble">${formatText(text)}</div>
                    <span class="message-time">${time}</span>
                </div>
            `;
        } else {
            messageDiv.innerHTML = `
                <div class="avatar user-avatar">U</div>
                <div class="message-content">
                    <div class="message-bubble">${formatText(text)}</div>
                    <span class="message-time">${time}</span>
                </div>
            `;
        }

        messagesWrapper.appendChild(messageDiv);
        scrollToBottom();
    };

    // Format Text (handle newlines)
    const formatText = (text) => {
        return text.replace(/\n/g, '<br>');
    };

    // Scroll to Bottom
    const scrollToBottom = () => {
        chatContainer.scrollTop = chatContainer.scrollHeight;
    };

    // Event Listeners
    sendButton.addEventListener('click', sendMessage);
    messageInput.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    });

    // Initial scroll to bottom
    scrollToBottom();
});
