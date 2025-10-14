from flask import Flask, jsonify
from datetime import datetime
import os

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({
        "message": "Welcome to the Flask API with Podman!",
        "version": "1.0",
        "endpoints": [
            "/",
            "/api/hello",
            "/api/time",
            "/health"
        ]
    })

@app.route('/api/hello')
def hello():
    return jsonify({
        "message": "Hello from Flask!",
        "container": os.getenv("HOSTNAME", "unknown"),
        "framework": "Flask",
        "runtime": "Podman"
    })

@app.route('/api/time')
def get_time():
    now = datetime.now()
    return jsonify({
        "timestamp": now.isoformat(),
        "date": now.strftime("%Y-%m-%d"),
        "time": now.strftime("%H:%M:%S"),
        "day": now.strftime("%A")
    })

@app.route('/health')
def health():
    return jsonify({
        "status": "healthy",
        "service": "flask-api"
    })

if __name__ == '__main__':
    print("🚀 Starting Flask API...")
    print("📍 Access at: http://localhost:5000")
    app.run(host='0.0.0.0', port=5000, debug=False)
