"""Test if Flask works"""
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({"message": "Flask is working!"})

@app.route('/health')
def health():
    return jsonify({"status": "healthy"})

if __name__ == '__main__':
    print("Starting test Flask server on http://localhost:5000")
    app.run(host='0.0.0.0', port=5000, debug=False)
