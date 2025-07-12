"""
ChatGPT-powered chatbot service for health management assistance.
"""
import os
import logging
from typing import Dict, Any, Optional, List
from datetime import datetime

try:
    import openai
    OPENAI_AVAILABLE = True
except ImportError:
    openai = None
    OPENAI_AVAILABLE = False

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

class ChatbotService:
    """ChatGPT-powered chatbot for health management assistance."""

    def __init__(self):
        """Initialize the chatbot service with OpenAI API."""
        self.is_initialized = False
        self.client = None

        if not OPENAI_AVAILABLE:
            logger.warning("OpenAI library not available. Install with: pip install openai")
            return

        api_key = os.environ.get('OPENAI_API_KEY')
        if not api_key:
            logger.warning("OpenAI API key not found. Chatbot functionality disabled.")
            return

        try:
            openai.api_key = api_key
            self.client = openai
            self.is_initialized = True
            logger.info("ChatGPT chatbot service initialized successfully.")
        except Exception as e:
            logger.error(f"Failed to initialize OpenAI client: {e}")

    def get_health_context(self) -> str:
        """Get system context for health-related conversations."""
        return f"""You are a helpful health management assistant integrated into a health tracking application.

Your role is to:
- Provide general health information and wellness tips
- Help users understand their health data and metrics
- Suggest healthy lifestyle practices
- Answer questions about medications, appointments, and health tracking
- Offer motivation and support for health goals

Important guidelines:
- Always recommend consulting healthcare professionals for medical advice
- Never provide specific medical diagnoses or treatment recommendations
- Focus on general wellness, prevention, and health management
- Be supportive, encouraging, and informative
- Keep responses concise and practical

The user is using a health management app that tracks:
- Medications and dosages
- Health metrics (blood pressure, glucose, weight, etc.)
- Medical appointments
- Health reminders and notifications

Current date and time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

Remember: You're an assistant, not a replacement for professional medical care."""

    def chat(self, message: str, conversation_history: Optional[List[Dict[str, str]]] = None) -> Dict[str, Any]:
        """
        Process a chat message and return ChatGPT response.

        Args:
            message: User's message
            conversation_history: Previous messages in the conversation

        Returns:
            Dictionary with response data and metadata
        """
        if not self.is_initialized:
            return {
                'success': False,
                'error': 'ChatGPT service not available. Please check API key configuration.',
                'response': 'I\'m sorry, but the ChatGPT service is currently unavailable. Please ensure the OpenAI API key is properly configured.'
            }

        try:
            # Build conversation messages
            messages = [{"role": "system", "content": self.get_health_context()}]

            if conversation_history:
                for entry in conversation_history[-10:]:  # Only last 10 exchanges
                    if 'user' in entry:
                        messages.append({"role": "user", "content": entry['user']})
                    if 'assistant' in entry:
                        messages.append({"role": "assistant", "content": entry['assistant']})

            messages.append({"role": "user", "content": message})

            # Call OpenAI API
            response = self.client.ChatCompletion.create(
                model="gpt-4o",
                messages=messages,
                max_tokens=500,
                temperature=0.7,
                presence_penalty=0.1,
                frequency_penalty=0.1
            )

            assistant_response = response.choices[0].message.content

            return {
                'success': True,
                'response': assistant_response,
                'tokens_used': response.usage.total_tokens if hasattr(response, 'usage') else 0,
                'model': 'gpt-4o',
                'timestamp': datetime.now().isoformat()
            }

        except Exception as e:
            logger.error(f"ChatGPT API error: {e}")
            return {
                'success': False,
                'error': str(e),
                'response': 'I apologize, but I encountered an error while processing your request. Please try again later.'
            }

    def get_health_tips(self, category: str = "general") -> Dict[str, Any]:
        """Get health tips for specific categories."""
        tips_prompts = {
            "general": "Provide 3 practical daily health tips for general wellness.",
            "medication": "Provide 3 tips for proper medication management and adherence.",
            "exercise": "Provide 3 tips for maintaining regular physical activity.",
            "nutrition": "Provide 3 tips for healthy eating and nutrition.",
            "sleep": "Provide 3 tips for better sleep hygiene and quality rest.",
            "stress": "Provide 3 tips for managing stress and mental wellness."
        }

        prompt = tips_prompts.get(category, tips_prompts["general"])
        prompt += " Keep each tip concise (1-2 sentences) and actionable."

        return self.chat(prompt)

    def is_available(self) -> bool:
        """Check if the chatbot service is available."""
        return self.is_initialized


# Global chatbot service instance
chatbot_service = ChatbotService()