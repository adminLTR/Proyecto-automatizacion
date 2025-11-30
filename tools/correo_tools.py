import os
import base64
from email.mime.text import MIMEText
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# --- CONFIGURACIÓN DE RUTAS ---
TOOLS_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(TOOLS_DIR)
TOKEN_PATH = os.path.join(ROOT_DIR, 'token.json')

# ---------------------------------------------------------
# 1. CONEXIÓN (Reutiliza el token generado por calendar_tools)
# ---------------------------------------------------------
def conectar_gmail():
    """
    Carga el token existente y conecta con Gmail.
    NO genera token nuevo (eso lo hace calendar_tools).
    """
    if os.path.exists(TOKEN_PATH):
        creds = Credentials.from_authorized_user_file(TOKEN_PATH)
        return build('gmail', 'v1', credentials=creds)
    else:
        print("⚠️ No se encontró token.json. Ejecuta primero la autenticación.")
        return None

# ---------------------------------------------------------
# 2. LEER CORREOS (Nueva funcionalidad)
# ---------------------------------------------------------
def tool_leer_correos(service, cantidad=5):
    """
    Lista los últimos correos no leídos de la bandeja de entrada.
    """
    try:
        # Buscamos mensajes en INBOX que no estén leídos
        results = service.users().messages().list(
            userId='me', 
            labelIds=['INBOX'], 
            q='is:unread', 
            maxResults=cantidad
        ).execute()
        
        messages = results.get('messages', [])

        if not messages:
            return "📭 No tienes correos nuevos sin leer."

        respuesta = "📧 **Tus últimos correos sin leer:**\n\n"

        for msg in messages:
            txt = service.users().messages().get(userId='me', id=msg['id']).execute()
            payload = txt['payload']
            headers = payload.get('headers', [])

            subject = next((h['value'] for h in headers if h['name'] == 'Subject'), '(Sin Asunto)')
            sender = next((h['value'] for h in headers if h['name'] == 'From'), '(Desconocido)')
            
            if "<" in sender:
                sender = sender.split("<")[0].strip()

            respuesta += f"• **De:** {sender}\n  **Asunto:** {subject}\n\n"

        return respuesta

    except Exception as e:
        return f"❌ Error al leer correos: {str(e)}"

# ---------------------------------------------------------
# 3. ENVIAR CORREOS (Tu código original)
# ---------------------------------------------------------
def crear_mensaje(destinatario, asunto, cuerpo_texto):
    message = MIMEText(cuerpo_texto)
    message['to'] = destinatario
    message['subject'] = asunto    
    message['from'] = 'me'
    raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
    return {'raw': raw_message}

def tool_enviar_correo(service_gmail, destinatario, asunto, cuerpo):
    try:
        mensaje_body = crear_mensaje(destinatario, asunto, cuerpo)
        send_message = service_gmail.users().messages().send(userId='me', body=mensaje_body).execute()        
        return f"Correo enviado exitosamente a {destinatario}. ID: {send_message['id']}"
    except HttpError as error:
        return f"Error de Google API: {error}"
    except Exception as ex:
        return f"Error inesperado: {str(ex)}"