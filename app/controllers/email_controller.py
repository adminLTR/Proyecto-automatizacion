"""
Email Controller - Handles email-related commands from Telegram.
"""
import datetime
from typing import Dict, Any

from app.services import get_google_service, get_telegram_service
from app.config import config


class EmailController:
    """Controller for processing email commands."""
    
    def __init__(self):
        """Initialize email controller."""
        self.google_service = get_google_service()
        self.telegram_service = get_telegram_service()
    
    def handle_command(self, chat_id: int, command: str) -> Dict[str, Any]:
        """
        Route email commands to appropriate handlers.
        
        Args:
            chat_id: Telegram chat ID
            command: Command code (111, 112, 113)
            
        Returns:
            Dict with execution result
        """
        handlers = {
            '111': self.send_email,
            '112': self.delete_old_emails,
            '113': self.read_today_emails
        }
        
        handler = handlers.get(command)
        if handler:
            return handler(chat_id)
        else:
            return {
                'success': False,
                'message': f'Unknown email command: {command}'
            }
    
    def send_email(self, chat_id: int) -> Dict[str, Any]:
        """
        Send a default email (command 111).
        
        Args:
            chat_id: Telegram chat ID
            
        Returns:
            Dict with execution result
        """
        try:
            recipient = config.DEFAULT_EMAIL_RECIPIENT
            subject = "Mensaje automático desde Telegram Bot"
            body = """Hola,

Este es un mensaje enviado automáticamente desde el Bot de Telegram.

Saludos."""
            
            result = self.google_service.send_email(recipient, subject, body)
            
            if result['success']:
                message = f"✅ *Email enviado exitosamente*\n\n"
                message += f"📧 Destinatario: `{recipient}`\n"
                message += f"📋 Asunto: {subject}\n"
                message += f"🆔 ID: `{result['message_id']}`"
            else:
                message = f"❌ *Error al enviar email*\n\n{result['message']}"
            
            self.telegram_service.send_message(chat_id, message)
            return result
            
        except Exception as e:
            error_msg = f"❌ *Error inesperado*\n\n{str(e)}"
            self.telegram_service.send_message(chat_id, error_msg)
            return {
                'success': False,
                'message': str(e)
            }
    
    def delete_old_emails(self, chat_id: int, days_ago: int = None) -> Dict[str, Any]:
        """
        Delete old emails (command 112).
        
        Args:
            chat_id: Telegram chat ID
            days_ago: Number of days to look back (default from config)
            
        Returns:
            Dict with execution result
        """
        try:
            if days_ago is None:
                days_ago = config.EMAIL_DELETE_DAYS_AGO
            
            result = self.google_service.delete_old_emails(days_ago)
            
            if result['success']:
                message = f"✅ *Emails eliminados*\n\n"
                message += f"🗑️ Movidos a la papelera: {result['deleted_count']} emails\n"
                message += f"📅 Más antiguos que: {days_ago} días"
            else:
                message = f"❌ *Error al eliminar emails*\n\n{result['message']}"
            
            self.telegram_service.send_message(chat_id, message)
            return result
            
        except Exception as e:
            error_msg = f"❌ *Error inesperado*\n\n{str(e)}"
            self.telegram_service.send_message(chat_id, error_msg)
            return {
                'success': False,
                'message': str(e)
            }
    
    def read_today_emails(self, chat_id: int) -> Dict[str, Any]:
        """
        Read today's emails (command 113).
        
        Args:
            chat_id: Telegram chat ID
            
        Returns:
            Dict with execution result
        """
        try:
            result = self.google_service.list_emails(max_results=10, days_ago=0)
            
            if result['success']:
                emails = result['emails']
                
                if not emails:
                    message = "📭 *No hay emails de hoy*"
                else:
                    message = f"📬 *Emails de hoy ({result['count']})*\n\n"
                    
                    for idx, email in enumerate(emails, 1):
                        message += f"*{idx}. {email['subject']}*\n"
                        message += f"   De: {email['from']}\n"
                        message += f"   Fecha: {email['date']}\n\n"
                
                # Split message if too long (Telegram limit is 4096 characters)
                if len(message) > 4000:
                    parts = self._split_message(message, 4000)
                    for part in parts:
                        self.telegram_service.send_message(chat_id, part)
                else:
                    self.telegram_service.send_message(chat_id, message)
            else:
                message = f"❌ *Error al leer emails*\n\n{result['message']}"
                self.telegram_service.send_message(chat_id, message)
            
            return result
            
        except Exception as e:
            error_msg = f"❌ *Error inesperado*\n\n{str(e)}"
            self.telegram_service.send_message(chat_id, error_msg)
            return {
                'success': False,
                'message': str(e)
            }
    
    def _split_message(self, message: str, max_length: int = 4000) -> list:
        """
        Split a long message into smaller chunks.
        
        Args:
            message: Message to split
            max_length: Maximum length of each chunk
            
        Returns:
            List of message chunks
        """
        lines = message.split('\n')
        chunks = []
        current_chunk = ""
        
        for line in lines:
            if len(current_chunk) + len(line) + 1 <= max_length:
                current_chunk += line + '\n'
            else:
                if current_chunk:
                    chunks.append(current_chunk)
                current_chunk = line + '\n'
        
        if current_chunk:
            chunks.append(current_chunk)
        
        return chunks


# Global controller instance
_email_controller = None

def get_email_controller() -> EmailController:
    """Get or create the email controller instance."""
    global _email_controller
    if _email_controller is None:
        _email_controller = EmailController()
    return _email_controller
