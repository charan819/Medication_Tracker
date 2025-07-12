/**
 * Floating Health Assistant Chat Widget
 */

class HealthChatWidget {
    constructor() {
        this.isOpen = false;
        this.isMinimized = false;
        this.conversationHistory = [];
        this.isTyping = false;
        
        this.createWidget();
        this.initializeEventListeners();
        this.checkServiceStatus();
    }
    
    createWidget() {
        // Create widget container
        const widget = document.createElement('div');
        widget.id = 'health-chat-widget';
        widget.className = 'health-chat-widget';
        
        widget.innerHTML = `
            <!-- Floating Button -->
            <div id="chat-toggle-btn" class="chat-toggle-btn" title="Health Assistant">
                <i class="fas fa-robot"></i>
                <span class="status-indicator" id="widget-status"></span>
            </div>
            
            <!-- Chat Window -->
            <div id="chat-window" class="chat-window d-none">
                <div class="chat-header">
                    <div class="d-flex align-items-center">
                        <div class="avatar-sm bg-primary text-white me-2">
                            <i class="fas fa-robot"></i>
                        </div>
                        <div>
                            <h6 class="mb-0">Health Assistant</h6>
                            <small class="text-muted" id="widget-service-status">Checking...</small>
                        </div>
                    </div>
                    <div class="chat-controls">
                        <button class="btn btn-sm btn-outline-light me-1" id="expand-chat-btn" title="Open Full Chat">
                            <i class="fas fa-expand"></i>
                        </button>
                        <button class="btn btn-sm btn-outline-light me-1" id="minimize-chat-btn" title="Minimize">
                            <i class="fas fa-minus"></i>
                        </button>
                        <button class="btn btn-sm btn-outline-light" id="close-chat-btn" title="Close">
                            <i class="fas fa-times"></i>
                        </button>
                    </div>
                </div>
                
                <div class="chat-body" id="widget-chat-messages">
                    <div class="welcome-message">
                        <div class="d-flex align-items-start">
                            <div class="avatar-xs bg-primary text-white me-2">
                                <i class="fas fa-robot"></i>
                            </div>
                            <div class="message-content">
                                <div class="message-bubble-sm bg-light">
                                    <p class="mb-1">Hi! I'm your health assistant.</p>
                                    <p class="mb-0 small text-muted">Ask me about medications, health tips, or wellness advice.</p>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                
                <div class="chat-footer">
                    <div class="quick-actions mb-2">
                        <button class="btn btn-outline-primary btn-xs me-1 quick-tip-btn" data-category="general">
                            General Tips
                        </button>
                        <button class="btn btn-outline-success btn-xs quick-tip-btn" data-category="medication">
                            Medication
                        </button>
                    </div>
                    
                    <form id="widget-chat-form" class="d-flex gap-2">
                        <input type="text" 
                               id="widget-message-input" 
                               class="form-control form-control-sm" 
                               placeholder="Ask about your health..." 
                               maxlength="200"
                               disabled>
                        <button type="submit" 
                                id="widget-send-btn" 
                                class="btn btn-primary btn-sm" 
                                disabled>
                            <i class="fas fa-paper-plane"></i>
                        </button>
                    </form>
                </div>
            </div>
        `;
        
        document.body.appendChild(widget);
        
        // Add styles
        this.addWidgetStyles();
    }
    
