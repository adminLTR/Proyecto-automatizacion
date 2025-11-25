"""
WSGI entry point for production deployment.
This file is used by gunicorn.
"""
from app import create_app

app = create_app()

if __name__ == '__main__':
    app.run()
