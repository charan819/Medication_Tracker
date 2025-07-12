"""
API resources for notification management and push notifications.
"""
from flask import request, jsonify
from flask_restful import Resource
from datetime import datetime
import logging

from services.notification_service import notification_service

logger = logging.getLogger(__name__)

class NotificationListResource(Resource):
    def get(self):
        """
        Get pending notifications for the user
        ---
        responses:
          200:
            description: List of pending notifications
        """
        try:
            notifications = notification_service.get_pending_notifications()
            return notifications, 200
        except Exception as e:
            logger.error(f"Error retrieving notifications: {str(e)}")
            return {'error': 'Failed to retrieve notifications'}, 500

class NotificationResource(Resource):
    def put(self, notification_id):
        """
        Mark notification as read
        ---
        parameters:
          - in: path
            name: notification_id
            type: string
            required: true
        responses:
          200:
            description: Notification marked as read
          404:
            description: Notification not found
        """
        try:
            success = notification_service.mark_notification_read(notification_id)
            if success:
                return {'message': 'Notification marked as read'}, 200
            else:
                return {'error': 'Notification not found'}, 404
        except Exception as e:
            logger.error(f"Error marking notification as read: {str(e)}")
            return {'error': 'Failed to update notification'}, 500

class NotificationTestResource(Resource):
    def post(self):
        """
        Send a test notification
        ---
        responses:
          200:
            description: Test notification sent
        """
        try:
            success = notification_service.send_test_notification()
            if success:
                return {'message': 'Test notification sent successfully'}, 200
            else:
                return {'error': 'Failed to send test notification'}, 500
        except Exception as e:
            logger.error(f"Error sending test notification: {str(e)}")
            return {'error': 'Failed to send test notification'}, 500

class NotificationSettingsResource(Resource):
    def get(self):
        """
        Get notification service status and settings
        ---
        responses:
          200:
            description: Notification service status
        """
        try:
            status = {
                'email_enabled': notification_service.email_service.is_enabled(),
                'push_enabled': True,  # Browser push is always available
                'active_reminders': len(notification_service.active_timers),
                'sendgrid_configured': notification_service.email_service.is_enabled()
            }
            return status, 200
        except Exception as e:
            logger.error(f"Error getting notification settings: {str(e)}")
            return {'error': 'Failed to get notification settings'}, 500