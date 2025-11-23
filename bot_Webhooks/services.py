import requests
from config import settings
from keyboards import keyboard_main


def send_message(chat_id, text):
    payload = {
        "chat_id": chat_id,
        "text": text
    }
    requests.post(f"{settings.telegram_api}/sendMessage", json=payload)


def send_keyboard(chat_id, text):
    payload = {
        "chat_id": chat_id,
        "text": text,
        "reply_markup": keyboard_main
    }
    requests.post(f"{settings.telegram_api}/sendMessage", json=payload)
