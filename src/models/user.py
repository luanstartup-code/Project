from src.database.config import db
from datetime import datetime
from sqlalchemy import Boolean, DateTime, String, Integer, Text
from sqlalchemy.orm import Mapped, mapped_column

class User(db.Model):
    """Modelo de usuário"""
    
    __tablename__ = 'users'
    
    # Campos principais
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    
    # Status e permissões
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    is_admin: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    last_login: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    
    # Configurações do usuário
    profile_image: Mapped[str] = mapped_column(String(500), nullable=True)
    bio: Mapped[str] = mapped_column(Text, nullable=True)
    preferences: Mapped[str] = mapped_column(Text, nullable=True)  # JSON string
    
    # Campos de segurança
    failed_login_attempts: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    locked_until: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    password_reset_token: Mapped[str] = mapped_column(String(255), nullable=True)
    password_reset_expires: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    verification_token: Mapped[str] = mapped_column(String(255), nullable=True)
    
    def __repr__(self):
        return f'<User {self.email}>'
    
    def to_dict(self, include_sensitive=False):
        """Converter para dicionário"""
        data = {
            'id': self.id,
            'email': self.email,
            'name': self.name,
            'is_active': self.is_active,
            'is_admin': self.is_admin,
            'is_verified': self.is_verified,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'last_login': self.last_login.isoformat() if self.last_login else None,
            'profile_image': self.profile_image,
            'bio': self.bio
        }
        
        if include_sensitive:
            data.update({
                'failed_login_attempts': self.failed_login_attempts,
                'locked_until': self.locked_until.isoformat() if self.locked_until else None,
                'preferences': self.preferences
            })
        
        return data
    
    def update_last_login(self):
        """Atualizar último login"""
        self.last_login = datetime.utcnow()
        db.session.commit()
    
    def increment_failed_login(self):
        """Incrementar tentativas de login falhadas"""
        self.failed_login_attempts += 1
        
        # Bloquear conta após 5 tentativas falhadas
        if self.failed_login_attempts >= 5:
            from datetime import timedelta
            self.locked_until = datetime.utcnow() + timedelta(minutes=30)
        
        db.session.commit()
    
    def reset_failed_login(self):
        """Resetar tentativas de login falhadas"""
        self.failed_login_attempts = 0
        self.locked_until = None
        db.session.commit()
    
    def is_locked(self):
        """Verificar se conta está bloqueada"""
        if self.locked_until:
            return datetime.utcnow() < self.locked_until
        return False
    
    def set_verification_token(self, token):
        """Definir token de verificação"""
        self.verification_token = token
        db.session.commit()
    
    def verify_account(self):
        """Verificar conta"""
        self.is_verified = True
        self.verification_token = None
        db.session.commit()
    
    def set_password_reset_token(self, token, expires_in_hours=24):
        """Definir token de reset de senha"""
        from datetime import timedelta
        self.password_reset_token = token
        self.password_reset_expires = datetime.utcnow() + timedelta(hours=expires_in_hours)
        db.session.commit()
    
    def clear_password_reset(self):
        """Limpar token de reset de senha"""
        self.password_reset_token = None
        self.password_reset_expires = None
        db.session.commit()
    
    def is_password_reset_valid(self):
        """Verificar se token de reset é válido"""
        if self.password_reset_expires:
            return datetime.utcnow() < self.password_reset_expires
        return False