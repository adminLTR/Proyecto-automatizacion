"""
Configuration module for the application.
Loads environment variables and provides application settings.
"""
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Config:
    """Base configuration class."""
    
    # Flask Configuration
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    FLASK_ENV = os.getenv('FLASK_ENV', 'development')
    DEBUG = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    
    # Application Configuration
    APP_HOST = os.getenv('APP_HOST', '0.0.0.0')
    APP_PORT = int(os.getenv('APP_PORT', 5000))
    
    # Telegram Configuration
    TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
    TELEGRAM_BASE_URL = os.getenv('TELEGRAM_BASE_URL', 'https://api.telegram.org/bot')
    USE_WEBHOOK = os.getenv('USE_WEBHOOK', 'False').lower() == 'true'
    WEBHOOK_URL = os.getenv('WEBHOOK_URL', '')
    
    # Google API Configuration
    GOOGLE_CREDENTIALS_PATH = os.getenv('GOOGLE_CREDENTIALS_PATH', 'credentials.json')
    GOOGLE_TOKEN_PATH = os.getenv('GOOGLE_TOKEN_PATH', 'token.json')
    GOOGLE_SCOPES = [
        'https://www.googleapis.com/auth/calendar',
        'https://www.googleapis.com/auth/gmail.send',
        'https://www.googleapis.com/auth/gmail.readonly',
        'https://www.googleapis.com/auth/gmail.modify'
    ]
    
    # Email Configuration
    DEFAULT_EMAIL_RECIPIENT = os.getenv('DEFAULT_EMAIL_RECIPIENT', 'default@example.com')
    EMAIL_DELETE_DAYS_AGO = int(os.getenv('EMAIL_DELETE_DAYS_AGO', 7))
    
    # Calendar Configuration
    CALENDAR_TIMEZONE = os.getenv('CALENDAR_TIMEZONE', 'America/Lima')
    
    # Logging
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    
    @property
    def telegram_api_url(self):
        """Get the full Telegram API URL."""
        if not self.TELEGRAM_BOT_TOKEN:
            raise ValueError("TELEGRAM_BOT_TOKEN is not set in environment variables")
        return f"{self.TELEGRAM_BASE_URL}{self.TELEGRAM_BOT_TOKEN}"
    
    def validate(self):
        """Validate that required configuration is present."""
        errors = []
        warnings = []
        
        if not self.TELEGRAM_BOT_TOKEN:
            warnings.append("TELEGRAM_BOT_TOKEN is not set - set it in .env file")
        
        if not os.path.exists(self.GOOGLE_CREDENTIALS_PATH):
            warnings.append(f"Google credentials file not found: {self.GOOGLE_CREDENTIALS_PATH} - download from Google Cloud Console")
        
        if warnings:
            print("\n⚠️  WARNING: Missing configuration:")
            for warning in warnings:
                print(f"   - {warning}")
            print("\n   The app will start but some features may not work until configured.\n")
        
        return True


# Create a global config instance
config = Config()
