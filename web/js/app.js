/**
 * Sermon AI - Web Interface
 * Frontend JavaScript for chat interaction
 */

// State
const state = {
    messages: [],
    isLoading: false,
    currentMode: 'chat',
    sessionContext: {
        scripture: '',
        topic: '',
        moduleOutputs: {}
    }
};

// DOM Elements
const messagesContainer = document.getElementById('messages');
const messageInput = document.getElementById('message-input');
const sendBtn = document.getElementById('send-btn');
const newChatBtn = document.getElementById('new-chat');
const chatTitle = document.getElementById('chat-title');
const chatSubtitle = document.getElementById('chat-subtitle');
const modulePanel = document.getElementById('module-panel');
const closePanel = document.getElementById('close-panel');

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    setupEventListeners();
    autoResizeTextarea();
});

// Event Listeners
function setupEventListeners() {
    // Send message
    sendBtn.addEventListener('click', sendMessage);
    messageInput.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    });

    // Input validation
    messageInput.addEventListener('input', () => {
        sendBtn.disabled = !messageInput.value.trim();
        autoResizeTextarea();
    });

    // New chat
    newChatBtn.addEventListener('click', startNewChat);

    // Starter prompts
    document.querySelectorAll('.starter-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            messageInput.value = btn.textContent.replace(/^"|"$/g, '');
            sendBtn.disabled = false;
            messageInput.focus();
        });
    });

    // Quick actions
    document.querySelectorAll('.action-btn').forEach(btn => {
        btn.addEventListener('click', () => handleQuickAction(btn.dataset.action));
    });

    // Navigation
    document.querySelectorAll('.nav-btn').forEach(btn => {
        btn.addEventListener('click', () => handleNavigation(btn.dataset.mode));
    });

    // Module panel
    closePanel.addEventListener('click', () => {
        modulePanel.classList.remove('active');
    });

    // Module items
    document.querySelectorAll('.module-item').forEach(item => {
        item.addEventListener('click', () => handleModuleClick(item.dataset.module));
    });
}

// Auto-resize textarea
function autoResizeTextarea() {
    messageInput.style.height = 'auto';
    messageInput.style.height = Math.min(messageInput.scrollHeight, 200) + 'px';
}

// Send message
async function sendMessage() {
    const content = messageInput.value.trim();
    if (!content || state.isLoading) return;

    // Clear input
    messageInput.value = '';
    sendBtn.disabled = true;
    autoResizeTextarea();

    // Remove welcome message if present
    const welcomeMsg = document.querySelector('.welcome-message');
    if (welcomeMsg) {
        welcomeMsg.remove();
    }

    // Add user message
    addMessage('user', content);

    // Show typing indicator
    const typingDiv = showTypingIndicator();

    // Send to API
    state.isLoading = true;
    try {
        const response = await fetch('/.netlify/functions/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                message: content,
                context: state.sessionContext,
                history: state.messages.slice(-10) // Last 10 messages for context
            })
        });

        if (!response.ok) {
            throw new Error('Failed to get response');
        }

        const data = await response.json();

        // Remove typing indicator
        typingDiv.remove();

        // Add assistant message
        addMessage('assistant', data.response);

        // Update context if provided
        if (data.context) {
            state.sessionContext = { ...state.sessionContext, ...data.context };
        }

    } catch (error) {
        console.error('Error:', error);
        typingDiv.remove();
        addMessage('assistant', 'Sorry, I encountered an error. Please try again.');
    }

    state.isLoading = false;
}

