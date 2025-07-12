/**
 * ChatGPT Health Assistant - Frontend JavaScript
 */

class HealthChatbot {
    constructor() {
        this.conversationHistory = [];
        this.isTyping = false;
        this.totalTokens = 0;
        
        this.initializeElements();
        this.initializeEventListeners();
        this.checkServiceStatus();
    }
    
    initializeElements() {
        this.chatMessages = document.getElementById('chatMessages');
        this.messageInput = document.getElementById('messageInput');
        this.sendBtn = document.getElementById('sendBtn');
        this.chatForm = document.getElementById('chatForm');
        this.clearBtn = document.getElementById('clearChatBtn');
        this.statusBadge = document.getElementById('chatbotStatus');
        this.serviceAlert = document.getElementById('serviceAlert');
        this.tokenUsage = document.getElementById('tokenUsage');
        this.tokenCount = document.getElementById('tokenCount');
        this.healthTipBtns = document.querySelectorAll('.health-tip-btn');
    }
    
    initializeEventListeners() {
        // Chat form submission
        this.chatForm.addEventListener('submit', (e) => {
            e.preventDefault();
            this.sendMessage();
        });
        
        // Clear chat button
        this.clearBtn.addEventListener('click', () => {
            this.clearChat();
        });
        
        // Health tip buttons
        this.healthTipBtns.forEach(btn => {
            btn.addEventListener('click', () => {
                const category = btn.dataset.category;
                this.getHealthTips(category);
            });
        });
        
        // Enter key in input
        this.messageInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                this.sendMessage();
            }
        });
    }
    
    async checkServiceStatus() {
        try {
            const response = await fetch('/api/chatbot/status');
            const data = await response.json();
            
            if (data.available) {
                this.setServiceStatus('available', 'ChatGPT Ready');
                this.enableChat();
            } else {
                this.setServiceStatus('unavailable', 'Service Unavailable');
                this.disableChat();
                this.serviceAlert.classList.remove('d-none');
            }
        } catch (error) {
            console.error('Failed to check service status:', error);
            this.setServiceStatus('error', 'Connection Error');
            this.disableChat();
        }
    }
    
    setServiceStatus(status, message) {
        this.statusBadge.className = 'badge';
        
        switch (status) {
            case 'available':
                this.statusBadge.classList.add('bg-success');
                this.statusBadge.innerHTML = `<i class="fas fa-check-circle me-1"></i>${message}`;
                break;
            case 'unavailable':
                this.statusBadge.classList.add('bg-warning', 'text-dark');
                this.statusBadge.innerHTML = `<i class="fas fa-exclamation-triangle me-1"></i>${message}`;
                break;
            case 'error':
                this.statusBadge.classList.add('bg-danger');
                this.statusBadge.innerHTML = `<i class="fas fa-times-circle me-1"></i>${message}`;
                break;
        }
    }
    
    enableChat() {
        this.messageInput.disabled = false;
        this.sendBtn.disabled = false;
        this.messageInput.placeholder = "Ask me about your health, medications, or wellness tips...";
    }
    
    disableChat() {
        this.messageInput.disabled = true;
        this.sendBtn.disabled = true;
        this.messageInput.placeholder = "ChatGPT service is currently unavailable...";
    }
    
    async sendMessage() {
        const message = this.messageInput.value.trim();
        if (!message || this.isTyping) return;
        
        // Add user message to chat
        this.addUserMessage(message);
        this.messageInput.value = '';
        
        // Show typing indicator
        this.showTypingIndicator();
        
        try {
            const response = await fetch('/api/chatbot', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    message: message,
                    conversation_history: this.conversationHistory
                })
            });
            
            const data = await response.json();
            
            this.hideTypingIndicator();
            
            if (data.success) {
                this.addAssistantMessage(data.response);
                
                // Update conversation history
                this.conversationHistory.push({
                    user: message,
                    assistant: data.response
                });
                
                // Keep only last 10 exchanges
                if (this.conversationHistory.length > 10) {
                    this.conversationHistory = this.conversationHistory.slice(-10);
                }
                
                // Update token usage
                if (data.tokens_used) {
                    this.totalTokens += data.tokens_used;
                    this.updateTokenUsage();
                }
            } else {
                this.addErrorMessage(data.response || 'Sorry, I encountered an error. Please try again.');
            }
        } catch (error) {
            console.error('Chat error:', error);
            this.hideTypingIndicator();
            this.addErrorMessage('Failed to connect to the health assistant. Please check your connection and try again.');
        }
    }
    
    async getHealthTips(category) {
        // Disable tip buttons temporarily
        this.healthTipBtns.forEach(btn => btn.disabled = true);
        
        try {
            const response = await fetch(`/api/chatbot/tips/${category}`);
            const data = await response.json();
            
            if (data.success) {
                this.addSystemMessage(`Health Tips - ${category.charAt(0).toUpperCase() + category.slice(1)}`, data.response);
                
                if (data.tokens_used) {
                    this.totalTokens += data.tokens_used;
                    this.updateTokenUsage();
                }
            } else {
                this.addErrorMessage(`Failed to get ${category} tips: ${data.response}`);
            }
        } catch (error) {
            console.error('Health tips error:', error);
            this.addErrorMessage(`Failed to get ${category} tips. Please try again.`);
        } finally {
            // Re-enable tip buttons
            this.healthTipBtns.forEach(btn => btn.disabled = false);
        }
    }
    
    addUserMessage(message) {
        const messageDiv = document.createElement('div');
        messageDiv.className = 'message user-message';
        messageDiv.innerHTML = `
            <div class="d-flex align-items-start justify-content-end">
                <div class="message-content">
                    <div class="message-bubble">
                        <p class="mb-0">${this.escapeHtml(message)}</p>
                    </div>
                    <small class="text-muted mt-1 d-block text-end">${this.formatTime()}</small>
                </div>
                <div class="avatar bg-primary text-white ms-3">
                    <i class="fas fa-user"></i>
                </div>
            </div>
        `;
        
        this.chatMessages.appendChild(messageDiv);
        this.scrollToBottom();
    }
    
    addAssistantMessage(message) {
        const messageDiv = document.createElement('div');
        messageDiv.className = 'message assistant-message';
        messageDiv.innerHTML = `
            <div class="d-flex align-items-start">
                <div class="avatar bg-success text-white me-3">
                    <i class="fas fa-robot"></i>
                </div>
                <div class="message-content">
                    <div class="message-bubble">
                        ${this.formatMessage(message)}
                    </div>
                    <small class="text-muted mt-1 d-block">${this.formatTime()}</small>
                </div>
            </div>
        `;
        
        this.chatMessages.appendChild(messageDiv);
        this.scrollToBottom();
    }
    
    addSystemMessage(title, message) {
        const messageDiv = document.createElement('div');
        messageDiv.className = 'message assistant-message';
        messageDiv.innerHTML = `
            <div class="d-flex align-items-start">
                <div class="avatar bg-info text-white me-3">
                    <i class="fas fa-lightbulb"></i>
                </div>
                <div class="message-content">
                    <div class="message-bubble">
                        <h6 class="text-info mb-2"><i class="fas fa-stars me-1"></i>${title}</h6>
                        ${this.formatMessage(message)}
                    </div>
                    <small class="text-muted mt-1 d-block">${this.formatTime()}</small>
                </div>
            </div>
        `;
        
        this.chatMessages.appendChild(messageDiv);
        this.scrollToBottom();
    }
    
    addErrorMessage(message) {
        const messageDiv = document.createElement('div');
        messageDiv.className = 'message assistant-message';
        messageDiv.innerHTML = `
            <div class="d-flex align-items-start">
                <div class="avatar bg-danger text-white me-3">
                    <i class="fas fa-exclamation-triangle"></i>
                </div>
                <div class="message-content">
                    <div class="message-bubble border border-danger">
                        <p class="mb-0 text-danger">${this.escapeHtml(message)}</p>
                    </div>
                    <small class="text-muted mt-1 d-block">${this.formatTime()}</small>
                </div>
            </div>
        `;
        
        this.chatMessages.appendChild(messageDiv);
        this.scrollToBottom();
    }
    
    showTypingIndicator() {
        this.isTyping = true;
        this.sendBtn.disabled = true;
        
        const typingDiv = document.createElement('div');
        typingDiv.id = 'typingIndicator';
        typingDiv.className = 'message assistant-message';
        typingDiv.innerHTML = `
            <div class="d-flex align-items-start">
                <div class="avatar bg-secondary text-white me-3">
                    <i class="fas fa-robot"></i>
                </div>
                <div class="message-content">
                    <div class="message-bubble">
                        <div class="typing-indicator">
                            <span>Thinking</span>
                            <div class="dot"></div>
                            <div class="dot"></div>
                            <div class="dot"></div>
                        </div>
                    </div>
                </div>
            </div>
        `;
        
        this.chatMessages.appendChild(typingDiv);
        this.scrollToBottom();
    }
    
    hideTypingIndicator() {
        this.isTyping = false;
        this.sendBtn.disabled = false;
        
        const typingIndicator = document.getElementById('typingIndicator');
        if (typingIndicator) {
            typingIndicator.remove();
        }
    }
    
    clearChat() {
        if (confirm('Are you sure you want to clear the chat history?')) {
            // Remove all messages except the initial welcome message
            const messages = this.chatMessages.querySelectorAll('.message:not(:first-child)');
            messages.forEach(message => message.remove());
            
            // Clear conversation history
            this.conversationHistory = [];
            this.totalTokens = 0;
            this.updateTokenUsage();
        }
    }
    
    updateTokenUsage() {
        this.tokenCount.textContent = this.totalTokens;
        if (this.totalTokens > 0) {
            this.tokenUsage.classList.remove('d-none');
        }
    }
    
    formatMessage(message) {
        if (!message) return '<div>No response received</div>';
        
        // Convert markdown-like formatting to HTML
        let formatted = this.escapeHtml(message);
        
        // Convert line breaks
        formatted = formatted.replace(/\n/g, '<br>');
        
        // Convert lists
        formatted = formatted.replace(/^\s*[-•]\s*(.+)$/gm, '<li>$1</li>');
        formatted = formatted.replace(/(<li>.*<\/li>)/s, '<ul>$1</ul>');
        
        // Convert bold text
        formatted = formatted.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
        
        // Convert italic text
        formatted = formatted.replace(/\*(.*?)\*/g, '<em>$1</em>');
        
        // Ensure there's visible content
        if (formatted.trim() === '') {
            formatted = 'Response received but appears to be empty.';
        }
        
        return `<p>${formatted}</p>`;
    }
    
    formatTime() {
        return new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    }
    
    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
    
    scrollToBottom() {
        setTimeout(() => {
            this.chatMessages.scrollTop = this.chatMessages.scrollHeight;
        }, 100);
    }
}

// Initialize chatbot when page loads
document.addEventListener('DOMContentLoaded', () => {
    window.healthChatbot = new HealthChatbot();
    console.log('Health Assistant Chatbot initialized');
});