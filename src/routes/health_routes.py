from flask import Blueprint, jsonify
from src.database.config import db

health_bp = Blueprint('health', __name__)

@health_bp.route('/')
def health_check():
    """Health check básico"""
    return jsonify({
        'status': 'healthy',
        'message': 'AI Video Generator API is running',
        'version': '1.0.0'
    })

@health_bp.route('/ready')
def ready_check():
    """Verificar se a aplicação está pronta"""
    try:
        # Verificar conexão com banco de dados
        db.session.execute('SELECT 1')
        return jsonify({
            'status': 'ready',
            'message': 'Application is ready to serve requests',
            'database': 'connected'
        })
    except Exception as e:
        return jsonify({
            'status': 'not_ready',
            'message': 'Application is not ready',
            'error': str(e)
        }), 503