    addWidgetStyles() {
        const style = document.createElement('style');
        style.textContent = `
            .health-chat-widget {
                position: fixed;
                bottom: 20px;
                right: 20px;
                z-index: 1000;
                font-family: inherit;
            }
            
            .chat-toggle-btn {
                width: 60px;
                height: 60px;
                border-radius: 50%;
                background: linear-gradient(135deg, var(--bs-primary), var(--bs-success));
                color: white;
                border: none;
                cursor: pointer;
                display: flex;
                align-items: center;
                justify-content: center;
                box-shadow: 0 4px 12px rgba(0,0,0,0.15);
                transition: all 0.3s ease;
                position: relative;
            }
            
            .chat-toggle-btn:hover {
                transform: translateY(-2px);
                box-shadow: 0 6px 20px rgba(0,0,0,0.2);
            }
            
            .chat-toggle-btn i {
                font-size: 24px;
            }
            
            .status-indicator {
                position: absolute;
                top: 5px;
                right: 5px;
                width: 12px;
                height: 12px;
                border-radius: 50%;
                border: 2px solid white;
            }
            
            .status-indicator.available {
                background-color: #28a745;
            }
            
            .status-indicator.unavailable {
                background-color: #ffc107;
            }
            
            .status-indicator.error {
                background-color: #dc3545;
            }
            
            .chat-window {
                position: absolute;
                bottom: 80px;
                right: 0;
                width: 350px;
                height: 500px;
                background: white;
                border-radius: 12px;
                box-shadow: 0 8px 32px rgba(0,0,0,0.1);
                border: 1px solid var(--bs-border-color);
                display: flex;
                flex-direction: column;
                overflow: hidden;
                animation: slideUp 0.3s ease;
            }
            
            .chat-window.minimized {
                height: 60px;
            }
            
            .chat-window.minimized .chat-body,
            .chat-window.minimized .chat-footer {
                display: none;
            }
            
            @keyframes slideUp {
                from {
                    opacity: 0;
                    transform: translateY(20px);
                }
                to {
                    opacity: 1;
                    transform: translateY(0);
                }
            }
            
            .chat-header {
                background: var(--bs-primary);
                color: white;
                padding: 12px 16px;
                display: flex;
                align-items: center;
                justify-content: space-between;
                border-radius: 12px 12px 0 0;
            }
            
            .chat-controls {
                display: flex;
                gap: 4px;
            }
            
            .chat-controls .btn {
                padding: 4px 8px;
                border: 1px solid rgba(255,255,255,0.3);
            }
            
            .chat-body {
                flex: 1;
                padding: 16px;
                overflow-y: auto;
                background: #f8f9fa;
            }
            
            .chat-footer {
                padding: 12px 16px;
                border-top: 1px solid var(--bs-border-color);
                background: white;
            }
            
            .avatar-sm {
                width: 32px;
                height: 32px;
                border-radius: 50%;
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 14px;
                flex-shrink: 0;
            }
            
            .avatar-xs {
                width: 24px;
                height: 24px;
                border-radius: 50%;
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 12px;
                flex-shrink: 0;
            }
            
            .message-bubble-sm {
                padding: 8px 12px;
                border-radius: 12px;
                max-width: 100%;
                word-wrap: break-word;
                font-size: 14px;
                line-height: 1.4;
            }
            
            .user-message-widget .message-bubble-sm {
                background-color: var(--bs-primary);
                color: white;
                margin-left: auto;
            }
            
            .assistant-message-widget .message-bubble-sm {
                background-color: white;
                border: 1px solid var(--bs-border-color);
            }
            
            .quick-actions {
                display: flex;
                gap: 6px;
                flex-wrap: wrap;
            }
            
            .btn-xs {
                padding: 4px 8px;
                font-size: 11px;
                border-radius: 12px;
            }
            
            .welcome-message {
                margin-bottom: 16px;
            }
            
            .widget-message {
                margin-bottom: 12px;
            }
            
            .widget-typing-indicator {
                display: flex;
                align-items: center;
                gap: 8px;
                color: var(--bs-secondary);
                font-size: 12px;
            }
            
            .widget-typing-indicator .dot {
                width: 6px;
                height: 6px;
                border-radius: 50%;
                background-color: var(--bs-secondary);
                animation: typing 1.4s infinite ease-in-out;
            }
            
            .widget-typing-indicator .dot:nth-child(1) { animation-delay: -0.32s; }
            .widget-typing-indicator .dot:nth-child(2) { animation-delay: -0.16s; }
            .widget-typing-indicator .dot:nth-child(3) { animation-delay: 0s; }
            
            @media (max-width: 768px) {
                .health-chat-widget {
                    bottom: 15px;
                    right: 15px;
                }
                
                .chat-window {
                    width: calc(100vw - 30px);
                    max-width: 350px;
                }
                
                .chat-toggle-btn {
                    width: 50px;
                    height: 50px;
                }
                
                .chat-toggle-btn i {
                    font-size: 20px;
                }
            }
        `;
        
        document.head.appendChild(style);
    }
    
