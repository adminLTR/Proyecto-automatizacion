"""
Application initialization and factory.
"""
from flask import Flask
import logging
import sys

from app.config import config
from app.views import webhook_bp


def create_app():
    """
    Create and configure the Flask application.
    
    Returns:
        Flask: Configured Flask application instance
    """
    # Create Flask app
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object(config)
    
    # Setup logging
    setup_logging(app)
    
    # Validate configuration (non-blocking)
    try:
        config.validate()
        app.logger.info("Configuration validated successfully")
    except Exception as e:
        app.logger.warning(f"Configuration validation warning: {e}")
        # Don't exit, just warn
    
    # Register blueprints
    app.register_blueprint(webhook_bp)
    
    # Log startup
    app.logger.info("Application initialized successfully")
    app.logger.info(f"Running in {config.FLASK_ENV} mode")
    
    return app


def setup_logging(app):
    """
    Configure application logging.
    
    Args:
        app: Flask application instance
    """
    # Set log level from config
    log_level = getattr(logging, config.LOG_LEVEL.upper(), logging.INFO)
    
    # Configure root logger
    logging.basicConfig(
        level=log_level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(sys.stdout)
        ]
    )
    
    # Set Flask logger level
    app.logger.setLevel(log_level)
    
    # Reduce noise from third-party libraries
    logging.getLogger('werkzeug').setLevel(logging.WARNING)
    logging.getLogger('urllib3').setLevel(logging.WARNING)
