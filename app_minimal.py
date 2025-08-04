#!/usr/bin/env python3
"""
🎬 CineAI - App Mínimo para Debug
Versão reduzida do app.py para identificar problema
"""

import os
from flask import Flask, jsonify, request
from flask_cors import CORS
from src.database.config import db
from config import config

def create_minimal_app():
    app = Flask(__name__)
    
    # Configuração básica
    config_name = os.getenv('FLASK_ENV', 'development')
    app.config.from_object(config[config_name])
    
    # Inicializar banco
    db.init_app(app)
    
    # CORS simples
    CORS(app, 
         origins=['*'],
         methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'],
         allow_headers=['Content-Type', 'Authorization'],
         supports_credentials=True)
    
    # Rota de saúde manual
    @app.route('/api/health')
    def health_check():
        return jsonify({
            'status': 'healthy',
            'message': 'API funcionando!',
            'version': '1.0.0'
        })
    
    @app.route('/')
    def home():
        return jsonify({
            'message': '🎬 CineAI API is running!',
            'status': 'ok'
        })
    
    # Middleware para logging (pode ser o problema)
    @app.before_request
    def log_request_info():
        """Log das informações de request"""
        if app.debug:
            print(f"{request.method} {request.url}")
            if hasattr(request, 'json') and request.json:
                print(f"JSON Body: {request.json}")
    
    return app

if __name__ == '__main__':
    app = create_minimal_app()
    
    # Criar tabelas
    with app.app_context():
        db.create_all()
        print("✅ Database tables created/verified")
    
    print("🚀 Starting CineAI Minimal Backend...")
    print("📍 URLs:")
    print("   • Home: http://localhost:5000/")
    print("   • Health: http://localhost:5000/api/health")
    
    app.run(host='0.0.0.0', port=5000, debug=True)