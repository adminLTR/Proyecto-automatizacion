import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# AQUI AGREGAMOS EL SCOPE DE GMAIL
SCOPES = [
    'https://www.googleapis.com/auth/calendar',
    'https://www.googleapis.com/auth/gmail.send' 
]

def obtener_credenciales():
    """
    Maneja la autenticación y devuelve las credenciales (creds).
    Sirve tanto para Calendar como para Gmail.
    """
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        
        # Guardamos el token para la próxima
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
            
    return creds

def conectar_servicios():
    """
    Devuelve una tupla con ambos servicios listos para usar.
    """
    creds = obtener_credenciales()
    service_calendar = build('calendar', 'v3', credentials=creds)
    service_gmail = build('gmail', 'v1', credentials=creds)
    
    return service_calendar, service_gmail