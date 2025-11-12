"""
Main Flask application
"""

from flask import Flask, jsonify
from flask_cors import CORS
from routes.game import game_bp
from routes.ai import ai_bp

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})

# Register blueprints
app.register_blueprint(game_bp, url_prefix='/api/game')
app.register_blueprint(ai_bp, url_prefix='/api/ai')

@app.route('/')
def home():
    return jsonify({
        "message": "AI Detective Backend API", 
        "status": "running", 
        "version": "2.0"
    })

@app.route('/health')
def health():
    return jsonify({
        "status": "healthy", 
        "port": 5002
    })

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "success": False,
        "message": "Endpoint not found"
    }), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        "success": False,
        "message": "Internal server error"
    }), 500

if __name__ == '__main__':
    print("🕵️ Starting AI Detective Backend Server...")
    print("📡 Server running on http://localhost:5002")
    print("✅ CORS enabled for all origins")
    app.run(debug=True, port=5002, host='0.0.0.0')