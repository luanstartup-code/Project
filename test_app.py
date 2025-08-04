#!/usr/bin/env python3
"""
🎬 CineAI - Teste Backend Simplificado
Versão mínima para testar se o Flask funciona
"""

import os
from flask import Flask, jsonify
from flask_cors import CORS

def create_test_app():
    app = Flask(__name__)
    
    # CORS simples
    CORS(app, origins=['*'])
    
    # Configuração básica
    app.config['SECRET_KEY'] = 'test-secret-key'
    app.config['DEBUG'] = True
    
    @app.route('/')
    def home():
        return jsonify({
            'status': 'ok',
            'message': '🎬 CineAI Test Backend is running!',
            'version': '1.0.0-test'
        })
    
    @app.route('/api/health')
    def health():
        return jsonify({
            'status': 'healthy',
            'message': 'API funcionando!',
            'environment': 'test'
        })
    
    @app.route('/api/test')
    def test():
        return jsonify({
            'backend': '✅ Working',
            'flask': '✅ OK',
            'cors': '✅ Enabled',
            'apis': {
                'openai': '✅ Mock' if os.getenv('OPENAI_API_KEY') else '❌ Not configured',
                'gemini': '✅ Mock' if os.getenv('GEMINI_API_KEY') else '❌ Not configured'
            }
        })
    
    return app

if __name__ == '__main__':
    app = create_test_app()
    print("🚀 Starting CineAI Test Backend...")
    print("📍 URLs:")
    print("   • Home: http://localhost:5000/")
    print("   • Health: http://localhost:5000/api/health")
    print("   • Test: http://localhost:5000/api/test")
    
    app.run(host='0.0.0.0', port=5000, debug=True)