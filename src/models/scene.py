from src.database.config import db
from datetime import datetime

class Scene(db.Model):
    """Modelo de cena de vídeo"""
    __tablename__ = 'scenes'
    
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), nullable=False)
    
    # Informações básicas
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    order = db.Column(db.Integer, default=0)  # Ordem na timeline
    
    # Configurações de vídeo
    duration = db.Column(db.Float, default=5.0)  # Duração em segundos
    background = db.Column(db.String(500))  # URL ou path do background
    transition = db.Column(db.String(50), default='fade')  # fade, slide, cut
    
    # Avatar e voz
    avatar_id = db.Column(db.Integer, db.ForeignKey('avatars.id'))
    voice_id = db.Column(db.String(100))  # ID da voz no ElevenLabs
    voice_settings = db.Column(db.Text)  # JSON com configurações de voz
    
    # Texto e script
    script = db.Column(db.Text)  # Texto a ser falado
    subtitle = db.Column(db.Text)  # Legenda opcional
    
    # Configurações de IA
    ai_prompt = db.Column(db.Text)  # Prompt para geração
    ai_model = db.Column(db.String(50), default='gen-3')  # Modelo de IA
    
    # Status
    status = db.Column(db.String(20), default='pending')  # pending, processing, completed, failed
    file_path = db.Column(db.String(500))  # Path do vídeo gerado
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        """Converter para dicionário"""
        return {
            'id': self.id,
            'project_id': self.project_id,
            'title': self.title,
            'description': self.description,
            'order': self.order,
            'duration': self.duration,
            'background': self.background,
            'transition': self.transition,
            'avatar_id': self.avatar_id,
            'voice_id': self.voice_id,
            'voice_settings': self.voice_settings,
            'script': self.script,
            'subtitle': self.subtitle,
            'ai_prompt': self.ai_prompt,
            'ai_model': self.ai_model,
            'status': self.status,
            'file_path': self.file_path,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def __repr__(self):
        return f'<Scene {self.id}: {self.title}>'

class Project(db.Model):
    """Modelo de projeto de vídeo"""
    __tablename__ = 'projects'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    
    # Configurações do projeto
    template = db.Column(db.String(100))  # Template usado
    resolution = db.Column(db.String(20), default='1920x1080')  # Resolução do vídeo
    fps = db.Column(db.Integer, default=30)  # Frames por segundo
    format = db.Column(db.String(10), default='mp4')  # Formato de saída
    
    # Cenas do projeto
    scenes = db.relationship('Scene', backref='project', lazy=True, order_by='Scene.order', cascade='all, delete-orphan')
    
    # Status
    status = db.Column(db.String(20), default='draft')  # draft, processing, completed, failed
    final_video_path = db.Column(db.String(500))  # Path do vídeo final
    
    # Métricas
    total_duration = db.Column(db.Float, default=0.0)
    scene_count = db.Column(db.Integer, default=0)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        """Converter para dicionário"""
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'template': self.template,
            'resolution': self.resolution,
            'fps': self.fps,
            'format': self.format,
            'scenes': [scene.to_dict() for scene in self.scenes],
            'status': self.status,
            'final_video_path': self.final_video_path,
            'total_duration': self.total_duration,
            'scene_count': self.scene_count,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def __repr__(self):
        return f'<Project {self.id}: {self.title}>'