from flask import Flask, request, jsonify
from flask_cors import CORS
from src.database.config import db
from src.routes.video_routes import video_bp
from src.routes.health_routes import health_bp
from src.routes.chat_routes import chat_bp
from src.routes.settings_routes import settings_bp
from src.routes.avatar_routes import avatar_bp
from src.routes.project_routes import project_bp
from src.routes.auth_routes import auth_bp
from src.routes.prompt_routes import prompt_bp
from src.utils.auth_manager import auth_manager
from config import config
import os

def create_app(config_name=None):
    app = Flask(__name__)
    
    # Configuração baseada no ambiente
    if config_name is None:
        config_name = os.getenv('FLASK_ENV', 'development')
    
    app.config.from_object(config[config_name])
    
    # Configuração adicional para autenticação
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key')
    app.config['SESSION_COOKIE_SECURE'] = config_name == 'production'
    app.config['SESSION_COOKIE_HTTPONLY'] = True
    app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
    app.permanent_session_lifetime = auth_manager.session_timeout
    
    # Configuração do CORS para produção
    cors_origins = os.getenv('CORS_ORIGINS', 'http://localhost:3000').split(',')
    all_origins = cors_origins + [
        'http://localhost:3000',   # Desenvolvimento local
        'https://cineai.vercel.app',  # Produção
        'https://*.vercel.app',    # Preview builds
    ]
    CORS(app, 
         origins=all_origins,
         supports_credentials=True,
         allow_headers=['Content-Type', 'Authorization'],
         methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'])
    
    # Inicializar banco de dados
    db.init_app(app)
    
    # Registrar blueprints
    app.register_blueprint(health_bp, url_prefix='/api/health')
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(prompt_bp, url_prefix='/api/prompt')
    app.register_blueprint(video_bp, url_prefix='/api/videos')
    app.register_blueprint(chat_bp, url_prefix='/api/chat')
    app.register_blueprint(settings_bp, url_prefix='/api/settings')
    app.register_blueprint(avatar_bp, url_prefix='/api/avatars')
    app.register_blueprint(project_bp, url_prefix='/api/projects')
    
    # Middleware para logging de requests
    @app.before_request
    def log_request_info():
        """Log das informações de request"""
        if app.debug:
            print(f"{request.method} {request.url}")
            if request.json:
                # Não logar dados sensíveis
                safe_data = {k: v for k, v in request.json.items() 
                           if k not in ['password', 'api_key', 'token']}
                if safe_data:
                    print(f"Body: {safe_data}")
    
    # Middleware para headers de segurança
    @app.after_request
    def after_request(response):
        """Adicionar headers de segurança"""
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['X-Frame-Options'] = 'DENY'
        response.headers['X-XSS-Protection'] = '1; mode=block'
        
        if config_name == 'production':
            response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
        
        return response
    
    # Handler para erros 404
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'error': 'Endpoint não encontrado',
            'status': 404
        }), 404
    
    # Handler para erros 500
    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return jsonify({
            'error': 'Erro interno do servidor',
            'status': 500
        }), 500
    
    # Handler para erros de autenticação
    @app.errorhandler(401)
    def unauthorized(error):
        return jsonify({
            'error': 'Não autorizado',
            'status': 401,
            'message': 'Token de acesso necessário'
        }), 401
    
    # Handler para erros de permissão
    @app.errorhandler(403)
    def forbidden(error):
        return jsonify({
            'error': 'Acesso negado',
            'status': 403,
            'message': 'Permissões insuficientes'
        }), 403
    
    # Rota raiz com informações do sistema
    @app.route('/')
    def home():
        return jsonify({
            'message': 'AI Video Generator Studio API',
            'version': '2.0.0',
            'status': 'running',
            'environment': config_name,
            'features': [
                'Authentication System',
                'API Key Management',
                'Video Generation',
                'Avatar Creation',
                'Chat AI with Fallback',
                'Prompt Enhancement',
                'Project Management',
                'Settings Management'
            ],
            'endpoints': {
                'auth': '/api/auth',
                'prompt': '/api/prompt',
                'videos': '/api/videos',
                'avatars': '/api/avatars',
                'chat': '/api/chat',
                'projects': '/api/projects',
                'settings': '/api/settings',
                'health': '/api/health'
            }
        })
    
    # Rota para informações do sistema (protegida)
    @app.route('/api/system/info')
    @auth_manager.admin_required
    def system_info():
        """Informações detalhadas do sistema (apenas admins)"""
        return jsonify({
            'system': {
                'environment': config_name,
                'debug_mode': app.debug,
                'database_url': app.config.get('SQLALCHEMY_DATABASE_URI', '').split('@')[-1] if '@' in app.config.get('SQLALCHEMY_DATABASE_URI', '') else 'local',
                'session_timeout': auth_manager.session_timeout,
                'cors_origins': app.config.get('CORS_ORIGINS', [])
            },
            'services': {
                'openai': bool(os.getenv('OPENAI_API_KEY')),
                'gemini': bool(os.getenv('GEMINI_API_KEY')),
                'heygen': bool(os.getenv('HEYGEN_API_KEY')),
                'runway': bool(os.getenv('RUNWAY_API_KEY')),
                'elevenlabs': bool(os.getenv('ELEVENLABS_API_KEY'))
            }
        })
    
        return app

