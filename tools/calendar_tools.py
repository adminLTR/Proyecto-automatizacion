import os.path
import datetime
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/calendar']
ZONA_HORARIA = 'America/Lima'

# 1. CONEXIÓN Y AUTH 
def conectar_google():
    """
    Autentica con Google y devuelve el servicio de Calendar.
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
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
            
    return build('calendar', 'v3', credentials=creds)

# 2. Lógica interna
def construir_iso(fecha_str, hora_str):
    """Convierte fecha (YYYY-MM-DD) y hora (HH:MM) a datetime aware."""
    dt_str = f"{fecha_str} {hora_str}"
    dt_obj = datetime.datetime.strptime(dt_str, "%Y-%m-%d %H:%M")
    return dt_obj.astimezone()

def formatear_respuesta(evento):
    """Devuelve un string limpio con los detalles del evento."""
    start = evento['start'].get('dateTime', evento['start'].get('date'))
    end = evento['end'].get('dateTime', evento['end'].get('date'))
    summary = evento.get('summary', '(Sin título)')
    try:
        dt_ini = datetime.datetime.fromisoformat(start)
        dt_fin = datetime.datetime.fromisoformat(end)
        return f"'{summary}' | 🕒 {dt_ini.strftime('%Y-%m-%d %H:%M')} - {dt_fin.strftime('%H:%M')} | ID: {evento['id']}"
    except:
        return f"'{summary}' | {start} | ID: {evento['id']}"


# HERRAMIENTAS PARA EL AGENTE (TOOLS)

def tool_listar_eventos(service):
    """
    Lista los próximos 10 eventos del calendario.
    Retorna un string con la lista formateada.
    """
    now_utc = datetime.datetime.now(datetime.timezone.utc)
    
    try:
        events_result = service.events().list(
            calendarId='primary', timeMin=now_utc.isoformat(),
            maxResults=10, singleEvents=True, orderBy='startTime'
        ).execute()
        events = events_result.get('items', [])

        if not events:
            return "No se encontraron eventos próximos en tu calendario."
        
        resultado = "**Tus próximos eventos:**\n"
        for event in events:
            resultado += f"- {formatear_respuesta(event)}\n"
            
        return resultado # El Agente leerá este texto

    except Exception as e:
        return f"Error al leer el calendario: {str(e)}"


def tool_crear_evento(service, titulo, fecha, hora_inicio, hora_fin):
    """
    Crea un evento nuevo.
    Args:
        titulo (str): Nombre de la reunión.
        fecha (str): Formato YYYY-MM-DD (ej. 2025-11-25).
        hora_inicio (str): Formato HH:MM (ej. 14:00).
        hora_fin (str): Formato HH:MM (ej. 15:00).
    """
    try:
        dt_inicio = construir_iso(fecha, hora_inicio)
        dt_fin = construir_iso(fecha, hora_fin)

        # Validación lógica
        if dt_fin <= dt_inicio:
            return f" Error: La hora de fin ({hora_fin}) no puede ser antes o igual al inicio ({hora_inicio})."

        evento = {
            'summary': titulo,
            'start': {'dateTime': dt_inicio.isoformat(), 'timeZone': ZONA_HORARIA},
            'end': {'dateTime': dt_fin.isoformat(), 'timeZone': ZONA_HORARIA},
        }
        
        creado = service.events().insert(calendarId='primary', body=evento).execute()
        return f"Evento creado exitosamente:\n{formatear_respuesta(creado)}"

    except ValueError:
        return "Error de formato: Asegúrate de usar fecha YYYY-MM-DD y hora HH:MM."
    except Exception as e:
        return f"Error inesperado al crear: {str(e)}"


def tool_actualizar_evento(service, event_id, nuevo_titulo=None, nueva_fecha=None, nueva_hora_inicio=None, nueva_hora_fin=None):
    """
    Actualiza un evento existente. Solo requiere el event_id y los campos que cambian.
    Args:
        event_id (str): El ID único del evento (obtenido al listar).
        nuevo_titulo (str, optional): Nuevo nombre.
        nueva_fecha, nueva_hora_inicio, nueva_hora_fin: (Opcionales).
    """
    try:
        # 1. Obtenemos el evento actual para no perder datos
        evento_original = service.events().get(calendarId='primary', eventId=event_id).execute()
        
        cuerpo_patch = {}
        
        # Si hay cambio de título
        if nuevo_titulo:
            cuerpo_patch['summary'] = nuevo_titulo

        # Si hay cambios de horario, necesitamos recalcular todo el bloque
        if nueva_fecha or nueva_hora_inicio or nueva_hora_fin:
            start_actual = evento_original['start'].get('dateTime')
            end_actual = evento_original['end'].get('dateTime')
            
            # Convertimos a objetos
            dt_ini = datetime.datetime.fromisoformat(start_actual)
            dt_fin = datetime.datetime.fromisoformat(end_actual)

            # Aplicamos cambios si existen
            if nueva_fecha:
                y, m, d = map(int, nueva_fecha.split('-'))
                dt_ini = dt_ini.replace(year=y, month=m, day=d)
                dt_fin = dt_fin.replace(year=y, month=m, day=d)
            
            if nueva_hora_inicio:
                h, m = map(int, nueva_hora_inicio.split(':'))
                dt_ini = dt_ini.replace(hour=h, minute=m)
                
            if nueva_hora_fin:
                h, m = map(int, nueva_hora_fin.split(':'))
                dt_fin = dt_fin.replace(hour=h, minute=m)

            # Validación
            if dt_fin <= dt_ini:
                return "Error: El nuevo horario de fin es anterior al de inicio."

            cuerpo_patch['start'] = {'dateTime': dt_ini.isoformat(), 'timeZone': ZONA_HORARIA}
            cuerpo_patch['end'] = {'dateTime': dt_fin.isoformat(), 'timeZone': ZONA_HORARIA}

        # Ejecutar actualización
        actualizado = service.events().patch(calendarId='primary', eventId=event_id, body=cuerpo_patch).execute()
        return f"Actualización correcta:\n{formatear_respuesta(actualizado)}"

    except Exception as e:
        return f"Error al actualizar (Verifica que el ID sea correcto): {str(e)}"


def tool_eliminar_evento(service, event_id):
    """Elimina un evento dado su ID."""
    try:
        service.events().delete(calendarId='primary', eventId=event_id).execute()
        return f"Evento con ID {event_id} eliminado correctamente."
    except Exception as e:
        return f"Error al eliminar (¿El ID es correcto?): {str(e)}"