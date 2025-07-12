"""
Push notification service for browser notifications and reminder management.
"""
import os
import logging
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
from threading import Timer
import json

from database import db
from models import Reminder
from services.email_service import EmailService

logger = logging.getLogger(__name__)

class NotificationService:
    """Service for managing push notifications and reminder alerts."""
    
    def __init__(self):
        self.email_service = EmailService()
        self.active_timers = {}  # Store active reminder timers
        logger.info("Notification service initialized")
    
    def schedule_reminder(self, reminder_id: int) -> bool:
        """
        Schedule a reminder for future notification.
        
        Args:
            reminder_id: ID of the reminder to schedule
            
        Returns:
            bool: True if successfully scheduled, False otherwise
        """
        try:
            reminder = db.session.get(Reminder, reminder_id)
            if not reminder or not reminder.is_active:
                logger.warning(f"Reminder {reminder_id} not found or inactive")
                return False
            
            # Calculate time until reminder
            now = datetime.utcnow()
            time_until_reminder = (reminder.reminder_time - now).total_seconds()
            
            if time_until_reminder <= 0:
                # Reminder is overdue, send immediately
                self.send_reminder_notification(reminder_id)
                return True
            
            # Schedule the reminder
            timer = Timer(time_until_reminder, self.send_reminder_notification, args=[reminder_id])
            timer.start()
            
            # Store timer reference
            self.active_timers[reminder_id] = timer
            
            logger.info(f"Reminder {reminder_id} scheduled for {reminder.reminder_time}")
            return True
            
        except Exception as e:
            logger.error(f"Error scheduling reminder {reminder_id}: {str(e)}")
            return False
    
    def cancel_reminder(self, reminder_id: int) -> bool:
        """Cancel a scheduled reminder."""
        try:
            if reminder_id in self.active_timers:
                self.active_timers[reminder_id].cancel()
                del self.active_timers[reminder_id]
                logger.info(f"Cancelled reminder {reminder_id}")
                return True
            return False
        except Exception as e:
            logger.error(f"Error cancelling reminder {reminder_id}: {str(e)}")
            return False
    
    def send_reminder_notification(self, reminder_id: int) -> bool:
        """
        Send notification for a specific reminder.
        
        Args:
            reminder_id: ID of the reminder to send
            
        Returns:
            bool: True if notification sent successfully
        """
        try:
            reminder = db.session.get(Reminder, reminder_id)
            if not reminder:
                logger.warning(f"Reminder {reminder_id} not found")
                return False
            
            # Prepare reminder data
            reminder_data = {
                'id': reminder.id,
                'reminder_type': reminder.reminder_type,
                'title': reminder.title,
                'message': reminder.message,
                'reminder_time': reminder.reminder_time,
                'target_id': reminder.target_id
            }
            
            # Send email notification if configured
            email_sent = False
            user_email = os.environ.get('USER_EMAIL')  # Get user email from environment
            if user_email and self.email_service.is_enabled():
                email_sent = self.email_service.send_reminder_email(user_email, reminder_data)
            
            # Store notification in database for web push
            self.store_notification(reminder_data)
            
            # Handle recurring reminders
            if reminder.repeat_interval and reminder.repeat_interval != 'once':
                self.schedule_recurring_reminder(reminder)
            
            logger.info(f"Notification sent for reminder {reminder_id} (email: {email_sent})")
            return True
            
        except Exception as e:
            logger.error(f"Error sending notification for reminder {reminder_id}: {str(e)}")
            return False
    
    def store_notification(self, reminder_data: Dict[str, Any]) -> bool:
        """Store notification data for web push retrieval."""
        try:
            # Create notifications table entry or use a simple file-based approach
            notification_file = 'data/notifications.json'
            
            # Ensure directory exists
            os.makedirs(os.path.dirname(notification_file), exist_ok=True)
            
            # Load existing notifications
            notifications = []
            if os.path.exists(notification_file):
                try:
                    with open(notification_file, 'r') as f:
                        notifications = json.load(f)
                except:
                    notifications = []
            
            # Add new notification
            notification = {
                'id': f"reminder_{reminder_data['id']}_{int(datetime.now().timestamp())}",
                'type': 'reminder',
                'title': reminder_data['title'],
                'body': reminder_data['message'],
                'data': reminder_data,
                'timestamp': datetime.now().isoformat(),
                'read': False
            }
            
            notifications.append(notification)
            
            # Keep only last 100 notifications
            notifications = notifications[-100:]
            
            # Save back to file
            with open(notification_file, 'w') as f:
                json.dump(notifications, f, indent=2, default=str)
            
            logger.info(f"Notification stored for web push")
            return True
            
        except Exception as e:
            logger.error(f"Error storing notification: {str(e)}")
            return False
    
    def get_pending_notifications(self) -> List[Dict[str, Any]]:
        """Get all pending notifications for web push."""
        try:
            notification_file = 'data/notifications.json'
            if not os.path.exists(notification_file):
                return []
            
            with open(notification_file, 'r') as f:
                notifications = json.load(f)
            
            # Return unread notifications
            return [n for n in notifications if not n.get('read', False)]
            
        except Exception as e:
            logger.error(f"Error retrieving notifications: {str(e)}")
            return []
    
    def mark_notification_read(self, notification_id: str) -> bool:
        """Mark a notification as read."""
        try:
            notification_file = 'data/notifications.json'
            if not os.path.exists(notification_file):
                return False
            
            with open(notification_file, 'r') as f:
                notifications = json.load(f)
            
            # Find and mark notification as read
            for notification in notifications:
                if notification['id'] == notification_id:
                    notification['read'] = True
                    break
            
            # Save back to file
            with open(notification_file, 'w') as f:
                json.dump(notifications, f, indent=2, default=str)
            
            return True
            
        except Exception as e:
            logger.error(f"Error marking notification as read: {str(e)}")
            return False
    
    def schedule_recurring_reminder(self, reminder: Reminder) -> bool:
        """Schedule the next occurrence of a recurring reminder."""
        try:
            if reminder.repeat_interval == 'daily':
                next_time = reminder.reminder_time + timedelta(days=1)
            elif reminder.repeat_interval == 'weekly':
                next_time = reminder.reminder_time + timedelta(weeks=1)
            elif reminder.repeat_interval == 'monthly':
                next_time = reminder.reminder_time + timedelta(days=30)  # Approximate
            else:
                return False
            
            # Update reminder time
            reminder.reminder_time = next_time
            db.session.commit()
            
            # Schedule next occurrence
            return self.schedule_reminder(reminder.id)
            
        except Exception as e:
            logger.error(f"Error scheduling recurring reminder: {str(e)}")
            return False
    
    def initialize_all_reminders(self) -> int:
        """Initialize all active reminders on application startup."""
        try:
            now = datetime.utcnow()
            active_reminders = db.session.query(Reminder).filter(
                Reminder.is_active == True,
                Reminder.reminder_time > now
            ).all()
            
            scheduled_count = 0
            for reminder in active_reminders:
                if self.schedule_reminder(reminder.id):
                    scheduled_count += 1
            
            logger.info(f"Initialized {scheduled_count} active reminders")
            return scheduled_count
            
        except Exception as e:
            logger.error(f"Error initializing reminders: {str(e)}")
            return 0
    
    def send_test_notification(self) -> bool:
        """Send a test notification to verify the service is working."""
        test_reminder_data = {
            'id': 'test',
            'reminder_type': 'health_check',
            'title': 'Test Notification',
            'message': 'This is a test notification from your Health Management System.',
            'reminder_time': datetime.now(),
            'target_id': None
        }
        
        # Store test notification
        self.store_notification(test_reminder_data)
        
        # Send test email if configured
        user_email = os.environ.get('USER_EMAIL')
        if user_email and self.email_service.is_enabled():
            self.email_service.send_reminder_email(user_email, test_reminder_data)
        
        logger.info("Test notification sent")
        return True

# Global notification service instance
notification_service = NotificationService()