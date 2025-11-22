import requests
import time
from config import BASE_URL

# ------------------------------
# Funciones principales del MVP
# ------------------------------

def send_message(chat_id, text):
    """Envia un mensaje simple"""
    endpoint = f"{BASE_URL}/sendMessage"
    requests.get(endpoint, params={"chat_id": chat_id, "text": text})


def get_updates(offset=None):
    """Obtiene mensajes del bot"""
    endpoint = f"{BASE_URL}/getUpdates"
    params = {"timeout": 100, "offset": offset}
    return requests.get(endpoint, params=params).json()


# -----------------------------------------------
# PROCESAR MENSAJE → RESPUESTA EN FORMATO JSON
# -----------------------------------------------

def procesar(texto):
    """Devuelve un JSON simple para decidir la respuesta"""
    text_low = texto.lower()

    if text_low in ["hola", "hi", "buenas", "hey"]:
        return {
            "tipo": "saludo",
            "respuesta": "Hola 👋, soy tu bot. ¿Qué necesitas?"
        }

    if "horario" in text_low or "agenda" in text_low:
        return {
            "tipo": "consulta",
            "respuesta": "Entendido. Consultaré tu horario. (Funcionalidad próximamente)"
        }

    return {
        "tipo": "desconocido",
        "respuesta": "No entiendo tu mensaje. Intenta con 'hola' o 'horario'."
    }


# -----------------------------
# BUCLE PRINCIPAL DEL BOT MVP
# -----------------------------

def main():
    offset = None
    print("🤖 Bot Telegram MVP iniciado. Escuchando mensajes...")

    while True:
        updates = get_updates(offset)

        if "result" in updates:
            for upd in updates["result"]:
                offset = upd["update_id"] + 1

                if "message" not in upd:
                    continue

                msg = upd["message"]
                chat_id = msg["chat"]["id"]
                texto = msg.get("text", "")

                # Procesar el mensaje en JSON
                respuesta_json = procesar(texto)

                # Enviar la respuesta del JSON
                send_message(chat_id, respuesta_json["respuesta"])

        time.sleep(0.5)


if __name__ == "__main__":
    main()
