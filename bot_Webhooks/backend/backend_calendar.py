import sys
import os
import datetime
from datetime import timedelta
from fastapi import FastAPI, Request

# ---------------------------------------------------
# 1. CONFIGURACIÓN DE RUTAS E IMPORTACIONES
# ---------------------------------------------------
# Ajustamos el path para poder importar desde la carpeta 'tools'
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

# Importamos las herramientas de CALENDARIO
from tools.calendar_tools import conectar_google, tool_listar_eventos

# Importamos las herramientas de CORREO (Asegúrate de que correo_tools.py tenga estas funciones)
from tools.correo_tools import conectar_gmail, tool_leer_correos, tool_enviar_correo

app = FastAPI()

# Variables Globales para los servicios
calendar_service = None
gmail_service = None

# ---------------------------------------------------
# 2. EVENTO DE INICIO (CONEXIÓN)
# ---------------------------------------------------
@app.on_event("startup")
async def startup_event():
    global calendar_service, gmail_service
    print("🔌 Backend UNIFICADO iniciando en puerto 7000...")
    try:
        # Conectamos Calendar
        calendar_service = conectar_google()
        print("✅ Google Calendar conectado.")
        
        # Conectamos Gmail
        gmail_service = conectar_gmail()
        if gmail_service:
            print("✅ Gmail conectado.")
        else:
            print("⚠️ Gmail no conectado (revisar token o correo_tools.py).")
            
    except Exception as e:
        print(f"❌ Error conectando a Google: {e}")

# ---------------------------------------------------
# 3. ENDPOINT PRINCIPAL
# ---------------------------------------------------
@app.post("/consulta")
async def procesar_consulta(request: Request):
    data = await request.json()
    consulta = data.get("consulta")
    print(f"📩 Consulta recibida: {consulta}")

    # Fecha actual para cálculos
    now = datetime.datetime.now()

    # ==========================================
    # BLOQUE A: CALENDARIO
    # ==========================================
    if consulta in ["horario_hoy", "horario_manana", "semana", "sugerencias"]:
        
        if not calendar_service:
            return {"tipo": "error", "detalle": "Calendar no conectado."}

        if consulta == "horario_hoy":
            fin_hoy = now.replace(hour=23, minute=59, second=59)
            iso_inicio = now.isoformat() + 'Z'
            iso_fin = fin_hoy.isoformat() + 'Z'
            res = tool_listar_eventos(calendar_service, time_min=iso_inicio, time_max=iso_fin)
            return {"tipo": "respuesta_texto", "mensaje": f"📅 **Hoy:**\n\n{res}"}

        elif consulta == "horario_manana":
            manana = now + timedelta(days=1)
            inicio = manana.replace(hour=0, minute=0, second=0).isoformat() + 'Z'
            fin = manana.replace(hour=23, minute=59, second=59).isoformat() + 'Z'
            res = tool_listar_eventos(calendar_service, time_min=inicio, time_max=fin)
            return {"tipo": "respuesta_texto", "mensaje": f"📅 **Mañana:**\n\n{res}"}

        elif consulta == "semana":
            fin = (now + timedelta(days=7)).isoformat() + 'Z'
            inicio = now.isoformat() + 'Z'
            res = tool_listar_eventos(calendar_service, time_min=inicio, time_max=fin)
            return {"tipo": "respuesta_texto", "mensaje": f"📅 **Semana:**\n\n{res}"}
            
        elif consulta == "sugerencias":
             return {"tipo": "respuesta_texto", "mensaje": "🤖 Sugerencia: Revisa tus correos pendientes."}

    # ==========================================
    # BLOQUE B: GMAIL
    # ==========================================
    elif consulta in ["leer_correos", "crear_mensaje_simulado", "enviar_correo_real"]:
        
        if not gmail_service:
            return {"tipo": "error", "detalle": "Gmail no conectado."}

        if consulta == "leer_correos":
            return {"tipo": "respuesta_texto", "mensaje": tool_leer_correos(gmail_service)}

        elif consulta == "crear_mensaje_simulado":
            mi_correo = "jose.parrales@unmsm.edu.pe" 
            msg = (
                "📝 **Borrador:**\n\n"
                f"**Para:** {mi_correo}\n"
                "**Asunto:** Prueba\n"
                "**Cuerpo:** Hola, prueba de envío.\n\n"
                "👉 Presiona 'Enviar Correo' para confirmar."
            )
            return {"tipo": "respuesta_texto", "mensaje": msg}

        elif consulta == "enviar_correo_real":
            destinatario = "jose.parrales@unmsm.edu.pe"
            asunto = "Prueba"
            cuerpo = "Hola, esto es una prueba enviada desde el Bot."
            print(f"📤 Intentando enviar a {destinatario}...")
            res = tool_enviar_correo(gmail_service, destinatario, asunto, cuerpo)
            return {"tipo": "respuesta_texto", "mensaje": f"✅ {res}"}

    # ==========================================
    # BLOQUE C: ERROR / DESCONOCIDO
    # ==========================================
    return {"tipo": "error", "detalle": "Consulta no reconocida."}