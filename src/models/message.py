from src.database.config import db
from datetime import datetime

class Message(db.Model):
    """Modelo de mensagem do chat"""
    __tablename__ = 'messages'
    
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    role = db.Column(db.String(20), nullable=False)  # 'user' ou 'assistant'
    session_id = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        """Converter para dicionário"""
        return {
            'id': self.id,
            'content': self.content,
            'role': self.role,
            'session_id': self.session_id,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
    
    def __repr__(self):
        return f'<Message {self.id}: {self.role}>'