if __name__ == '__main__':
    app = create_app()
    
    # Criar tabelas do banco de dados
    with app.app_context():
        # Importar todos os modelos
        from src.models.user import User
        from src.models.avatar import Avatar
        from src.models.scene import Scene
        from src.models.project import Project
        from src.models.video import Video
        
        db.create_all()
        
        # Criar usuário admin padrão se não existir
        admin_email = os.getenv('ADMIN_EMAIL', 'admin@aistudio.com')
        admin_password = os.getenv('ADMIN_PASSWORD', 'admin123')
        
        admin_user = User.query.filter_by(email=admin_email).first()
        if not admin_user:
            admin_user = User(
                email=admin_email,
                password_hash=auth_manager.hash_password(admin_password),
                name='Administrator',
                is_admin=True,
                is_active=True,
                is_verified=True
            )
            db.session.add(admin_user)
            db.session.commit()
            print(f"✅ Usuário admin criado: {admin_email}")
        
        print(f"🚀 Servidor iniciado no ambiente: {os.getenv('FLASK_ENV', 'development')}")
        print(f"📊 Banco de dados: {app.config['SQLALCHEMY_DATABASE_URI']}")
        print(f"🔐 Sistema de autenticação: Ativo")
        print(f"🔑 Gerenciador de API Keys: Ativo")
        print(f"🤖 OpenAI: {'✅ Configurado' if os.getenv('OPENAI_API_KEY') else '❌ Não configurado'}")
        print(f"🤖 Gemini: {'✅ Configurado' if os.getenv('GEMINI_API_KEY') else '❌ Não configurado'}")
        print(f"🎬 HeyGen: {'✅ Configurado' if os.getenv('HEYGEN_API_KEY') else '❌ Não configurado'}")
        print(f"🎥 Runway: {'✅ Configurado' if os.getenv('RUNWAY_API_KEY') else '❌ Não configurado'}")
        print(f"🎤 ElevenLabs: {'✅ Configurado' if os.getenv('ELEVENLABS_API_KEY') else '❌ Não configurado'}")
    
        # Para desenvolvimento local  
        if os.getenv('FLASK_ENV') == 'development':
            port = int(os.getenv('PORT', 5000))
            app.run(host='0.0.0.0', port=port, debug=True)
        

# Criar aplicação para produção (WSGI)
app = create_app()

# Ponto de entrada para desenvolvimento
if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    debug_mode = os.getenv('FLASK_ENV') == 'development'
    app.run(host='0.0.0.0', port=port, debug=debug_mode)