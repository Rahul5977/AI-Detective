"""
Main Flask application
"""

from flask import Flask
from flask_cors import CORS
from api.routes import api
from routes.ai_detective import ai_detective_bp

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend

# Register blueprints
app.register_blueprint(api, url_prefix='/api')
app.register_blueprint(ai_detective_bp, url_prefix='/api/ai')  # Add this line

@app.route('/')
def home():
    return {
        'message': 'AI Detective CSP API',
        'status': 'running',
        'version': '1.0'
    }

if __name__ == '__main__':
    print("=" * 50)
    print("🔍 AI DETECTIVE - CSP Investigation System")
    print("=" * 50)
    print("🚀 Server starting...")
    print("📍 URL: http://localhost:5002")
    print("📚 API Docs: http://localhost:5002/api")
    print("=" * 50)
    print("\nAvailable endpoints:")
    print("  POST /api/game/start       - Start new game")
    print("  POST /api/game/action      - Take action")
    print("  POST /api/ai/suggest       - Get A* suggestion")
    print("  POST /api/ai/minimax       - Get Minimax strategy")
    print("  POST /api/game/accuse      - Make accusation")
    print("\nPress CTRL+C to stop\n")
    
    app.run(debug=True, port=5002, host='0.0.0.0')