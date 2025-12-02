#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Telegram Bot con POLLING - Automatización de Email y Calendar
Versión simplificada SIN Flask, SIN webhooks, SIN ngrok
Solo ejecuta y funciona directamente desde tu PC
"""
import os
import sys
import base64
import datetime
import logging
import time
from typing import Dict, Any, Optional
from email.mime.text import MIMEText

from dotenv import load_dotenv
import requests

# Google API imports
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# ==================== CONFIGURACIÓN ====================

load_dotenv()

# Telegram
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
TELEGRAM_BASE_URL = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}" if TELEGRAM_BOT_TOKEN else None

# Google
GOOGLE_CREDENTIALS_PATH = os.getenv('GOOGLE_CREDENTIALS_PATH', 'credentials.json')
GOOGLE_TOKEN_PATH = os.getenv('GOOGLE_TOKEN_PATH', 'token.json')
GOOGLE_SCOPES = [
    'https://www.googleapis.com/auth/calendar',
    'https://www.googleapis.com/auth/gmail.send',
    'https://www.googleapis.com/auth/gmail.readonly',
    'https://www.googleapis.com/auth/gmail.modify'
]

# Email y Calendar
DEFAULT_EMAIL_RECIPIENT = os.getenv('DEFAULT_EMAIL_RECIPIENT', 'default@example.com')
CALENDAR_TIMEZONE = os.getenv('CALENDAR_TIMEZONE', 'America/Lima')

# Logging
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')

# ==================== CONFIGURACIÓN DE LOGGING ====================

logging.basicConfig(
    level=getattr(logging, LOG_LEVEL.upper(), logging.INFO),
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)

# Reducir ruido de librerías
logging.getLogger('urllib3').setLevel(logging.WARNING)

# ==================== SERVICIOS GOOGLE ====================

class GoogleService:
    """Servicio para interactuar con Gmail y Google Calendar"""
    
    def __init__(self):
        self.creds = None
        self.calendar_service = None
        self.gmail_service = None
        self.authenticated = False
        
        try:
            self._authenticate()
            self.authenticated = True
            logger.info("✅ Google service authenticated")
        except Exception as e:
            logger.warning(f"⚠️  Google authentication failed: {e}")
            logger.warning("   Email and Calendar features will not work")
    
    def _authenticate(self):
        """Autenticar con Google APIs"""
        if os.path.exists(GOOGLE_TOKEN_PATH):
            self.creds = Credentials.from_authorized_user_file(GOOGLE_TOKEN_PATH, GOOGLE_SCOPES)
        
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(GOOGLE_CREDENTIALS_PATH, GOOGLE_SCOPES)
                self.creds = flow.run_local_server(port=0)
            
            with open(GOOGLE_TOKEN_PATH, 'w') as token:
                token.write(self.creds.to_json())
        
        self.calendar_service = build('calendar', 'v3', credentials=self.creds)
        self.gmail_service = build('gmail', 'v1', credentials=self.creds)
    
    # ---------- GMAIL METHODS ----------
    
    def send_email(self, recipient: str, subject: str, body: str) -> Dict[str, Any]:
        """Enviar email via Gmail API"""
        if not self.authenticated:
            return {'success': False, 'message': 'Google not authenticated'}
        
        try:
            message = MIMEText(body)
            message['to'] = recipient
            message['subject'] = subject
            message['from'] = 'me'
            
            raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
            send_message = self.gmail_service.users().messages().send(
                userId='me', body={'raw': raw_message}
            ).execute()
            
            return {'success': True, 'message_id': send_message['id']}
        except Exception as e:
            return {'success': False, 'message': str(e)}
    
    def list_emails(self, max_results: int = 10, days_ago: int = 0) -> Dict[str, Any]:
        """Listar emails (days_ago=0 para emails de hoy)"""
        if not self.authenticated:
            return {'success': False, 'emails': [], 'message': 'Google not authenticated'}
        
        try:
            query = ''
            if days_ago >= 0:
                date = (datetime.datetime.now() - datetime.timedelta(days=days_ago)).strftime('%Y/%m/%d')
                query = f'after:{date}'
            
            results = self.gmail_service.users().messages().list(
                userId='me', maxResults=max_results, q=query
            ).execute()
            
            messages = results.get('messages', [])
            email_list = []
            
            for msg in messages:
                msg_data = self.gmail_service.users().messages().get(
                    userId='me', id=msg['id'], format='metadata',
                    metadataHeaders=['From', 'Subject', 'Date']
                ).execute()
                
                headers = msg_data['payload']['headers']
                email_list.append({
                    'id': msg['id'],
                    'from': next((h['value'] for h in headers if h['name'] == 'From'), 'Unknown'),
                    'subject': next((h['value'] for h in headers if h['name'] == 'Subject'), 'No Subject'),
                    'date': next((h['value'] for h in headers if h['name'] == 'Date'), 'Unknown')
                })
            
            return {'success': True, 'count': len(email_list), 'emails': email_list}
        except Exception as e:
            return {'success': False, 'emails': [], 'message': str(e)}
    
    # ---------- CALENDAR METHODS ----------
    
    def list_events(self, max_results: int = 50, time_min: str = None) -> Dict[str, Any]:
        """Listar eventos del calendario"""
        if not self.authenticated:
            return {'success': False, 'events': [], 'message': 'Google not authenticated'}
        
        try:
            if time_min is None:
                time_min = datetime.datetime.now().astimezone().isoformat()
            
            events_result = self.calendar_service.events().list(
                calendarId='primary', timeMin=time_min, maxResults=max_results,
                singleEvents=True, orderBy='startTime'
            ).execute()
            
            events = events_result.get('items', [])
            event_list = []
            
            for event in events:
                start = event['start'].get('dateTime', event['start'].get('date'))
                event_list.append({
                    'id': event['id'],
                    'summary': event.get('summary', 'Sin título'),
                    'start': start,
                    'description': event.get('description', ''),
                    'link': event.get('htmlLink', '')
                })
            
            return {'success': True, 'count': len(event_list), 'events': event_list}
        except Exception as e:
            return {'success': False, 'events': [], 'message': str(e)}
    
    def create_event(self, title: str, date: str, start_time: str = "10:00", 
                     end_time: str = "11:00", description: str = "") -> Dict[str, Any]:
        """Crear evento en el calendario"""
        if not self.authenticated:
            return {'success': False, 'message': 'Google not authenticated'}
        
        try:
            start_datetime = f"{date}T{start_time}:00"
            end_datetime = f"{date}T{end_time}:00"
            
            event = {
                'summary': title,
                'description': description,
                'start': {'dateTime': start_datetime, 'timeZone': CALENDAR_TIMEZONE},
                'end': {'dateTime': end_datetime, 'timeZone': CALENDAR_TIMEZONE},
            }
            
            created_event = self.calendar_service.events().insert(
                calendarId='primary', body=event
            ).execute()
            
            return {
                'success': True,
                'event_id': created_event['id'],
                'link': created_event.get('htmlLink', '')
            }
        except Exception as e:
            return {'success': False, 'message': str(e)}
    
    def delete_today_events(self, date: str = None) -> Dict[str, Any]:
        """Eliminar eventos de una fecha específica"""
        if not self.authenticated:
            return {'success': False, 'deleted_count': 0, 'message': 'Google not authenticated'}
        
        try:
            if date is None:
                date = datetime.datetime.now().strftime('%Y-%m-%d')
            
            time_min = f"{date}T00:00:00Z"
            time_max = f"{date}T23:59:59Z"
            
            events_result = self.calendar_service.events().list(
                calendarId='primary', timeMin=time_min, timeMax=time_max,
                singleEvents=True
            ).execute()
            
            events = events_result.get('items', [])
            deleted_count = 0
            
            for event in events:
                self.calendar_service.events().delete(
                    calendarId='primary', eventId=event['id']
                ).execute()
                deleted_count += 1
            
            return {'success': True, 'deleted_count': deleted_count}
        except Exception as e:
            return {'success': False, 'deleted_count': 0, 'message': str(e)}


# Instancia global de Google Service
google_service = GoogleService()

# ==================== SERVICIO TELEGRAM ====================

def send_telegram_message(chat_id: int, text: str, parse_mode: str = 'Markdown') -> Dict[str, Any]:
    """Enviar mensaje de Telegram"""
    if not TELEGRAM_BASE_URL:
        logger.error("TELEGRAM_BOT_TOKEN not configured")
        return {'success': False, 'message': 'Telegram not configured'}
    
    try:
        url = f"{TELEGRAM_BASE_URL}/sendMessage"
        payload = {'chat_id': chat_id, 'text': text, 'parse_mode': parse_mode}
        response = requests.post(url, json=payload, timeout=10)
        response.raise_for_status()
        return {'success': True, 'response': response.json()}
    except Exception as e:
        logger.error(f"Error sending Telegram message: {e}")
        return {'success': False, 'message': str(e)}


def get_updates(offset: int = None, timeout: int = 30) -> Dict[str, Any]:
    """Obtener actualizaciones de Telegram (polling)"""
    if not TELEGRAM_BASE_URL:
        return {'success': False, 'updates': []}
    
    try:
        url = f"{TELEGRAM_BASE_URL}/getUpdates"
        params = {'timeout': timeout}
        if offset:
            params['offset'] = offset
        
        response = requests.get(url, params=params, timeout=timeout + 5)
        response.raise_for_status()
        data = response.json()
        
        if data.get('ok'):
            return {'success': True, 'updates': data.get('result', [])}
        else:
            return {'success': False, 'updates': []}
    except Exception as e:
        logger.error(f"Error getting updates: {e}")
        return {'success': False, 'updates': []}

# ==================== HANDLERS DE COMANDOS ====================

def handle_email_command_111(chat_id: int):
    """111 - Enviar email de prueba"""
    recipient = DEFAULT_EMAIL_RECIPIENT
    subject = "Mensaje automático desde Telegram Bot"
    body = "Hola,\n\nEste es un mensaje enviado automáticamente desde el Bot de Telegram.\n\nSaludos."
    
    result = google_service.send_email(recipient, subject, body)
    
    if result['success']:
        message = f"✅ *Email enviado exitosamente*\n\n📧 Destinatario: `{recipient}`\n📋 Asunto: {subject}"
    else:
        message = f"❌ *Error al enviar email*\n\n{result['message']}"
    
    send_telegram_message(chat_id, message)


def handle_email_command_113(chat_id: int):
    """113 - Leer emails de hoy"""
    result = google_service.list_emails(max_results=10, days_ago=0)
    
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
                
                if len(message) > 3800:
                    message += "\n_...más emails disponibles_"
                    break
    else:
        message = f"❌ *Error al leer emails*\n\n{result['message']}"
    
    send_telegram_message(chat_id, message)


def handle_calendar_command_211(chat_id: int):
    """211 - Ver eventos del mes actual"""
    today = datetime.datetime.now()
    first_day = today.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    time_min = first_day.astimezone().isoformat()
    
    result = google_service.list_events(max_results=50, time_min=time_min)
    
    if result['success']:
        events = result['events']
        if not events:
            message = "📅 *No hay eventos este mes*"
        else:
            month_name = today.strftime('%B %Y')
            message = f"📅 *Eventos de {month_name} ({result['count']})*\n\n"
            
            for idx, event in enumerate(events, 1):
                try:
                    start_dt = datetime.datetime.fromisoformat(event['start'].replace('Z', '+00:00'))
                    date_str = start_dt.strftime('%d/%m/%Y %H:%M')
                except:
                    date_str = event['start']
                
                message += f"*{idx}. {event['summary']}*\n"
                message += f"   📅 {date_str}\n"
                
                if len(message) > 3800:
                    message += "\n_...más eventos disponibles_"
                    break
    else:
        message = f"❌ *Error al leer eventos*\n\n{result['message']}"
    
    send_telegram_message(chat_id, message)


def handle_calendar_command_212(chat_id: int, title: str = None, date: str = None, 
                                 start_time: str = None, end_time: str = None):
    """212 - Crear evento en el calendario"""
    if title is None:
        title = "Cumpleaños"
    if date is None:
        date = datetime.datetime.now().strftime('%Y-%m-%d')
    if start_time is None:
        start_time = "10:00"
    if end_time is None:
        end_time = "11:00"
    
    description = "Evento creado desde Telegram Bot"
    result = google_service.create_event(title, date, start_time, end_time, description)
    
    if result['success']:
        message = f"✅ *Evento creado exitosamente*\n\n"
        message += f"📋 Título: *{title}*\n"
        message += f"📅 Fecha: {date}\n"
        message += f"🕐 Hora: {start_time} - {end_time}\n"
        if result.get('link'):
            message += f"🔗 [Ver en Calendar]({result['link']})"
    else:
        message = f"❌ *Error al crear evento*\n\n{result['message']}"
    
    send_telegram_message(chat_id, message)


def handle_calendar_command_213(chat_id: int, date: str = None):
    """213 - Eliminar eventos de hoy"""
    if date is None:
        date = datetime.datetime.now().strftime('%Y-%m-%d')
    
    result = google_service.delete_today_events(date)
    
    if result['success']:
        message = f"✅ *Eventos eliminados*\n\n🗑️ Eliminados: {result['deleted_count']} eventos\n📅 Fecha: {date}"
    else:
        message = f"❌ *Error al eliminar eventos*\n\n{result['message']}"
    
    send_telegram_message(chat_id, message)


def handle_message(message: Dict[str, Any]):
    """Procesar mensaje de Telegram"""
    chat_id = message['chat']['id']
    text = message.get('text', '').strip()
    
    logger.info(f"📩 Mensaje de chat_id={chat_id}: '{text}'")
    
    # Comando /start o /help
    if text in ['/start', '/help']:
        help_message = """🤖 *Bot de Automatización - Email y Calendar*

