import os

class Config:
    """Configuração base"""
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///video_generator.db')
    
    # Configurações de vídeo
    MAX_VIDEO_DURATION = 300  # 5 minutos
    SUPPORTED_VIDEO_FORMATS = ['txt', 'mp4', 'avi', 'mov', 'mkv']
    VIDEO_OUTPUT_DIR = 'src/static/assets/videos'
    
    # Configurações de serviços de IA
    HEYGEN_API_KEY = os.getenv('HEYGEN_API_KEY', '')
    RUNWAY_API_KEY = os.getenv('RUNWAY_API_KEY', '')
    ELEVENLABS_API_KEY = os.getenv('ELEVENLABS_API_KEY', '')
    ELEVENLABS_VOICE_ID = os.getenv('ELEVENLABS_VOICE_ID', '')
    
    # Configurações de upload
    MAX_CONTENT_LENGTH = 100 * 1024 * 1024  # 100MB
    
    # Configurações de polling
    POLLING_INTERVAL = 2  # segundos
    MAX_POLLING_ATTEMPTS = 60

class DevelopmentConfig(Config):
    """Configuração para desenvolvimento"""
    DEBUG = True
    FLASK_ENV = 'development'

class ProductionConfig(Config):
    """Configuração para produção"""
    DEBUG = False
    FLASK_ENV = 'production'
    
    # Configurações de segurança para produção
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///video_generator.db')
    SECRET_KEY = os.getenv('SECRET_KEY', 'prod-secret-key-change-in-production')

class TestingConfig(Config):
    """Configuração para testes"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False

# Dicionário de configurações
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}