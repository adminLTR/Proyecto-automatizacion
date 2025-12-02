#!/usr/bin/env python3
"""Debug script to find why the server exits"""
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

print("=" * 60)
print("DEBUG: Script started")
print("=" * 60)

try:
    print("\nDEBUG: Importing Flask...")
    from flask import Flask
    print("✅ Flask imported")
    
    print("\nDEBUG: Creating simple Flask app...")
    app = Flask(__name__)
    print("✅ Flask app created")
    
    print("\nDEBUG: Adding route...")
    @app.route('/')
    def home():
        return "Hello!"
    print("✅ Route added")
    
    print("\nDEBUG: Starting server...")
    print("=" * 60)
    
    # Use the exact same configuration as start.py
    from app.config import config
    
    app.run(
        host=config.APP_HOST,
        port=config.APP_PORT,
        debug=False,
        use_reloader=False,
        threaded=True
    )
    
    print("\nDEBUG: After app.run()")
    
except Exception as e:
    print(f"\n❌ DEBUG ERROR: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
