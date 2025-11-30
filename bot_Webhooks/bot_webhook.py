from fastapi import FastAPI, Request
import requests
from config import settings
from services import send_message, send_keyboard

URL_CALENDAR = "http://127.0.0.1:7000/consulta"
URL_GMAIL    = "http://127.0.0.1:7002/consulta"

app = FastAPI()


# --------------------------------------
# 1. Convertir texto en "consulta" JSON
# --------------------------------------
def determinar_consulta(texto):
    t = texto.lower()

    # Mapeamos las frases a las intenciones
    if t == "horario de hoy":
        return "horario_hoy"

    if t == "horario de mañana":
        return "horario_manana"

    if t == "mi semana":
        return "semana"

    if t == "sugerencias ia":
        return "sugerencias"
    
    if "leer correos" in t:
        return "leer_correos"
    
    if "crear mensaje" in t:
        return "crear_mensaje_simulado"
        
    if "enviar correo" in t:
        return "enviar_correo_real"
    return None


# -----------------------------------------
# 2. Enviar consulta al backend (Puerto 7000)
# -----------------------------------------
def enviar_consulta_backend(chat_id, user_id, consulta):
    url_backend = f"{settings.BACKEND_URL}/consulta"

    payload = {
        "tipo": "consulta",
        "consulta": consulta,
        "user_id": user_id,
        "fuente": "telegram"
    }

    try:
        resp = requests.post(url_backend, json=payload)
        return resp.json()
    except:
        return {"tipo": "error", "detalle": "Backend no disponible"}

# -----------------------------------------
# 3. Procesar respuesta del backend
# -----------------------------------------
def procesar_respuesta(chat_id, json_resp):

    tipo = json_resp.get("tipo")

    # --- [NUEVO] SOPORTE PARA CALENDAR TOOLS ---
    if tipo == "respuesta_texto":
        send_message(chat_id, json_resp.get("mensaje"))
        return
    # -------------------------------------------

    if tipo == "respuesta_horario":
        actividades = "\n".join(
            [f"- {a['hora']}: {a['texto']}" for a in json_resp["actividades"]]
        )
        send_message(chat_id, f"{json_resp['dia']}:\n\n{actividades}")
        return

    if tipo == "respuesta_sugerencias":
        lista = "\n".join([f"• {s}" for s in json_resp["sugerencias"]])
        send_message(chat_id, f"Sugerencias IA:\n\n{lista}")
        return

    if tipo == "respuesta_semana":
        send_message(chat_id, "Resumen de semana:\n\n" + json_resp["resumen"])
        return

    if tipo == "error":
        send_message(chat_id, "Error:\n" + json_resp["detalle"])
        return

    send_message(chat_id, "No se pudo interpretar la respuesta.")


# -----------------------------------------
# 4. Endpoint Webhook (MANTENIENDO EL TOKEN)
# -----------------------------------------
@app.post(f"/webhook/{settings.BOT_TOKEN}")
async def recibir_update(request: Request):

    data = await request.json()

    if "message" not in data:
        return {"ok": True}

    msg = data["message"]
    chat_id = msg["chat"]["id"]
    user_id = msg["from"]["id"]
    texto = msg.get("text", "")

    # /start → mostrar teclado
    if texto == "/start":
        send_keyboard(chat_id, "Bienvenido, selecciona una opción.")
        return {"ok": True}

    consulta = determinar_consulta(texto)

    if consulta:
        resp = enviar_consulta_backend(chat_id, user_id, consulta)
        procesar_respuesta(chat_id, resp)
    else:
        send_keyboard(chat_id, "Selecciona una opción válida.")

    return {"ok": True}



