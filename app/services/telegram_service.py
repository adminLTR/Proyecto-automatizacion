"""
Telegram Service - Handles communication with Telegram API.
"""
import requests
from typing import Dict, Any, Optional
from app.config import config


class TelegramService:
    """Service for sending messages and interacting with Telegram API."""
    
    def __init__(self):
        """Initialize Telegram service."""
        self.base_url = config.telegram_api_url
    
    def send_message(self, chat_id: int, text: str, parse_mode: str = 'Markdown') -> Dict[str, Any]:
        """
        Send a text message to a Telegram chat.
        
        Args:
            chat_id: Telegram chat ID
            text: Message text to send
            parse_mode: Parse mode for the message (Markdown or HTML)
            
        Returns:
            Dict with status and response
        """
        try:
            url = f"{self.base_url}/sendMessage"
            payload = {
                'chat_id': chat_id,
                'text': text,
                'parse_mode': parse_mode
            }
            
            response = requests.post(url, json=payload, timeout=10)
            response.raise_for_status()
            
            return {
                'success': True,
                'response': response.json()
            }
        except requests.RequestException as e:
            return {
                'success': False,
                'message': f'Error sending message: {str(e)}'
            }
    
    def send_keyboard(self, chat_id: int, text: str, keyboard: list) -> Dict[str, Any]:
        """
        Send a message with a custom keyboard.
        
        Args:
            chat_id: Telegram chat ID
            text: Message text
            keyboard: Keyboard layout (list of lists of button texts)
            
        Returns:
            Dict with status and response
        """
        try:
            url = f"{self.base_url}/sendMessage"
            reply_markup = {
                'keyboard': keyboard,
                'resize_keyboard': True,
                'one_time_keyboard': False
            }
            
            payload = {
                'chat_id': chat_id,
                'text': text,
                'reply_markup': reply_markup
            }
            
            response = requests.post(url, json=payload, timeout=10)
            response.raise_for_status()
            
            return {
                'success': True,
                'response': response.json()
            }
        except requests.RequestException as e:
            return {
                'success': False,
                'message': f'Error sending keyboard: {str(e)}'
            }
    
    def get_webhook_info(self) -> Dict[str, Any]:
        """
        Get current webhook information.
        
        Returns:
            Dict with webhook information
        """
        try:
            url = f"{self.base_url}/getWebhookInfo"
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            
            return {
                'success': True,
                'info': response.json()
            }
        except requests.RequestException as e:
            return {
                'success': False,
                'message': f'Error getting webhook info: {str(e)}'
            }
    
    def set_webhook(self, webhook_url: str) -> Dict[str, Any]:
        """
        Set webhook URL for receiving updates.
        
        Args:
            webhook_url: The HTTPS URL for webhook
            
        Returns:
            Dict with status
        """
        try:
            url = f"{self.base_url}/setWebhook"
            payload = {'url': webhook_url}
            
            response = requests.post(url, json=payload, timeout=10)
            response.raise_for_status()
            
            return {
                'success': True,
                'response': response.json()
            }
        except requests.RequestException as e:
            return {
                'success': False,
                'message': f'Error setting webhook: {str(e)}'
            }
    
    def delete_webhook(self) -> Dict[str, Any]:
        """
        Delete the current webhook.
        
        Returns:
            Dict with status
        """
        try:
            url = f"{self.base_url}/deleteWebhook"
            response = requests.post(url, timeout=10)
            response.raise_for_status()
            
            return {
                'success': True,
                'response': response.json()
            }
        except requests.RequestException as e:
            return {
                'success': False,
                'message': f'Error deleting webhook: {str(e)}'
            }


# Global service instance (singleton)
_telegram_service = None

def get_telegram_service() -> TelegramService:
    """Get or create the Telegram service instance."""
    global _telegram_service
    if _telegram_service is None:
        _telegram_service = TelegramService()
    return _telegram_service
