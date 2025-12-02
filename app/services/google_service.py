"""
Google Services - Handles authentication and operations for Gmail and Calendar.
"""
import os
import datetime
import base64
from typing import Optional, List, Dict, Any
from email.mime.text import MIMEText

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from app.config import config


class GoogleService:
    """Service for interacting with Google APIs (Gmail and Calendar)."""
    
    def __init__(self):
        """Initialize Google service with authentication."""
        self.creds = None
        self.calendar_service = None
        self.gmail_service = None
        self.authenticated = False
        try:
            self._authenticate()
            self.authenticated = True
        except Exception as e:
            print(f"⚠️  Google authentication failed: {e}")
            print("   Some features will not work until you configure Google credentials.")
            self.authenticated = False
    
    def _authenticate(self):
        """Authenticate with Google API and create service objects."""
        # Load existing credentials
        if os.path.exists(config.GOOGLE_TOKEN_PATH):
            self.creds = Credentials.from_authorized_user_file(
                config.GOOGLE_TOKEN_PATH, 
                config.GOOGLE_SCOPES
            )
        
        # Refresh or get new credentials
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    config.GOOGLE_CREDENTIALS_PATH, 
                    config.GOOGLE_SCOPES
                )
                self.creds = flow.run_local_server(port=0)
            
            # Save credentials for future use
            with open(config.GOOGLE_TOKEN_PATH, 'w') as token:
                token.write(self.creds.to_json())
        
        # Build service objects
        self.calendar_service = build('calendar', 'v3', credentials=self.creds)
        self.gmail_service = build('gmail', 'v1', credentials=self.creds)
    
    # ==================== GMAIL METHODS ====================
    
    def send_email(self, recipient: str, subject: str, body: str) -> Dict[str, Any]:
        """
        Send an email via Gmail API.
        
        Args:
            recipient: Email address of the recipient
            subject: Email subject
            body: Email body text
            
        Returns:
            Dict with status and message
        """
        if not self.authenticated:
            return {
                'success': False,
                'message': 'Google service not authenticated. Please configure credentials.json'
            }
        
        try:
            message = MIMEText(body)
            message['to'] = recipient
            message['subject'] = subject
            message['from'] = 'me'
            
            raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
            send_message = self.gmail_service.users().messages().send(
                userId='me',
                body={'raw': raw_message}
            ).execute()
            
            return {
                'success': True,
                'message': f'Email sent successfully to {recipient}',
                'message_id': send_message['id']
            }
        except HttpError as error:
            return {
                'success': False,
                'message': f'Gmail API error: {str(error)}'
            }
        except Exception as e:
            return {
                'success': False,
                'message': f'Unexpected error: {str(e)}'
            }
    
    def list_emails(self, max_results: int = 10, days_ago: int = 0) -> Dict[str, Any]:
        """
        List emails from Gmail.
        
        Args:
            max_results: Maximum number of emails to retrieve
            days_ago: Filter emails from N days ago (0 = today)
            
        Returns:
            Dict with status and list of emails
        """
        if not self.authenticated:
            return {
                'success': False,
                'message': 'Google service not authenticated. Please configure credentials.json',
                'emails': []
            }
        
        try:
            query = ''
            if days_ago > 0:
                date = (datetime.datetime.now() - datetime.timedelta(days=days_ago)).strftime('%Y/%m/%d')
                query = f'after:{date}'
            
            results = self.gmail_service.users().messages().list(
                userId='me',
                maxResults=max_results,
                q=query
            ).execute()
            
            messages = results.get('messages', [])
            email_list = []
            
            for msg in messages:
                msg_data = self.gmail_service.users().messages().get(
                    userId='me',
                    id=msg['id'],
                    format='metadata',
                    metadataHeaders=['From', 'Subject', 'Date']
                ).execute()
                
                headers = msg_data['payload']['headers']
                email_info = {
                    'id': msg['id'],
                    'from': next((h['value'] for h in headers if h['name'] == 'From'), 'Unknown'),
                    'subject': next((h['value'] for h in headers if h['name'] == 'Subject'), 'No Subject'),
                    'date': next((h['value'] for h in headers if h['name'] == 'Date'), 'Unknown')
                }
                email_list.append(email_info)
            
            return {
                'success': True,
                'count': len(email_list),
                'emails': email_list
            }
        except Exception as e:
            return {
                'success': False,
                'message': f'Error listing emails: {str(e)}',
                'emails': []
            }
    
    def delete_old_emails(self, days_ago: int = 7) -> Dict[str, Any]:
        """
        Delete emails older than specified days.
        
        Args:
            days_ago: Delete emails older than this many days
            
        Returns:
            Dict with status and count of deleted emails
        """
        if not self.authenticated:
            return {
                'success': False,
                'message': 'Google service not authenticated. Please configure credentials.json',
                'deleted_count': 0
            }
        
        try:
            date = (datetime.datetime.now() - datetime.timedelta(days=days_ago)).strftime('%Y/%m/%d')
            query = f'before:{date}'
            
            results = self.gmail_service.users().messages().list(
                userId='me',
                q=query
            ).execute()
            
            messages = results.get('messages', [])
            deleted_count = 0
            
            for msg in messages:
                self.gmail_service.users().messages().trash(
                    userId='me',
                    id=msg['id']
                ).execute()
                deleted_count += 1
            
            return {
                'success': True,
                'message': f'Moved {deleted_count} emails to trash',
                'deleted_count': deleted_count
            }
        except Exception as e:
            return {
                'success': False,
                'message': f'Error deleting emails: {str(e)}',
                'deleted_count': 0
            }
    
    # ==================== CALENDAR METHODS ====================
    
    def list_events(self, max_results: int = 10, time_min: Optional[str] = None) -> Dict[str, Any]:
        """
        List calendar events.
        
        Args:
            max_results: Maximum number of events to retrieve
            time_min: ISO format datetime for minimum time filter
            
        Returns:
            Dict with status and list of events
        """
        if not self.authenticated:
            return {
                'success': False,
                'message': 'Google service not authenticated. Please configure credentials.json',
                'events': []
            }
        
        try:
            if not time_min:
                time_min = datetime.datetime.now(datetime.timezone.utc).isoformat()
            
            events_result = self.calendar_service.events().list(
                calendarId='primary',
                timeMin=time_min,
                maxResults=max_results,
                singleEvents=True,
                orderBy='startTime'
            ).execute()
            
            events = events_result.get('items', [])
            event_list = []
            
            for event in events:
                start = event['start'].get('dateTime', event['start'].get('date'))
                end = event['end'].get('dateTime', event['end'].get('date'))
                
                event_list.append({
                    'id': event['id'],
                    'summary': event.get('summary', 'No title'),
                    'start': start,
                    'end': end,
                    'description': event.get('description', '')
                })
            
            return {
                'success': True,
                'count': len(event_list),
                'events': event_list
            }
        except Exception as e:
            return {
                'success': False,
                'message': f'Error listing events: {str(e)}',
                'events': []
            }
    
    def create_event(self, title: str, date: str, start_time: str, end_time: str, 
                    description: str = '') -> Dict[str, Any]:
        """
        Create a calendar event.
        
        Args:
            title: Event title
            date: Date in YYYY-MM-DD format
            start_time: Start time in HH:MM format
            end_time: End time in HH:MM format
            description: Event description
            
        Returns:
            Dict with status and event details
        """
        if not self.authenticated:
            return {
                'success': False,
                'message': 'Google service not authenticated. Please configure credentials.json'
            }
        
        try:
            # Parse datetime
            start_datetime = datetime.datetime.strptime(f"{date} {start_time}", "%Y-%m-%d %H:%M")
            end_datetime = datetime.datetime.strptime(f"{date} {end_time}", "%Y-%m-%d %H:%M")
            
            # Validate times
            if end_datetime <= start_datetime:
                return {
                    'success': False,
                    'message': 'End time must be after start time'
                }
            
            # Create event
            event = {
                'summary': title,
                'description': description,
                'start': {
                    'dateTime': start_datetime.astimezone().isoformat(),
                    'timeZone': config.CALENDAR_TIMEZONE,
                },
                'end': {
                    'dateTime': end_datetime.astimezone().isoformat(),
                    'timeZone': config.CALENDAR_TIMEZONE,
                }
            }
            
            created_event = self.calendar_service.events().insert(
                calendarId='primary',
                body=event
            ).execute()
            
            return {
                'success': True,
                'message': f'Event created: {title}',
                'event_id': created_event['id'],
                'link': created_event.get('htmlLink', '')
            }
        except ValueError as e:
            return {
                'success': False,
                'message': f'Invalid date/time format: {str(e)}'
            }
        except Exception as e:
            return {
                'success': False,
                'message': f'Error creating event: {str(e)}'
            }
    
    def delete_events_by_date(self, date: str) -> Dict[str, Any]:
        """
        Delete all events on a specific date.
        
        Args:
            date: Date in YYYY-MM-DD format
            
        Returns:
            Dict with status and count of deleted events
        """
        if not self.authenticated:
            return {
                'success': False,
                'message': 'Google service not authenticated. Please configure credentials.json',
                'deleted_count': 0
            }
        
        try:
            # Parse date
            target_date = datetime.datetime.strptime(date, "%Y-%m-%d")
            time_min = target_date.replace(hour=0, minute=0, second=0).astimezone().isoformat()
            time_max = target_date.replace(hour=23, minute=59, second=59).astimezone().isoformat()
            
            # Get events for the date
            events_result = self.calendar_service.events().list(
                calendarId='primary',
                timeMin=time_min,
                timeMax=time_max,
                singleEvents=True
            ).execute()
            
            events = events_result.get('items', [])
            deleted_count = 0
            
            for event in events:
                self.calendar_service.events().delete(
                    calendarId='primary',
                    eventId=event['id']
                ).execute()
                deleted_count += 1
            
            return {
                'success': True,
                'message': f'Deleted {deleted_count} events on {date}',
                'deleted_count': deleted_count
            }
        except ValueError as e:
            return {
                'success': False,
                'message': f'Invalid date format: {str(e)}',
                'deleted_count': 0
            }
        except Exception as e:
            return {
                'success': False,
                'message': f'Error deleting events: {str(e)}',
                'deleted_count': 0
            }


# Global service instance (singleton)
_google_service = None

def get_google_service() -> GoogleService:
    """Get or create the Google service instance."""
    global _google_service
    if _google_service is None:
        _google_service = GoogleService()
    return _google_service
