import time
import requests
from config import BASE_URL
from services import send_message, send_keyboard, get_updates

# -----------------------------------------
# 1) Determinar qué botón presionó el usuario
# -----------------------------------------

def determinar_consulta(texto):
    texto = texto.lower()

    if texto == "horario de hoy":
        return {"consulta": "horario_hoy"}

    if texto == "horario de mañana":
        return {"consulta": "horario_manana"}

    if texto == "mi semana":
        return {"consulta": "semana"}

    if texto == "sugerencias ia":
        return {"consulta": "sugerencias"}

    return None


# -------------------------------------------------------
# 2) Enviar el JSON estándar al backend que procesa datos
# -------------------------------------------------------

def enviar_consulta_backend(chat_id, user_id, consulta):
    payload = {
        "tipo": "consulta",
        "consulta": consulta,
        "user_id": user_id,
        "fuente": "telegram"
    }

    try:
        resp = requests.post("http://localhost:7000/consulta", json=payload)
        return resp.json()
    except:
        return {"tipo": "error", "detalle": f"No se pudo conectar con el backend"}


# ------------------------------------------
# 3) Procesar respuesta que devuelve backend
# ------------------------------------------

def procesar_respuesta(chat_id, json_resp):

    tipo = json_resp.get("tipo")

    if tipo == "respuesta_horario":
        actividades = "\n".join(
            [f"- {a['hora']}: {a['texto']}" for a in json_resp["actividades"]]
        )
        send_message(chat_id, f"{json_resp['dia']}:\n\n{actividades}")
        return

    if tipo == "respuesta_semana":
        send_message(chat_id, "Resumen semanal:\n\n" + json_resp["resumen"])
        return

    if tipo == "respuesta_sugerencias":
        sug = "\n".join([f"• {s}" for s in json_resp["sugerencias"]])
        send_message(chat_id, f"Sugerencias IA:\n\n{sug}")
        return

    if tipo == "error":
        send_message(chat_id, "Error:\n" + json_resp["detalle"])
        return

    send_message(chat_id, "No se pudo interpretar la respuesta del backend.")


# -----------------------
# 4) Bucle principal
# -----------------------

def main():
    offset = None
    print("🤖 Bot Telegram MVP 2 Iniciado...")

    while True:
        updates = get_updates(offset)

        if "result" in updates:
            for upd in updates["result"]:
                offset = upd["update_id"] + 1

                if "message" not in upd:
                    continue

                msg = upd["message"]
                chat_id = msg["chat"]["id"]
                user_id = msg["from"]["id"]
                texto = msg.get("text", "")

                # Si es primera vez → enviar teclado
                if texto == "/start":
                    send_keyboard(chat_id, "Bienvenido, selecciona una opción.")
                    continue

                consulta = determinar_consulta(texto)

                if consulta:
                    json_resp = enviar_consulta_backend(chat_id, user_id, consulta["consulta"])
                    procesar_respuesta(chat_id, json_resp)
                else:
                    send_keyboard(chat_id, "Selecciona una opción válida.")

        time.sleep(0.5)


if __name__ == "__main__":
    main()