// Add message to chat
function addMessage(role, content) {
    const message = { role, content, timestamp: Date.now() };
    state.messages.push(message);

    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${role}`;

    const avatar = document.createElement('div');
    avatar.className = 'message-avatar';
    avatar.textContent = role === 'assistant' ? '📖' : '👤';

    const contentDiv = document.createElement('div');
    contentDiv.className = 'message-content';
    contentDiv.innerHTML = formatMessage(content);

    messageDiv.appendChild(avatar);
    messageDiv.appendChild(contentDiv);

    messagesContainer.appendChild(messageDiv);
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
}

// Format message content (basic markdown)
function formatMessage(content) {
    // Escape HTML
    let formatted = content
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;');

    // Headers
    formatted = formatted.replace(/^### (.+)$/gm, '<h3>$1</h3>');
    formatted = formatted.replace(/^## (.+)$/gm, '<h2>$1</h2>');
    formatted = formatted.replace(/^# (.+)$/gm, '<h1>$1</h1>');

    // Bold
    formatted = formatted.replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>');

    // Italic
    formatted = formatted.replace(/\*(.+?)\*/g, '<em>$1</em>');

    // Code blocks
    formatted = formatted.replace(/```([\s\S]*?)```/g, '<pre><code>$1</code></pre>');

    // Inline code
    formatted = formatted.replace(/`(.+?)`/g, '<code>$1</code>');

    // Blockquotes
    formatted = formatted.replace(/^&gt; (.+)$/gm, '<blockquote>$1</blockquote>');

    // Lists
    formatted = formatted.replace(/^\* (.+)$/gm, '<li>$1</li>');
    formatted = formatted.replace(/^- (.+)$/gm, '<li>$1</li>');
    formatted = formatted.replace(/^(\d+)\. (.+)$/gm, '<li>$2</li>');

    // Wrap consecutive list items
    formatted = formatted.replace(/(<li>.*<\/li>\n?)+/g, '<ul>$&</ul>');

    // Paragraphs
    formatted = formatted.replace(/\n\n/g, '</p><p>');
    formatted = '<p>' + formatted + '</p>';

    // Clean up empty paragraphs
    formatted = formatted.replace(/<p><\/p>/g, '');
    formatted = formatted.replace(/<p>(<h[1-3]>)/g, '$1');
    formatted = formatted.replace(/(<\/h[1-3]>)<\/p>/g, '$1');
    formatted = formatted.replace(/<p>(<ul>)/g, '$1');
    formatted = formatted.replace(/(<\/ul>)<\/p>/g, '$1');
    formatted = formatted.replace(/<p>(<blockquote>)/g, '$1');
    formatted = formatted.replace(/(<\/blockquote>)<\/p>/g, '$1');
    formatted = formatted.replace(/<p>(<pre>)/g, '$1');
    formatted = formatted.replace(/(<\/pre>)<\/p>/g, '$1');

    return formatted;
}

// Show typing indicator
function showTypingIndicator() {
    const typingDiv = document.createElement('div');
    typingDiv.className = 'message assistant';
    typingDiv.innerHTML = `
        <div class="message-avatar">📖</div>
        <div class="message-content">
            <div class="typing-indicator">
                <span></span>
                <span></span>
                <span></span>
            </div>
        </div>
    `;
    messagesContainer.appendChild(typingDiv);
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
    return typingDiv;
}

// Start new chat
function startNewChat() {
    state.messages = [];
    state.sessionContext = { scripture: '', topic: '', moduleOutputs: {} };

    messagesContainer.innerHTML = `
        <div class="welcome-message">
            <div class="welcome-icon">📖</div>
            <h2>Welcome to Sermon AI</h2>
            <p>I'm your pastoral preparation assistant. I don't just generate content—I think like a pastor, communicator, and spiritual guide.</p>

            <div class="starter-prompts">
                <h3>Try asking:</h3>
                <button class="starter-btn">"Help me prepare a sermon on John 3:16"</button>
                <button class="starter-btn">"Find scriptures about hope in suffering"</button>
                <button class="starter-btn">"What's the sharp edge of Romans 8:28?"</button>
                <button class="starter-btn">"Help me create a bottom line for Psalm 23"</button>
            </div>
        </div>
    `;

    // Re-attach starter button listeners
    document.querySelectorAll('.starter-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            messageInput.value = btn.textContent.replace(/^"|"$/g, '');
            sendBtn.disabled = false;
            messageInput.focus();
        });
    });
}

// Handle quick actions
function handleQuickAction(action) {
    const prompts = {
        scriptures: 'Help me find scriptures for a sermon about ',
        illustrations: 'Generate sermon illustrations for the topic of ',
        outline: 'Create a sermon outline for ',
        series: 'Help me plan a sermon series on '
    };

    if (prompts[action]) {
        messageInput.value = prompts[action];
        messageInput.focus();
        sendBtn.disabled = false;
    }
}

// Handle navigation
function handleNavigation(mode) {
    document.querySelectorAll('.nav-btn').forEach(btn => {
        btn.classList.toggle('active', btn.dataset.mode === mode);
    });

    state.currentMode = mode;

    if (mode === 'prep') {
        modulePanel.classList.add('active');
        chatTitle.textContent = '12-Module Preparation';
        chatSubtitle.textContent = 'Guided sermon development';
    } else {
        modulePanel.classList.remove('active');
        chatTitle.textContent = 'Sermon Assistant';
        chatSubtitle.textContent = 'Ask anything about sermon preparation';
    }
}

// Handle module click
function handleModuleClick(moduleNum) {
    const moduleNames = {
        1: 'Define Preaching',
        2: 'Identify the People',
        3: 'Pick Text & Target',
        4: 'Original Context',
        5: 'Find Movement',
        6: 'Surprise & Offense',
        7: 'Bridge to Today',
        8: 'Bottom Line',
        9: 'Build Structure',
        10: 'Applications',
        11: 'Gospel Center',
        12: 'Preacher Formation'
    };

    const prompts = {
        1: 'Help me with Module 1: Define Preaching. What transformation should this sermon invite people into?',
        2: 'Help me with Module 2: Identify the People. Who is in my congregation - both the skeptics and the long-time believers?',
        3: 'Help me with Module 3: Pick the Text and Target. What needs healing, confronting, or re-orienting?',
        4: 'Help me with Module 4: Original Context Exegesis. What did this text mean to the original audience?',
        5: 'Help me with Module 5: Find Movement. How does this passage journey emotionally and theologically?',
        6: 'Help me with Module 6: Surprise and Offense. What sharp edge has familiarity dulled?',
        7: 'Help me with Module 7: Bridge to Today. Where does this show up in modern life?',
        8: 'Help me with Module 8: Form the Bottom Line. What one sentence should people remember?',
        9: 'Help me with Module 9: Build Structure. Create movements, chunks, and seams for my sermon.',
        10: 'Help me with Module 10: Applications. What specific, embodied applications should I include?',
        11: 'Help me with Module 11: Gospel Centering. How do I ensure Jesus is central, not optional?',
        12: 'Help me with Module 12: Preacher Formation. How should this sermon form ME before I deliver it?'
    };

    // Update active state
    document.querySelectorAll('.module-item').forEach(item => {
        item.classList.toggle('active', item.dataset.module === moduleNum);
    });

    // Set input
    if (prompts[moduleNum]) {
        let prompt = prompts[moduleNum];
        if (state.sessionContext.scripture) {
            prompt += ` My scripture is ${state.sessionContext.scripture}.`;
        }
        messageInput.value = prompt;
        messageInput.focus();
        sendBtn.disabled = false;
    }
}

// Export for potential module use
window.SermonAI = {
    state,
    addMessage,
    startNewChat
};