*Comandos disponibles:*

📧 *EMAIL:*
• `111` - Enviar email de prueba
• `113` - Leer emails de hoy

📅 *CALENDARIO:*
• `211` - Ver eventos del mes
• `212` - Crear evento (cumpleaños)
• `213` - Eliminar eventos de hoy

_Escribe el número del comando que quieras ejecutar._
"""
        send_telegram_message(chat_id, help_message)
        return
    
    # Comandos de Email (111, 113)
    if text == '111':
        handle_email_command_111(chat_id)
    elif text == '113':
        handle_email_command_113(chat_id)
    
    # Comandos de Calendar (211, 212, 213)
    elif text == '211':
        handle_calendar_command_211(chat_id)
    elif text == '212':
        handle_calendar_command_212(chat_id)
    elif text == '213':
        handle_calendar_command_213(chat_id)
    
    # Comando desconocido
    else:
        if text and not text.startswith('/'):
            send_telegram_message(chat_id, "❓ Comando no reconocido. Usa /help para ver los comandos disponibles.")


# ==================== MAIN - POLLING LOOP ====================

def main():
    """Loop principal de polling"""
    print("=" * 70)
    print("🤖 Telegram Bot - Modo POLLING")
    print("=" * 70)
    print()
    
    # Validar configuración
    if not TELEGRAM_BOT_TOKEN:
        print("❌ ERROR: TELEGRAM_BOT_TOKEN no configurado en .env")
        print("   Edita el archivo .env y agrega tu token de @BotFather")
        sys.exit(1)
    
    if not os.path.exists(GOOGLE_CREDENTIALS_PATH):
        print(f"⚠️  WARNING: {GOOGLE_CREDENTIALS_PATH} no encontrado")
        print("   Las funciones de Gmail y Calendar no funcionarán")
        print()
    
    print("✅ Bot iniciado correctamente")
    print("📱 Abre Telegram y habla con tu bot")
    print("💡 Presiona CTRL+C para detener")
    print("=" * 70)
    print()
    
    # Primero, eliminar webhook si existe
    try:
        requests.post(f"{TELEGRAM_BASE_URL}/deleteWebhook")
        logger.info("Webhook eliminado")
    except:
        pass
    
    offset = None
    
    try:
        while True:
            # Obtener actualizaciones
            result = get_updates(offset=offset, timeout=30)
            
            if result['success']:
                updates = result['updates']
                
                for update in updates:
                    # Actualizar offset para no recibir el mismo mensaje dos veces
                    offset = update['update_id'] + 1
                    
                    # Procesar mensaje
                    if 'message' in update:
                        handle_message(update['message'])
            
            time.sleep(0.1)  # Pequeña pausa para no saturar
            
    except KeyboardInterrupt:
        print("\n\n🛑 Bot detenido por el usuario")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Error en el loop principal: {e}", exc_info=True)
        sys.exit(1)


if __name__ == '__main__':
    main()
