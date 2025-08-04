import os
import jwt
import bcrypt
import secrets
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from functools import wraps
from flask import request, jsonify, current_app, session

class AuthManager:
    """Gerenciador de autenticação e autorização"""
    
    def __init__(self):
        self.jwt_secret = os.getenv('JWT_SECRET_KEY', secrets.token_urlsafe(32))
        self.session_timeout = int(os.getenv('SESSION_TIMEOUT', 3600))  # 1 hora
        
    def hash_password(self, password: str) -> str:
        """Hash da senha usando bcrypt"""
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')
    
    def verify_password(self, password: str, hashed: str) -> bool:
        """Verificar senha"""
        return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))
    
    def generate_token(self, user_id: str, additional_claims: Dict = None) -> str:
        """Gerar JWT token"""
        payload = {
            'user_id': user_id,
            'iat': datetime.utcnow(),
            'exp': datetime.utcnow() + timedelta(seconds=self.session_timeout)
        }
        
        if additional_claims:
            payload.update(additional_claims)
            
        return jwt.encode(payload, self.jwt_secret, algorithm='HS256')
    
    def verify_token(self, token: str) -> Optional[Dict]:
        """Verificar e decodificar JWT token"""
        try:
            payload = jwt.decode(token, self.jwt_secret, algorithms=['HS256'])
            return payload
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None
    
    def login_required(self, f):
        """Decorator para rotas que requerem autenticação"""
        @wraps(f)
        def decorated_function(*args, **kwargs):
            token = None
            
            # Verificar token no header Authorization
            if 'Authorization' in request.headers:
                auth_header = request.headers['Authorization']
                try:
                    token = auth_header.split(" ")[1]  # Bearer TOKEN
                except IndexError:
                    return jsonify({'error': 'Token format invalid'}), 401
            
            # Verificar token na sessão
            elif 'token' in session:
                token = session['token']
            
            if not token:
                return jsonify({'error': 'Token is missing'}), 401
            
            payload = self.verify_token(token)
            if not payload:
                return jsonify({'error': 'Token is invalid or expired'}), 401
            
            # Adicionar user_id ao request context
            request.current_user = payload['user_id']
            return f(*args, **kwargs)
        
        return decorated_function
    
    def admin_required(self, f):
        """Decorator para rotas que requerem privilégios de admin"""
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # Primeiro verifica autenticação
            auth_result = self.login_required(f)(*args, **kwargs)
            
            # Verificar se usuário é admin (implementar lógica específica)
            if not self.is_admin(request.current_user):
                return jsonify({'error': 'Admin privileges required'}), 403
            
            return auth_result
        
        return decorated_function
    
    def is_admin(self, user_id: str) -> bool:
        """Verificar se usuário tem privilégios de admin"""
        # TODO: Implementar lógica de verificação de admin
        # Por enquanto, apenas usuários específicos
        admin_users = os.getenv('ADMIN_USERS', '').split(',')
        return user_id in admin_users
    
    def rate_limit_check(self, user_id: str, action: str) -> bool:
        """Verificar rate limiting para usuário"""
        # TODO: Implementar redis ou cache para rate limiting
        return True
    
    def create_session(self, user_id: str, user_data: Dict = None) -> str:
        """Criar sessão de usuário"""
        session_data = {
            'user_id': user_id,
            'created_at': datetime.utcnow().isoformat(),
            'last_activity': datetime.utcnow().isoformat()
        }
        
        if user_data:
            session_data.update(user_data)
        
        token = self.generate_token(user_id, session_data)
        
        # Salvar na sessão Flask
        session['token'] = token
        session['user_id'] = user_id
        session.permanent = True
        
        return token
    
    def destroy_session(self) -> bool:
        """Destruir sessão atual"""
        session.clear()
        return True
    
    def refresh_token(self, token: str) -> Optional[str]:
        """Renovar token se ainda válido"""
        payload = self.verify_token(token)
        if payload:
            user_id = payload['user_id']
            return self.generate_token(user_id)
        return None
    
    def get_user_permissions(self, user_id: str) -> list:
        """Obter permissões do usuário"""
        # TODO: Implementar sistema de permissões
        base_permissions = ['read', 'write']
        
        if self.is_admin(user_id):
            base_permissions.extend(['admin', 'delete', 'manage_users', 'manage_api_keys'])
        
        return base_permissions
    
    def check_permission(self, user_id: str, permission: str) -> bool:
        """Verificar se usuário tem permissão específica"""
        user_permissions = self.get_user_permissions(user_id)
        return permission in user_permissions

# Instância global
auth_manager = AuthManager()

# Decorators para uso direto
login_required = auth_manager.login_required
admin_required = auth_manager.admin_required