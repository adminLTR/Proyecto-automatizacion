"""
Application entry point.
Run this file to start the Flask server.
"""
from app import create_app
from app.config import config


def main():
    """Main function to run the Flask application."""
    # Create Flask app
    app = create_app()
    
    # Run the application
    app.run(
        host=config.APP_HOST,
        port=config.APP_PORT,
        debug=config.DEBUG
    )


if __name__ == '__main__':
    main()
