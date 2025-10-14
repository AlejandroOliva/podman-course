from flask import Flask, jsonify
from flask_cors import CORS
import psycopg2
import os
import time

app = Flask(__name__)
CORS(app)

DATABASE_URL = os.getenv('DATABASE_URL')

def get_db():
    return psycopg2.connect(DATABASE_URL)

def init_db():
    """Initialize database"""
    max_retries = 5
    for attempt in range(max_retries):
        try:
            conn = get_db()
            cur = conn.cursor()
            
            # Create table if not exists
            cur.execute("""
                CREATE TABLE IF NOT EXISTS items (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(100),
                    description TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Insert sample data if table is empty
            cur.execute("SELECT COUNT(*) FROM items")
            if cur.fetchone()[0] == 0:
                cur.execute("""
                    INSERT INTO items (name, description) VALUES
                    ('Item 1', 'First sample item'),
                    ('Item 2', 'Second sample item'),
                    ('Item 3', 'Third sample item')
                """)
            
            conn.commit()
            cur.close()
            conn.close()
            print("✅ Database initialized")
            return
        except Exception as e:
            print(f"❌ Error connecting to DB (attempt {attempt+1}/{max_retries}): {e}")
            time.sleep(2)
    
    print("❌ Could not initialize database")

@app.route('/')
def home():
    return jsonify({
        "message": "Backend API - Complete Stack",
        "version": "1.0",
        "endpoints": [
            "/",
            "/api/data",
            "/api/count",
            "/health"
        ]
    })

@app.route('/api/data')
def get_data():
    try:
        conn = get_db()
        cur = conn.cursor()
        cur.execute("SELECT id, name, description, created_at FROM items")
        rows = cur.fetchall()
        
        items = []
        for row in rows:
            items.append({
                "id": row[0],
                "name": row[1],
                "description": row[2],
                "created_at": str(row[3])
            })
        
        cur.close()
        conn.close()
        
        return jsonify({
            "success": True,
            "data": items,
            "count": len(items)
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route('/api/count')
def get_count():
    try:
        conn = get_db()
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM items")
        count = cur.fetchone()[0]
        cur.close()
        conn.close()
        
        return jsonify({
            "success": True,
            "count": count
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route('/health')
def health():
    try:
        conn = get_db()
        conn.close()
        return jsonify({"status": "healthy", "db": "connected"})
    except:
        return jsonify({"status": "unhealthy", "db": "disconnected"}), 500

if __name__ == '__main__':
    print("🚀 Starting Backend API...")
    init_db()
    app.run(host='0.0.0.0', port=5000, debug=False)
