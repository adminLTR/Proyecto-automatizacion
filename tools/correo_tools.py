import base64
from email.mime.text import MIMEText
from googleapiclient.errors import HttpError

def crear_mensaje(destinatario, asunto, cuerpo_texto):
    """
    Crea un objeto MIMEText y lo codifica en base64url para la API de Gmail.
    """
    message = MIMEText(cuerpo_texto)
    message['to'] = destinatario
    message['subject'] = asunto    
    message['from'] = 'me' # 'me' indica que el remitente es el usuario autenticado
    
    # Codificación necesaria para Gmail API
    raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
    return {'raw': raw_message}

def tool_enviar_correo(service_gmail, destinatario, asunto, cuerpo):
    """
    Envía un correo electrónico usando la cuenta de Gmail autenticada.
    
    Args:
        service_gmail: El objeto de servicio de Gmail (obtenido en Auth).
        destinatario (str): Email del receptor (ej: "cliente@ejemplo.com").
        asunto (str): Título del correo.
        cuerpo (str): Contenido del mensaje.
    """
    try:
        mensaje_body = crear_mensaje(destinatario, asunto, cuerpo)
        send_message = service_gmail.users().messages().send(userId='me', body=mensaje_body).execute()        
       
        return f"Correo enviado exitosamente a {destinatario}. ID del mensaje: {send_message['id']}"
    except HttpError as error:
        return f"Error de Google API al enviar correo: {error}"
    except Exception as ex:
        return f"Error inesperado al enviar correo: {str(ex)}"