    initializeEventListeners() {
        const toggleBtn = document.getElementById('chat-toggle-btn');
        const chatWindow = document.getElementById('chat-window');
        const closeBtn = document.getElementById('close-chat-btn');
        const minimizeBtn = document.getElementById('minimize-chat-btn');
        const expandBtn = document.getElementById('expand-chat-btn');
        const chatForm = document.getElementById('widget-chat-form');
        const messageInput = document.getElementById('widget-message-input');
        const quickTipBtns = document.querySelectorAll('.quick-tip-btn');
        
        // Toggle chat window
        toggleBtn.addEventListener('click', () => {
            this.toggleChat();
        });
        
        // Close chat
        closeBtn.addEventListener('click', () => {
            this.closeChat();
        });
        
        // Minimize chat
        minimizeBtn.addEventListener('click', () => {
            this.minimizeChat();
        });
        
        // Expand to full page
        expandBtn.addEventListener('click', () => {
            window.location.href = '/chatbot';
        });
        
        // Send message
        chatForm.addEventListener('submit', (e) => {
            e.preventDefault();
            this.sendMessage();
        });
        
        // Quick tip buttons
        quickTipBtns.forEach(btn => {
            btn.addEventListener('click', () => {
                const category = btn.dataset.category;
                this.getHealthTips(category);
            });
        });
        
        // Enter key
        messageInput.addEventListener('keypress', (e) => {
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
            
            const statusIndicator = document.getElementById('widget-status');
            const serviceStatus = document.getElementById('widget-service-status');
            
            if (data.available) {
                statusIndicator.className = 'status-indicator available';
                serviceStatus.textContent = 'Ready to help';
                this.enableChat();
            } else {
                statusIndicator.className = 'status-indicator unavailable';
                serviceStatus.textContent = 'Service unavailable';
                this.disableChat();
            }
        } catch (error) {
            const statusIndicator = document.getElementById('widget-status');
            const serviceStatus = document.getElementById('widget-service-status');
            statusIndicator.className = 'status-indicator error';
            serviceStatus.textContent = 'Connection error';
            this.disableChat();
        }
    }
    
    toggleChat() {
        const chatWindow = document.getElementById('chat-window');
        
        if (this.isOpen) {
            this.closeChat();
        } else {
            chatWindow.classList.remove('d-none');
            this.isOpen = true;
            this.isMinimized = false;
            document.getElementById('widget-message-input').focus();
        }
    }
    
    closeChat() {
        const chatWindow = document.getElementById('chat-window');
        chatWindow.classList.add('d-none');
        this.isOpen = false;
        this.isMinimized = false;
    }
    
    minimizeChat() {
        const chatWindow = document.getElementById('chat-window');
        if (this.isMinimized) {
            chatWindow.classList.remove('minimized');
            this.isMinimized = false;
        } else {
            chatWindow.classList.add('minimized');
            this.isMinimized = true;
        }
    }
    
    enableChat() {
        document.getElementById('widget-message-input').disabled = false;
        document.getElementById('widget-send-btn').disabled = false;
    }
    
    disableChat() {
        document.getElementById('widget-message-input').disabled = true;
        document.getElementById('widget-send-btn').disabled = true;
    }
    
    async sendMessage() {
        const messageInput = document.getElementById('widget-message-input');
        const message = messageInput.value.trim();
        
        if (!message || this.isTyping) return;
        
        this.addUserMessage(message);
        messageInput.value = '';
        
        this.showTypingIndicator();
        
        try {
            const response = await fetch('/api/chatbot', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    message: message,
                    conversation_history: this.conversationHistory.slice(-5) // Keep last 5 exchanges
                })
            });
            
            const data = await response.json();
            this.hideTypingIndicator();
            
