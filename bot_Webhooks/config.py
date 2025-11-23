import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    BOT_TOKEN = os.getenv("BOT_TOKEN")
    BASE_URL = os.getenv("BASE_URL")       # https://api.telegram.org/bot
    BACKEND_URL = os.getenv("BACKEND_URL")
    NGROK_URL = os.getenv("NGROK_URL")
    PORT = int(os.getenv("PORT", 8001))

    @property
    def telegram_api(self):
        return f"{self.BASE_URL}{self.BOT_TOKEN}"

settings = Settings()
