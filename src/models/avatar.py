from src.database.config import db
from datetime import datetime

class Avatar(db.Model):
    """Modelo de avatar personalizado"""
    __tablename__ = 'avatars'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    
    # Configurações do avatar
    heygen_id = db.Column(db.String(100))  # ID do avatar no HeyGen
    voice_id = db.Column(db.String(100))   # ID da voz no ElevenLabs
    
    # Fotos do usuário
    photos = db.relationship('AvatarPhoto', backref='avatar', lazy=True, cascade='all, delete-orphan')
    
    # Configurações
    quality = db.Column(db.String(20), default='high')  # low, medium, high
    voice_cloning = db.Column(db.Boolean, default=True)
    
    # Status
    status = db.Column(db.String(20), default='pending')  # pending, processing, completed, failed
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        """Converter para dicionário"""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'heygen_id': self.heygen_id,
            'voice_id': self.voice_id,
            'photos': [photo.to_dict() for photo in self.photos],
            'quality': self.quality,
            'voice_cloning': self.voice_cloning,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def __repr__(self):
        return f'<Avatar {self.id}: {self.name}>'

class AvatarPhoto(db.Model):
    """Modelo para fotos do avatar"""
    __tablename__ = 'avatar_photos'
    
    id = db.Column(db.Integer, primary_key=True)
    avatar_id = db.Column(db.Integer, db.ForeignKey('avatars.id'), nullable=False)
    
    # Informações do arquivo
    filename = db.Column(db.String(255), nullable=False)
    file_path = db.Column(db.String(500), nullable=False)
    file_size = db.Column(db.Integer)
    mime_type = db.Column(db.String(100))
    
    # Validação
    is_valid = db.Column(db.Boolean, default=False)
    validation_message = db.Column(db.Text)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        """Converter para dicionário"""
        return {
            'id': self.id,
            'avatar_id': self.avatar_id,
            'filename': self.filename,
            'file_path': self.file_path,
            'file_size': self.file_size,
            'mime_type': self.mime_type,
            'is_valid': self.is_valid,
            'validation_message': self.validation_message,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
    
    def __repr__(self):
        return f'<AvatarPhoto {self.id}: {self.filename}>'