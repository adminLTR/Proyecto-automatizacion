import requests
from config import BASE_URL

# ----------------------------------------
# Enviar mensaje normal
# ----------------------------------------
def send_message(chat_id, text):
    payload = {
        "chat_id": chat_id,
        "text": text
    }
    requests.post(f"{BASE_URL}/sendMessage", json=payload)

# ----------------------------------------
# Enviar teclado de botones
# ----------------------------------------
def send_keyboard(chat_id, text):
    keyboard = {
        "keyboard": [
            [{"text": "Horario de hoy"}],
            [{"text": "Horario de mañana"}],
            [{"text": "Mi semana"}],
            [{"text": "Sugerencias IA"}]
        ],
        "resize_keyboard": True
    }

    payload = {
        "chat_id": chat_id,
        "text": text,
        "reply_markup": keyboard
    }

    requests.post(f"{BASE_URL}/sendMessage", json=payload)

# ----------------------------------------
# Leer mensajes del usuario (long polling)
# ----------------------------------------
def get_updates(offset=None):
    params = {"timeout": 100, "offset": offset}
    resp = requests.get(f"{BASE_URL}/getUpdates", params=params)
    return resp.json()