            if (data.success) {
                this.addAssistantMessage(data.response);
                
                this.conversationHistory.push({
                    user: message,
                    assistant: data.response
                });
                
                if (this.conversationHistory.length > 10) {
                    this.conversationHistory = this.conversationHistory.slice(-10);
                }
            } else {
                this.addErrorMessage(data.response || 'Sorry, I encountered an error.');
            }
        } catch (error) {
            this.hideTypingIndicator();
            this.addErrorMessage('Failed to connect. Please try again.');
        }
    }
    
    async getHealthTips(category) {
        try {
            const response = await fetch(`/api/chatbot/tips/${category}`);
            const data = await response.json();
            
            if (data.success) {
                this.addSystemMessage(`${category.charAt(0).toUpperCase() + category.slice(1)} Tips`, data.response);
            } else {
                this.addErrorMessage(`Failed to get ${category} tips.`);
            }
        } catch (error) {
            this.addErrorMessage(`Failed to get ${category} tips.`);
        }
    }
    
    addUserMessage(message) {
        const messagesContainer = document.getElementById('widget-chat-messages');
        const messageDiv = document.createElement('div');
        messageDiv.className = 'widget-message user-message-widget';
        messageDiv.innerHTML = `
            <div class="d-flex align-items-start justify-content-end">
                <div class="message-content">
                    <div class="message-bubble-sm">
                        <p class="mb-0">${this.escapeHtml(message)}</p>
                    </div>
                </div>
                <div class="avatar-xs bg-primary text-white ms-2">
                    <i class="fas fa-user"></i>
                </div>
            </div>
        `;
        
        messagesContainer.appendChild(messageDiv);
        this.scrollToBottom();
    }
    
    addAssistantMessage(message) {
        const messagesContainer = document.getElementById('widget-chat-messages');
        const messageDiv = document.createElement('div');
        messageDiv.className = 'widget-message assistant-message-widget';
        messageDiv.innerHTML = `
            <div class="d-flex align-items-start">
                <div class="avatar-xs bg-success text-white me-2">
                    <i class="fas fa-robot"></i>
                </div>
                <div class="message-content">
                    <div class="message-bubble-sm">
                        ${this.formatMessage(message)}
                    </div>
                </div>
            </div>
        `;
        
        messagesContainer.appendChild(messageDiv);
        this.scrollToBottom();
    }
    
    addSystemMessage(title, message) {
        const messagesContainer = document.getElementById('widget-chat-messages');
        const messageDiv = document.createElement('div');
        messageDiv.className = 'widget-message assistant-message-widget';
        messageDiv.innerHTML = `
            <div class="d-flex align-items-start">
                <div class="avatar-xs bg-info text-white me-2">
                    <i class="fas fa-lightbulb"></i>
                </div>
                <div class="message-content">
                    <div class="message-bubble-sm">
                        <h6 class="text-info mb-1 small">${title}</h6>
                        ${this.formatMessage(message)}
                    </div>
                </div>
            </div>
        `;
        
        messagesContainer.appendChild(messageDiv);
        this.scrollToBottom();
    }
    
    addErrorMessage(message) {
        const messagesContainer = document.getElementById('widget-chat-messages');
        const messageDiv = document.createElement('div');
        messageDiv.className = 'widget-message assistant-message-widget';
        messageDiv.innerHTML = `
            <div class="d-flex align-items-start">
                <div class="avatar-xs bg-danger text-white me-2">
                    <i class="fas fa-exclamation-triangle"></i>
                </div>
                <div class="message-content">
                    <div class="message-bubble-sm border border-danger">
                        <p class="mb-0 text-danger small">${this.escapeHtml(message)}</p>
                    </div>
                </div>
            </div>
        `;
        
        messagesContainer.appendChild(messageDiv);
        this.scrollToBottom();
    }
    
    showTypingIndicator() {
        this.isTyping = true;
        document.getElementById('widget-send-btn').disabled = true;
        
        const messagesContainer = document.getElementById('widget-chat-messages');
        const typingDiv = document.createElement('div');
        typingDiv.id = 'widget-typing-indicator';
        typingDiv.className = 'widget-message assistant-message-widget';
        typingDiv.innerHTML = `
            <div class="d-flex align-items-start">
                <div class="avatar-xs bg-secondary text-white me-2">
                    <i class="fas fa-robot"></i>
                </div>
                <div class="message-content">
                    <div class="message-bubble-sm">
                        <div class="widget-typing-indicator">
                            <span>Thinking</span>
                            <div class="dot"></div>
                            <div class="dot"></div>
                            <div class="dot"></div>
                        </div>
                    </div>
                </div>
            </div>
        `;
        
        messagesContainer.appendChild(typingDiv);
        this.scrollToBottom();
    }
    
    hideTypingIndicator() {
        this.isTyping = false;
        document.getElementById('widget-send-btn').disabled = false;
        
        const typingIndicator = document.getElementById('widget-typing-indicator');
        if (typingIndicator) {
            typingIndicator.remove();
        }
    }
    
    formatMessage(message) {
        if (!message) return '<div class="small">No response</div>';
        
        let formatted = this.escapeHtml(message);
        formatted = formatted.replace(/\n/g, '<br>');
        formatted = formatted.replace(/^\s*[-•]\s*(.+)$/gm, '<li class="small">$1</li>');
        formatted = formatted.replace(/(<li.*<\/li>)/s, '<ul class="small mb-0">$1</ul>');
        formatted = formatted.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
        formatted = formatted.replace(/\*(.*?)\*/g, '<em>$1</em>');
        
        // Ensure there's visible content
        if (formatted.trim() === '') {
            formatted = 'Response received but appears to be empty.';
        }
        
        return `<p class="small mb-0">${formatted}</p>`;
    }
    
    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
    
    scrollToBottom() {
        const messagesContainer = document.getElementById('widget-chat-messages');
        setTimeout(() => {
            messagesContainer.scrollTop = messagesContainer.scrollHeight;
        }, 100);
    }
}

// Initialize widget when page loads
document.addEventListener('DOMContentLoaded', () => {
    // Only initialize if we're not on the dedicated chatbot page
    if (window.location.pathname !== '/chatbot') {
        window.healthChatWidget = new HealthChatWidget();
        console.log('Health Chat Widget initialized');
    }
});