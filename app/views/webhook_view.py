"""
Webhook View - Handles incoming Telegram webhook requests.
"""
from flask import Blueprint, request, jsonify
import logging

from app.controllers import get_email_controller, get_calendar_controller
from app.services import get_telegram_service

# Create blueprint
webhook_bp = Blueprint('webhook', __name__)

# Setup logging
logger = logging.getLogger(__name__)


@webhook_bp.route('/webhook', methods=['POST'])
def webhook():
    """
    Handle incoming webhook updates from Telegram.
    
    Expected format from Telegram:
    {
        "update_id": 123456789,
        "message": {
            "message_id": 1,
            "from": {"id": 12345, "first_name": "User"},
            "chat": {"id": 12345, "type": "private"},
            "text": "111"
        }
    }
    """
    try:
        data = request.get_json()
        
        if not data:
            logger.warning("Received empty webhook request")
            return jsonify({'ok': False, 'error': 'No data received'}), 400
        
        # Extract message data
        if 'message' not in data:
            logger.info("Webhook update without message (could be edited message, etc.)")
            return jsonify({'ok': True}), 200
        
        message = data['message']
        chat_id = message['chat']['id']
        user_id = message['from']['id']
        text = message.get('text', '').strip()
        
        logger.info(f"Received message from chat_id={chat_id}, user_id={user_id}, text='{text}'")
        
        # Handle /start command
        if text == '/start':
            handle_start_command(chat_id)
            return jsonify({'ok': True}), 200
        
        # Handle /help command
        if text == '/help':
            handle_help_command(chat_id)
            return jsonify({'ok': True}), 200
        
        # Route commands to appropriate controllers
        if text.startswith('1'):  # Email commands (111, 112, 113)
            handle_email_command(chat_id, text)
        elif text.startswith('2'):  # Calendar commands (211, 212, 213)
            handle_calendar_command(chat_id, text)
        else:
            handle_unknown_command(chat_id, text)
        
        return jsonify({'ok': True}), 200
        
    except Exception as e:
        logger.error(f"Error processing webhook: {str(e)}", exc_info=True)
        return jsonify({'ok': False, 'error': str(e)}), 500


def handle_start_command(chat_id: int):
    """Send welcome message with available commands."""
    telegram_service = get_telegram_service()
    
    message = """🤖 *Bienvenido al Bot de Automatización*

Este bot te permite gestionar tu email y calendario de Google mediante comandos simples.

*Comandos disponibles:*

📧 *EMAIL:*
• `111` - Enviar email de prueba
• `112` - Eliminar emails antiguos
• `113` - Leer emails de hoy

📅 *CALENDARIO:*
• `211` - Ver eventos del mes
• `212` - Crear evento (cumpleaños)
• `213` - Eliminar eventos de hoy

Usa `/help` para ver esta ayuda nuevamente.
"""
    
    telegram_service.send_message(chat_id, message)


def handle_help_command(chat_id: int):
    """Send help message."""
    handle_start_command(chat_id)


def handle_email_command(chat_id: int, command: str):
    """Route email commands to the email controller."""
    email_controller = get_email_controller()
    telegram_service = get_telegram_service()
    
    valid_commands = ['111', '112', '113']
    
    if command in valid_commands:
        logger.info(f"Processing email command: {command}")
        email_controller.handle_command(chat_id, command)
    else:
        message = f"❌ Comando de email inválido: `{command}`\n\n"
        message += "Comandos válidos: 111, 112, 113\n"
        message += "Usa `/help` para ver todos los comandos."
        telegram_service.send_message(chat_id, message)


def handle_calendar_command(chat_id: int, command: str):
    """Route calendar commands to the calendar controller."""
    calendar_controller = get_calendar_controller()
    telegram_service = get_telegram_service()
    
    valid_commands = ['211', '212', '213']
    
    if command in valid_commands:
        logger.info(f"Processing calendar command: {command}")
        calendar_controller.handle_command(chat_id, command)
    else:
        message = f"❌ Comando de calendario inválido: `{command}`\n\n"
        message += "Comandos válidos: 211, 212, 213\n"
        message += "Usa `/help` para ver todos los comandos."
        telegram_service.send_message(chat_id, message)


def handle_unknown_command(chat_id: int, text: str):
    """Handle unknown commands."""
    telegram_service = get_telegram_service()
    
    message = f"❓ Comando no reconocido: `{text}`\n\n"
    message += "Usa `/help` para ver los comandos disponibles."
    
    telegram_service.send_message(chat_id, message)


@webhook_bp.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({
        'status': 'healthy',
        'service': 'telegram-automation-bot'
    }), 200


@webhook_bp.route('/', methods=['GET'])
def index():
    """Root endpoint."""
    return jsonify({
        'service': 'Telegram Automation Bot',
        'version': '1.0.0',
        'status': 'running'
    }), 200
