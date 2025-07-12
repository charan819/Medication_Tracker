/**
 * Push notification system for health management reminders
 */

class NotificationManager {
    constructor() {
        this.permission = 'default';
        this.notificationQueue = [];
        this.checkInterval = null;
        this.init();
    }

    async init() {
        // Check for notification support
        if (!('Notification' in window)) {
            console.warn('This browser does not support notifications');
            return;
        }

        // Get current permission status
        this.permission = Notification.permission;
        
        // Request permission if not already granted
        if (this.permission === 'default') {
            await this.requestPermission();
        }

        // Start checking for new notifications
        this.startNotificationPolling();
        
        // Check for pending notifications on load
        this.checkPendingNotifications();
        
        console.log('Notification manager initialized');
    }

    async requestPermission() {
        try {
            this.permission = await Notification.requestPermission();
            
            if (this.permission === 'granted') {
                this.showWelcomeNotification();
            } else if (this.permission === 'denied') {
                console.warn('Notification permission denied');
                this.showPermissionDeniedMessage();
            }
        } catch (error) {
            console.error('Error requesting notification permission:', error);
        }
    }

    showWelcomeNotification() {
        const notification = new Notification('Health Management System', {
            body: 'Notifications are now enabled! You\'ll receive reminders for medications and appointments.',
            icon: '/static/img/health-icon.png',
            tag: 'welcome'
        });

        // Auto-close after 5 seconds
        setTimeout(() => {
            notification.close();
        }, 5000);
    }

