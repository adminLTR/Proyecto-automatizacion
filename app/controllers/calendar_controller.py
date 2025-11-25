"""
Calendar Controller - Handles calendar-related commands from Telegram.
"""
import datetime
from typing import Dict, Any

from app.services import get_google_service, get_telegram_service
from app.config import config


class CalendarController:
    """Controller for processing calendar commands."""
    
    def __init__(self):
        """Initialize calendar controller."""
        self.google_service = get_google_service()
        self.telegram_service = get_telegram_service()
    
    def handle_command(self, chat_id: int, command: str) -> Dict[str, Any]:
        """
        Route calendar commands to appropriate handlers.
        
        Args:
            chat_id: Telegram chat ID
            command: Command code (211, 212, 213)
            
        Returns:
            Dict with execution result
        """
        handlers = {
            '211': self.list_month_events,
            '212': self.create_event,
            '213': self.delete_today_events
        }
        
        handler = handlers.get(command)
        if handler:
            return handler(chat_id)
        else:
            return {
                'success': False,
                'message': f'Unknown calendar command: {command}'
            }
    
    def list_month_events(self, chat_id: int) -> Dict[str, Any]:
        """
        List events for this month (command 211).
        
        Args:
            chat_id: Telegram chat ID
            
        Returns:
            Dict with execution result
        """
        try:
            # Get first day of current month
            today = datetime.datetime.now()
            first_day = today.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
            time_min = first_day.astimezone().isoformat()
            
            result = self.google_service.list_events(max_results=50, time_min=time_min)
            
            if result['success']:
                events = result['events']
                
                if not events:
                    message = "📅 *No hay eventos este mes*"
                else:
                    month_name = today.strftime('%B %Y')
                    message = f"📅 *Eventos de {month_name} ({result['count']})*\n\n"
                    
                    for idx, event in enumerate(events, 1):
                        # Parse start datetime
                        try:
                            start_dt = datetime.datetime.fromisoformat(event['start'].replace('Z', '+00:00'))
                            date_str = start_dt.strftime('%d/%m/%Y %H:%M')
                        except:
                            date_str = event['start']
                        
                        message += f"*{idx}. {event['summary']}*\n"
                        message += f"   📅 {date_str}\n"
                        if event.get('description'):
                            desc = event['description'][:50] + '...' if len(event['description']) > 50 else event['description']
                            message += f"   📝 {desc}\n"
                        message += f"   🆔 `{event['id']}`\n\n"
                
                # Split message if too long
                if len(message) > 4000:
                    parts = self._split_message(message, 4000)
                    for part in parts:
                        self.telegram_service.send_message(chat_id, part)
                else:
                    self.telegram_service.send_message(chat_id, message)
            else:
                message = f"❌ *Error al leer eventos*\n\n{result['message']}"
                self.telegram_service.send_message(chat_id, message)
            
            return result
            
        except Exception as e:
            error_msg = f"❌ *Error inesperado*\n\n{str(e)}"
            self.telegram_service.send_message(chat_id, error_msg)
            return {
                'success': False,
                'message': str(e)
            }
    
    def create_event(self, chat_id: int, title: str = None, date: str = None, 
                    start_time: str = None, end_time: str = None) -> Dict[str, Any]:
        """
        Create a calendar event (command 212).
        
        Args:
            chat_id: Telegram chat ID
            title: Event title (default: "Cumpleaños")
            date: Date in YYYY-MM-DD format (default: today)
            start_time: Start time in HH:MM format (default: 10:00)
            end_time: End time in HH:MM format (default: 11:00)
            
        Returns:
            Dict with execution result
        """
        try:
            # Set defaults
            if title is None:
                title = "Cumpleaños"
            
            if date is None:
                date = datetime.datetime.now().strftime('%Y-%m-%d')
            
            if start_time is None:
                start_time = "10:00"
            
            if end_time is None:
                end_time = "11:00"
            
            description = "Evento creado desde Telegram Bot"
            
            result = self.google_service.create_event(title, date, start_time, end_time, description)
            
            if result['success']:
                message = f"✅ *Evento creado exitosamente*\n\n"
                message += f"📋 Título: *{title}*\n"
                message += f"📅 Fecha: {date}\n"
                message += f"🕐 Hora: {start_time} - {end_time}\n"
                message += f"🆔 ID: `{result['event_id']}`"
                
                if result.get('link'):
                    message += f"\n🔗 [Ver en Calendar]({result['link']})"
            else:
                message = f"❌ *Error al crear evento*\n\n{result['message']}"
            
            self.telegram_service.send_message(chat_id, message)
            return result
            
        except Exception as e:
            error_msg = f"❌ *Error inesperado*\n\n{str(e)}"
            self.telegram_service.send_message(chat_id, error_msg)
            return {
                'success': False,
                'message': str(e)
            }
    
    def delete_today_events(self, chat_id: int, date: str = None) -> Dict[str, Any]:
        """
        Delete all events for a specific date (command 213).
        
        Args:
            chat_id: Telegram chat ID
            date: Date in YYYY-MM-DD format (default: today)
            
        Returns:
            Dict with execution result
        """
        try:
            if date is None:
                date = datetime.datetime.now().strftime('%Y-%m-%d')
            
            result = self.google_service.delete_events_by_date(date)
            
            if result['success']:
                message = f"✅ *Eventos eliminados*\n\n"
                message += f"🗑️ Eliminados: {result['deleted_count']} eventos\n"
                message += f"📅 Fecha: {date}"
            else:
                message = f"❌ *Error al eliminar eventos*\n\n{result['message']}"
            
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
_calendar_controller = None

def get_calendar_controller() -> CalendarController:
    """Get or create the calendar controller instance."""
    global _calendar_controller
    if _calendar_controller is None:
        _calendar_controller = CalendarController()
    return _calendar_controller
