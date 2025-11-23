import requests
from config import settings

WEBHOOK_URL = f"{settings.NGROK_URL}/webhook/{settings.BOT_TOKEN}"

def set_webhook():
    url = f"https://api.telegram.org/bot{settings.BOT_TOKEN}/setWebhook"
    data = {"url": WEBHOOK_URL}

    response = requests.post(url, data=data)
    print("Respuesta Telegram:", response.json())

if __name__ == "__main__":
    set_webhook()