    showPermissionDeniedMessage() {
        // Show in-page message about enabling notifications
        const message = document.createElement('div');
        message.className = 'alert alert-warning alert-dismissible fade show';
        message.innerHTML = `
            <strong>Notifications Disabled:</strong> To receive health reminders, please enable notifications in your browser settings.
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;
        
        const container = document.querySelector('.container');
        if (container) {
            container.insertBefore(message, container.firstChild);
        }
    }

    async showNotification(title, options = {}) {
        if (this.permission !== 'granted') {
            console.warn('Cannot show notification: permission not granted');
            return;
        }

        try {
            const defaultOptions = {
                icon: '/static/img/health-icon.png',
                badge: '/static/img/health-badge.png',
                vibrate: [200, 100, 200],
                requireInteraction: true,
                actions: [
                    {
                        action: 'view',
                        title: 'View Details'
                    },
                    {
                        action: 'dismiss',
                        title: 'Dismiss'
                    }
                ]
            };

            const finalOptions = { ...defaultOptions, ...options };
            const notification = new Notification(title, finalOptions);

            // Handle notification clicks
            notification.onclick = () => {
                window.focus();
                notification.close();
                
                // Navigate to relevant page based on notification data
                if (options.data && options.data.reminder_type) {
                    this.handleNotificationClick(options.data);
                }
            };

            // Auto-close after 10 seconds if not persistent
            if (!finalOptions.requireInteraction) {
                setTimeout(() => {
                    notification.close();
                }, 10000);
            }

            return notification;
        } catch (error) {
            console.error('Error showing notification:', error);
        }
    }

    handleNotificationClick(data) {
        const reminderType = data.reminder_type;
        const targetId = data.target_id;

        switch (reminderType) {
            case 'medication':
                if (targetId) {
                    window.location.href = `/medications/${targetId}`;
                } else {
                    window.location.href = '/medications';
                }
                break;
            case 'appointment':
                window.location.href = '/appointments';
                break;
            case 'health_check':
                window.location.href = '/health-metrics';
                break;
            default:
                window.location.href = '/reminders';
        }
    }

    startNotificationPolling() {
        // Check for new notifications every 30 seconds
        this.checkInterval = setInterval(() => {
            this.checkPendingNotifications();
        }, 30000);
    }

    stopNotificationPolling() {
        if (this.checkInterval) {
            clearInterval(this.checkInterval);
            this.checkInterval = null;
        }
    }

    async checkPendingNotifications() {
        try {
            const response = await fetch('/api/notifications');
            if (response.ok) {
                const notifications = await response.json();
                
                for (const notification of notifications) {
                    if (!this.isNotificationShown(notification.id)) {
                        await this.processNotification(notification);
                        this.markNotificationShown(notification.id);
                    }
                }
            }
        } catch (error) {
            console.error('Error checking notifications:', error);
        }
    }

    async processNotification(notification) {
        const { title, body, data } = notification;
        
        // Show browser notification
        await this.showNotification(title, {
            body: body,
            data: data,
            tag: notification.id
        });

        // Mark as read on server
        await this.markNotificationRead(notification.id);
        
        // Show in-page notification as well
        this.showInPageNotification(notification);
    }

    showInPageNotification(notification) {
        // Create toast notification
        const toast = document.createElement('div');
        toast.className = 'toast show position-fixed bottom-0 end-0 m-3';
        toast.style.zIndex = '9999';
        
        const iconMap = {
            'medication': '💊',
            'appointment': '🏥',
            'health_check': '📊'
        };
        
        const icon = iconMap[notification.data?.reminder_type] || '🔔';
        
        toast.innerHTML = `
            <div class="toast-header">
                <span class="me-2">${icon}</span>
                <strong class="me-auto">${notification.title}</strong>
                <small>Just now</small>
                <button type="button" class="btn-close" data-bs-dismiss="toast"></button>
            </div>
            <div class="toast-body">
                ${notification.body}
                <div class="mt-2">
                    <button class="btn btn-primary btn-sm me-2" onclick="notificationManager.handleNotificationClick(${JSON.stringify(notification.data).replace(/"/g, '&quot;')})">
                        View Details
                    </button>
                </div>
            </div>
        `;

        document.body.appendChild(toast);

        // Auto-remove after 8 seconds
        setTimeout(() => {
            if (toast.parentNode) {
                toast.remove();
            }
        }, 8000);
    }

    async markNotificationRead(notificationId) {
        try {
            await fetch(`/api/notifications/${notificationId}`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json'
                }
            });
        } catch (error) {
            console.error('Error marking notification as read:', error);
        }
    }

    isNotificationShown(notificationId) {
        // Check localStorage to avoid showing duplicate notifications
        const shownNotifications = JSON.parse(localStorage.getItem('shownNotifications') || '[]');
        return shownNotifications.includes(notificationId);
    }

    markNotificationShown(notificationId) {
        const shownNotifications = JSON.parse(localStorage.getItem('shownNotifications') || '[]');
        shownNotifications.push(notificationId);
        
        // Keep only last 100 notification IDs
        const recentNotifications = shownNotifications.slice(-100);
        localStorage.setItem('shownNotifications', JSON.stringify(recentNotifications));
    }

    async sendTestNotification() {
        try {
            const response = await fetch('/api/notifications/test', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                }
            });

            if (response.ok) {
                console.log('Test notification sent');
                // Check for the test notification immediately
                setTimeout(() => {
                    this.checkPendingNotifications();
                }, 1000);
            } else {
                console.error('Failed to send test notification');
            }
        } catch (error) {
            console.error('Error sending test notification:', error);
        }
    }

    async getNotificationStatus() {
        try {
            const response = await fetch('/api/notifications/settings');
            if (response.ok) {
                return await response.json();
            }
        } catch (error) {
            console.error('Error getting notification status:', error);
        }
        return null;
    }

    destroy() {
        this.stopNotificationPolling();
    }
}

// Initialize notification manager when DOM is loaded
let notificationManager;

document.addEventListener('DOMContentLoaded', () => {
    notificationManager = new NotificationManager();
    
    // Add notification status to UI if there's a settings area
    setTimeout(() => {
        addNotificationControls();
    }, 1000);
});

async function addNotificationControls() {
    // Add notification controls to the page
    const navbarNav = document.querySelector('.navbar-nav');
    if (navbarNav) {
        const notificationItem = document.createElement('li');
        notificationItem.className = 'nav-item dropdown';
        
        const status = await notificationManager.getNotificationStatus();
        const emailStatus = status?.email_enabled ? '✅' : '❌';
        const pushStatus = notificationManager.permission === 'granted' ? '✅' : '❌';
        
        notificationItem.innerHTML = `
            <a class="nav-link dropdown-toggle" href="#" role="button" data-bs-toggle="dropdown">
                🔔 Notifications
            </a>
            <ul class="dropdown-menu">
                <li><h6 class="dropdown-header">Notification Status</h6></li>
                <li><span class="dropdown-item-text">Push: ${pushStatus}</span></li>
                <li><span class="dropdown-item-text">Email: ${emailStatus}</span></li>
                <li><hr class="dropdown-divider"></li>
                <li><a class="dropdown-item" href="#" onclick="notificationManager.sendTestNotification()">Send Test</a></li>
                <li><a class="dropdown-item" href="#" onclick="notificationManager.requestPermission()">Enable Push</a></li>
            </ul>
        `;
        
        navbarNav.appendChild(notificationItem);
    }
}

// Cleanup on page unload
window.addEventListener('beforeunload', () => {
    if (notificationManager) {
        notificationManager.destroy();
    }
});