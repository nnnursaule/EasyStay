// AI Assistant Component for EasyStay
// Include this script in any page where you want the AI assistant

document.addEventListener('DOMContentLoaded', function() {
    // Create the AI assistant widget elements
    const createAssistantWidget = () => {
        // Create the main container
        const aiWidget = document.createElement('div');
        aiWidget.className = 'ai-assistant-widget';
        aiWidget.id = 'aiAssistantWidget';

        // Create header
        const aiHeader = document.createElement('div');
        aiHeader.className = 'ai-header';

        const aiTitle = document.createElement('h3');
        aiTitle.textContent = 'EasyStay Assistant';

        const toggleBtn = document.createElement('button');
        toggleBtn.id = 'toggleAssistant';
        toggleBtn.textContent = '−';

        aiHeader.appendChild(aiTitle);
        aiHeader.appendChild(toggleBtn);

        // Create conversation container
        const aiConversation = document.createElement('div');
        aiConversation.className = 'ai-conversation';
        aiConversation.id = 'aiConversation';

        // Add welcome message
        const welcomeMsg = document.createElement('div');
        welcomeMsg.className = 'ai-message assistant';
        welcomeMsg.textContent = 'Hello! How can I help you with your accommodation needs today?';
        aiConversation.appendChild(welcomeMsg);

        // Create input area
        const aiInput = document.createElement('div');
        aiInput.className = 'ai-input';

        const userInput = document.createElement('input');
        userInput.type = 'text';
        userInput.id = 'userMessage';
        userInput.placeholder = 'Type your message...';

        const sendBtn = document.createElement('button');
        sendBtn.id = 'sendMessage';
        sendBtn.textContent = 'Send';

        aiInput.appendChild(userInput);
        aiInput.appendChild(sendBtn);

        // Create collapsed icon
        const collapsedIcon = document.createElement('div');
        collapsedIcon.className = 'ai-collapsed-icon';
        collapsedIcon.id = 'aiCollapsedIcon';

        const iconText = document.createElement('i');
        iconText.textContent = '💬';
        collapsedIcon.appendChild(iconText);

        // Append all elements to the widget
        aiWidget.appendChild(aiHeader);
        aiWidget.appendChild(aiConversation);
        aiWidget.appendChild(aiInput);
        aiWidget.appendChild(collapsedIcon);

        // Add styles
        const styleEl = document.createElement('style');
        styleEl.textContent = `
            .ai-assistant-widget {
                position: fixed;
                bottom: 20px;
                right: 20px;
                width: 350px;
                height: 450px;
                border-radius: 10px;
                box-shadow: 0 0 15px rgba(0,0,0,0.2);
                background-color: #fff;
                display: flex;
                flex-direction: column;
                overflow: hidden;
                z-index: 1000;
                transition: all 0.3s ease;
            }

            .ai-assistant-collapsed {
                height: 60px;
                width: 60px;
                border-radius: 50%;
            }

            .ai-header {
                background-color: #4a90e2;
                color: white;
                padding: 10px 15px;
                display: flex;
                justify-content: space-between;
                align-items: center;
            }

            .ai-header h3 {
                margin: 0;
                font-size: 16px;
            }

            .ai-header button {
                background: none;
                border: none;
                color: white;
                font-size: 20px;
                cursor: pointer;
            }

            .ai-conversation {
                flex: 1;
                padding: 15px;
                overflow-y: auto;
                display: flex;
                flex-direction: column;
            }

            .ai-message {
                margin-bottom: 10px;
                padding: 10px;
                border-radius: 8px;
                max-width: 80%;
                word-wrap: break-word;
            }

            .ai-message.user {
                align-self: flex-end;
                background-color: #e1f5fe;
            }

            .ai-message.assistant {
                align-self: flex-start;
                background-color: #f1f1f1;
            }

            .ai-input {
                padding: 10px;
                display: flex;
                border-top: 1px solid #eee;
            }

            .ai-input input {
                flex: 1;
                padding: 8px 10px;
                border: 1px solid #ddd;
                border-radius: 4px;
                margin-right: 8px;
            }

            .ai-input button {
                background-color: #4a90e2;
                color: white;
                border: none;
                padding: 8px 12px;
                border-radius: 4px;
                cursor: pointer;
            }

            .ai-collapsed-icon {
                display: none;
                width: 60px;
                height: 60px;
                background-color: #4a90e2;
                border-radius: 50%;
                justify-content: center;
                align-items: center;
                cursor: pointer;
            }

            .ai-collapsed-icon i {
                color: white;
                font-size: 24px;
            }

            .ai-assistant-collapsed .ai-header,
            .ai-assistant-collapsed .ai-conversation,
            .ai-assistant-collapsed .ai-input {
                display: none;
            }

            .ai-assistant-collapsed .ai-collapsed-icon {
                display: flex;
            }
        `;

        document.head.appendChild(styleEl);
        document.body.appendChild(aiWidget);

        return {
            widget: aiWidget,
            toggle: toggleBtn,
            collapsedIcon: collapsedIcon,
            conversation: aiConversation,
            inputField: userInput,
            sendButton: sendBtn
        };
    };

    // Initialize the widget and event handlers
    const initAssistant = () => {
        const elements = createAssistantWidget();
        let conversationId = null;
        let isCollapsed = false;

        // Toggle assistant visibility
        elements.toggle.addEventListener('click', function() {
            if (!isCollapsed) {
                elements.widget.classList.add('ai-assistant-collapsed');
                elements.toggle.textContent = '+';
                isCollapsed = true;
            } else {
                elements.widget.classList.remove('ai-assistant-collapsed');
                elements.toggle.textContent = '−';
                isCollapsed = false;
            }
        });

        // Expand when clicking the collapsed icon
        elements.collapsedIcon.addEventListener('click', function() {
            elements.widget.classList.remove('ai-assistant-collapsed');
            elements.toggle.textContent = '−';
            isCollapsed = false;
        });

        // Send message function
        async function sendMessage() {
            const userMessage = elements.inputField.value.trim();
            if (userMessage === '') return;

            // Add user message to the conversation
            addMessage(userMessage, 'user');
            elements.inputField.value = '';

            // Add a loading indicator
            const loadingIndicator = document.createElement('div');
            loadingIndicator.className = 'ai-message assistant';
            loadingIndicator.textContent = 'Typing...';
            elements.conversation.appendChild(loadingIndicator);

            try {
                // Make API call to your backend
                const response = await fetch('http://127.0.0.1:8011/api/ai/chat/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': getCookie('csrftoken')
                    },
                    body: JSON.stringify({
                        message: userMessage,
                        conversation_id: conversationId
                    })
                });

                const data = await response.json();

                // Remove loading indicator
                if (elements.conversation.contains(loadingIndicator)) {
                    elements.conversation.removeChild(loadingIndicator);
                }

                if (response.ok) {
                    // Add assistant response to the conversation
                    addMessage(data.response, 'assistant');
                    conversationId = data.conversation_id;
                } else {
                    // Add error message
                    addMessage('Sorry, I encountered an error. Please try again later.', 'assistant');
                    console.error('Error:', data.error);
                }
            } catch (error) {
                // Remove loading indicator and show error
                if (elements.conversation.contains(loadingIndicator)) {
                    elements.conversation.removeChild(loadingIndicator);
                }
                addMessage('Sorry, I encountered an error. Please try again later.', 'assistant');
                console.error('Error:', error);
            }
        }

        // Add a message to the conversation
        function addMessage(content, role) {
            const messageDiv = document.createElement('div');
            messageDiv.className = `ai-message ${role}`;
            messageDiv.textContent = content;
            elements.conversation.appendChild(messageDiv);
            elements.conversation.scrollTop = elements.conversation.scrollHeight;
        }

        // Send message on button click
        elements.sendButton.addEventListener('click', sendMessage);

        // Send message on Enter key
        elements.inputField.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                sendMessage();
            }
        });
    };

    // Helper function to get CSRF token
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    // Initialize the assistant
    initAssistant();
});
