from src.database.config import db
from datetime import datetime

class Session(db.Model):
    """Modelo de sessão do chat"""
    __tablename__ = 'sessions'
    
    id = db.Column(db.String(100), primary_key=True)
    title = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    message_count = db.Column(db.Integer, default=0)
    
    def to_dict(self):
        """Converter para dicionário"""
        return {
            'id': self.id,
            'title': self.title,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'message_count': self.message_count
        }
    
    def __repr__(self):
        return f'<Session {self.id}: {self.title}>'