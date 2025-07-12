"""
Email notification service using SendGrid for health management reminders.
"""
import os
import logging
from datetime import datetime
from typing import Optional, Dict, Any
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Email, To, Content

logger = logging.getLogger(__name__)

class EmailService:
    """Service for sending email notifications via SendGrid."""
    
    def __init__(self):
        self.api_key = os.environ.get('SENDGRID_API_KEY')
        self.from_email = os.environ.get('FROM_EMAIL', 'noreply@healthtracker.com')
        self.sg = None
        
        if self.api_key:
            self.sg = SendGridAPIClient(self.api_key)
            logger.info("SendGrid email service initialized successfully")
        else:
            logger.warning("SendGrid API key not found. Email notifications disabled.")
    
    def is_enabled(self) -> bool:
        """Check if email service is properly configured."""
        return self.sg is not None
    
    def send_reminder_email(self, 
                          to_email: str, 
                          reminder_data: Dict[str, Any]) -> bool:
        """
        Send a reminder email to the user.
        
        Args:
            to_email: Recipient email address
            reminder_data: Dictionary containing reminder information
            
        Returns:
            bool: True if email sent successfully, False otherwise
        """
        if not self.is_enabled():
            logger.warning("Email service not enabled. Cannot send reminder email.")
            return False
        
        try:
            subject = self._get_email_subject(reminder_data)
            html_content = self._get_email_html_content(reminder_data)
            text_content = self._get_email_text_content(reminder_data)
            
            message = Mail(
                from_email=Email(self.from_email),
                to_emails=To(to_email),
                subject=subject
            )
            
            # Add both HTML and text content
            message.content = [
                Content("text/plain", text_content),
                Content("text/html", html_content)
            ]
            
            response = self.sg.send(message)
            
            if response.status_code in [200, 202]:
                logger.info(f"Reminder email sent successfully to {to_email}")
                return True
            else:
                logger.error(f"Failed to send email. Status code: {response.status_code}")
                return False
                
        except Exception as e:
            logger.error(f"Error sending reminder email: {str(e)}")
            return False
    
    def _get_email_subject(self, reminder_data: Dict[str, Any]) -> str:
        """Generate email subject based on reminder type."""
        reminder_type = reminder_data.get('reminder_type', 'general')
        title = reminder_data.get('title', 'Health Reminder')
        
        if reminder_type == 'medication':
            return f"💊 Medication Reminder: {title}"
        elif reminder_type == 'appointment':
            return f"🏥 Appointment Reminder: {title}"
        elif reminder_type == 'health_check':
            return f"📊 Health Check Reminder: {title}"
        else:
            return f"🔔 Health Reminder: {title}"
    
    def _get_email_html_content(self, reminder_data: Dict[str, Any]) -> str:
        """Generate HTML email content."""
        reminder_type = reminder_data.get('reminder_type', 'general')
        title = reminder_data.get('title', 'Health Reminder')
        message = reminder_data.get('message', '')
        reminder_time = reminder_data.get('reminder_time', datetime.now())
        
        # Format reminder time
        if isinstance(reminder_time, str):
            try:
                reminder_time = datetime.fromisoformat(reminder_time.replace('Z', '+00:00'))
            except:
                reminder_time = datetime.now()
        
        formatted_time = reminder_time.strftime("%B %d, %Y at %I:%M %p")
        
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <title>Health Reminder</title>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background: #007bff; color: white; padding: 20px; text-align: center; border-radius: 8px 8px 0 0; }}
                .content {{ background: #f8f9fa; padding: 20px; border-radius: 0 0 8px 8px; }}
                .reminder-card {{ background: white; padding: 20px; border-radius: 8px; border-left: 4px solid #007bff; margin: 20px 0; }}
                .footer {{ text-align: center; margin-top: 20px; color: #666; font-size: 12px; }}
                .button {{ background: #007bff; color: white; padding: 12px 24px; text-decoration: none; border-radius: 4px; display: inline-block; margin: 10px 0; }}
                .icon {{ font-size: 24px; margin-right: 10px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>🏥 Health Management System</h1>
                    <p>Your Health Reminder</p>
                </div>
                <div class="content">
                    <div class="reminder-card">
                        <h2>{self._get_type_icon(reminder_type)} {title}</h2>
                        <p><strong>Scheduled for:</strong> {formatted_time}</p>
                        <p><strong>Message:</strong> {message}</p>
                        <p><strong>Type:</strong> {reminder_type.replace('_', ' ').title()}</p>
                    </div>
                    <div style="text-align: center;">
                        <a href="#" class="button">View in Health App</a>
                    </div>
                </div>
                <div class="footer">
                    <p>This is an automated reminder from your Health Management System.</p>
                    <p>Please do not reply to this email.</p>
                </div>
            </div>
        </body>
        </html>
        """
        return html_content
    
    def _get_email_text_content(self, reminder_data: Dict[str, Any]) -> str:
        """Generate plain text email content."""
        reminder_type = reminder_data.get('reminder_type', 'general')
        title = reminder_data.get('title', 'Health Reminder')
        message = reminder_data.get('message', '')
        reminder_time = reminder_data.get('reminder_time', datetime.now())
        
        # Format reminder time
        if isinstance(reminder_time, str):
            try:
                reminder_time = datetime.fromisoformat(reminder_time.replace('Z', '+00:00'))
            except:
                reminder_time = datetime.now()
        
        formatted_time = reminder_time.strftime("%B %d, %Y at %I:%M %p")
        
        text_content = f"""
Health Management System - Reminder

{title}

Scheduled for: {formatted_time}
Type: {reminder_type.replace('_', ' ').title()}

Message: {message}

This is an automated reminder from your Health Management System.
Please check your health app for more details.

---
Health Management System
        """
        return text_content.strip()
    
    def _get_type_icon(self, reminder_type: str) -> str:
        """Get appropriate icon for reminder type."""
        icons = {
            'medication': '💊',
            'appointment': '🏥',
            'health_check': '📊'
        }
        return icons.get(reminder_type, '🔔')
    
    def send_test_email(self, to_email: str) -> bool:
        """Send a test email to verify email service configuration."""
        if not self.is_enabled():
            return False
        
        test_reminder = {
            'reminder_type': 'medication',
            'title': 'Test Reminder',
            'message': 'This is a test email from your Health Management System.',
            'reminder_time': datetime.now()
        }
        
        return self.send_reminder_email(to_email, test_reminder)