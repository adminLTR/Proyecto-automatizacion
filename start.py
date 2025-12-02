"""
Simple start script for testing.
"""
import os
import sys

# Add the project directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Create .env if it doesn't exist
if not os.path.exists('.env'):
    print("📝 Creating .env file from template...")
    with open('.env.example', 'r') as f:
        content = f.read()
    with open('.env', 'w') as f:
        f.write(content)
    print("✅ .env file created. Please edit it with your credentials.")
    print()

print("🚀 Starting Flask application...")
print()

if __name__ == '__main__':
    try:
        from app import create_app
        from app.config import config
        
        app = create_app()
        
        print(f"✅ Application initialized successfully!")
        print(f"🌐 Server starting on http://{config.APP_HOST}:{config.APP_PORT}")
        print(f"📱 Send messages to your Telegram bot to test")
        print(f"🔍 Health check: http://localhost:{config.APP_PORT}/health")
        print()
        print("⚠️  Note: If you haven't configured credentials.json and token.json,")
        print("   the Google features won't work yet, but the server will run.")
        print()
        print("Press Ctrl+C to stop")
        print("-" * 70)
        print()
        
        app.run(
            host=config.APP_HOST,
            port=config.APP_PORT,
            debug=False,  # Debug OFF para evitar problemas
            use_reloader=False,  # Disable reloader to avoid double initialization
            threaded=True  # Allow multiple connections
        )
        
    except KeyboardInterrupt:
        print("\n\n🛑 Server stopped by user")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error starting application: {e}")
        print()
        print("Common issues:")
        print("1. Make sure .env file exists and has TELEGRAM_BOT_TOKEN")
        print("2. Make sure credentials.json exists (download from Google Cloud)")
        print("3. Check that all dependencies are installed: pip install -r requirements.txt")
        print()
        import traceback
        traceback.print_exc()
        sys.exit(1)
