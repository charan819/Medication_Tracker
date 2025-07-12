"""
ChatGPT chatbot API resource for health management assistance.
"""
from flask import request
from flask_restful import Resource
from services.chatbot_service import chatbot_service
import logging

logger = logging.getLogger(__name__)

class ChatbotResource(Resource):
    """ChatGPT chatbot endpoint for health assistance."""
    
    def post(self):
        """
        Send a message to the ChatGPT health assistant
        ---
        parameters:
          - in: body
            name: chat_message
            schema:
              type: object
              required:
                - message
              properties:
                message:
                  type: string
                  description: User's message to the chatbot
                conversation_history:
                  type: array
                  description: Previous conversation history
                  items:
                    type: object
                    properties:
                      user:
                        type: string
                      assistant:
                        type: string
        responses:
          200:
            description: Chatbot response
            schema:
              type: object
              properties:
                success:
                  type: boolean
                response:
                  type: string
                tokens_used:
                  type: integer
                model:
                  type: string
                timestamp:
                  type: string
          400:
            description: Invalid input or missing message
          503:
            description: ChatGPT service unavailable
        """
        data = request.get_json()
        
        if not data or 'message' not in data:
            return {'error': 'Message is required'}, 400
        
        message = data['message'].strip()
        if not message:
            return {'error': 'Message cannot be empty'}, 400
        
        # Get conversation history if provided
        conversation_history = data.get('conversation_history', [])
        
        # Process the message with ChatGPT
        result = chatbot_service.chat(message, conversation_history)
        
        if result['success']:
            return result, 200
        else:
            return result, 503

class ChatbotHealthTipsResource(Resource):
    """Get health tips from ChatGPT for specific categories."""
    
    def get(self, category=None):
        """
        Get health tips for a specific category
        ---
        parameters:
          - in: path
            name: category
            type: string
            enum: [general, medication, exercise, nutrition, sleep, stress]
            description: Category of health tips
            required: false
        responses:
          200:
            description: Health tips response
          503:
            description: ChatGPT service unavailable
        """
        if not category:
            category = "general"
        
        valid_categories = ["general", "medication", "exercise", "nutrition", "sleep", "stress"]
        if category not in valid_categories:
            return {'error': f'Invalid category. Valid options: {", ".join(valid_categories)}'}, 400
        
        result = chatbot_service.get_health_tips(category)
        
        if result['success']:
            return result, 200
        else:
            return result, 503

class ChatbotStatusResource(Resource):
    """Check ChatGPT chatbot service status."""
    
    def get(self):
        """
        Get chatbot service status
        ---
        responses:
          200:
            description: Service status
            schema:
              type: object
              properties:
                available:
                  type: boolean
                service:
                  type: string
                message:
                  type: string
        """
        is_available = chatbot_service.is_available()
        
        return {
            'available': is_available,
            'service': 'ChatGPT Health Assistant',
            'model': 'gpt-4o' if is_available else None,
            'message': 'ChatGPT service is ready' if is_available else 'ChatGPT service unavailable - check API key configuration'
        }, 200