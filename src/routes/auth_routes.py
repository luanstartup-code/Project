from flask import Blueprint, request, jsonify, session
from src.utils.auth_manager import auth_manager, login_required, admin_required
from src.utils.api_key_manager import api_key_manager
from src.database.config import db
from src.models.user import User
import re

auth_bp = Blueprint('auth', __name__)

def validate_email(email):
    """Validar formato de email"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_password(password):
    """Validar força da senha"""
    if len(password) < 8:
        return False, "Senha deve ter pelo menos 8 caracteres"
    if not re.search(r'[A-Z]', password):
        return False, "Senha deve conter pelo menos uma letra maiúscula"
    if not re.search(r'[a-z]', password):
        return False, "Senha deve conter pelo menos uma letra minúscula"
    if not re.search(r'\d', password):
        return False, "Senha deve conter pelo menos um número"
    return True, "Senha válida"

@auth_bp.route('/register', methods=['POST'])
def register():
    """Registrar novo usuário"""
    try:
        data = request.get_json()
        
        # Validar dados obrigatórios
        required_fields = ['email', 'password', 'name']
        for field in required_fields:
            if field not in data or not data[field]:
                return jsonify({
                    'error': f'Campo {field} é obrigatório'
                }), 400
        
        email = data['email'].lower().strip()
        password = data['password']
        name = data['name'].strip()
        
        # Validar email
        if not validate_email(email):
            return jsonify({
                'error': 'Formato de email inválido'
            }), 400
        
        # Validar senha
        password_valid, password_message = validate_password(password)
        if not password_valid:
            return jsonify({
                'error': password_message
            }), 400
        
        # Verificar se usuário já existe
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            return jsonify({
                'error': 'Usuário já existe com este email'
            }), 409
        
        # Criar novo usuário
        hashed_password = auth_manager.hash_password(password)
        user = User(
            email=email,
            password_hash=hashed_password,
            name=name,
            is_active=True
        )
        
        db.session.add(user)
        db.session.commit()
        
        # Criar sessão
        token = auth_manager.create_session(
            user_id=str(user.id),
            user_data={
                'email': user.email,
                'name': user.name,
                'is_admin': user.is_admin
            }
        )
        
        return jsonify({
            'message': 'Usuário registrado com sucesso',
            'user': {
                'id': user.id,
                'email': user.email,
                'name': user.name
            },
            'token': token
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'error': 'Erro interno do servidor',
            'details': str(e)
        }), 500

@auth_bp.route('/login', methods=['POST'])
def login():
    """Autenticar usuário"""
    try:
        data = request.get_json()
        
        if not data or 'email' not in data or 'password' not in data:
            return jsonify({
                'error': 'Email e senha são obrigatórios'
            }), 400
        
        email = data['email'].lower().strip()
        password = data['password']
        
        # Buscar usuário
        user = User.query.filter_by(email=email).first()
        if not user or not auth_manager.verify_password(password, user.password_hash):
            return jsonify({
                'error': 'Credenciais inválidas'
            }), 401
        
        if not user.is_active:
            return jsonify({
                'error': 'Conta desativada'
            }), 403
        
        # Criar sessão
        token = auth_manager.create_session(
            user_id=str(user.id),
            user_data={
                'email': user.email,
                'name': user.name,
                'is_admin': user.is_admin
            }
        )
        
        # Obter serviços configurados
        configured_services = api_key_manager.list_configured_services(str(user.id))
        
        return jsonify({
            'message': 'Login realizado com sucesso',
            'user': {
                'id': user.id,
                'email': user.email,
                'name': user.name,
                'is_admin': user.is_admin
            },
            'token': token,
            'configured_services': configured_services
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': 'Erro interno do servidor',
            'details': str(e)
        }), 500

@auth_bp.route('/logout', methods=['POST'])
@login_required
def logout():
    """Deslogar usuário"""
    auth_manager.destroy_session()
    return jsonify({
        'message': 'Logout realizado com sucesso'
    }), 200

@auth_bp.route('/profile', methods=['GET'])
@login_required
def get_profile():
    """Obter perfil do usuário"""
    try:
        user_id = request.current_user
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({
                'error': 'Usuário não encontrado'
            }), 404
        
        # Obter serviços configurados
        configured_services = api_key_manager.list_configured_services(user_id)
        
        return jsonify({
            'user': {
                'id': user.id,
                'email': user.email,
                'name': user.name,
                'is_admin': user.is_admin,
                'created_at': user.created_at.isoformat(),
                'last_login': user.last_login.isoformat() if user.last_login else None
            },
            'configured_services': configured_services,
            'permissions': auth_manager.get_user_permissions(user_id)
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': 'Erro ao obter perfil',
            'details': str(e)
        }), 500

@auth_bp.route('/api-keys', methods=['GET'])
@login_required
def list_api_keys():
    """Listar API keys configuradas"""
    try:
        user_id = request.current_user
        services = api_key_manager.list_configured_services(user_id)
        
        # Adicionar informações mascaradas das chaves
        for service in services:
            if service['configured']:
                service['masked_key'] = api_key_manager.get_masked_key(user_id, service['id'])
        
        return jsonify({
            'services': services
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': 'Erro ao listar API keys',
            'details': str(e)
        }), 500

@auth_bp.route('/api-keys/<service>', methods=['POST'])
@login_required
def configure_api_key(service):
    """Configurar API key para um serviço"""
    try:
        user_id = request.current_user
        data = request.get_json()
        
        if not data or 'api_key' not in data:
            return jsonify({
                'error': 'API key é obrigatória'
            }), 400
        
        api_key = data['api_key'].strip()
        additional_config = {k: v for k, v in data.items() if k != 'api_key'}
        
        result = api_key_manager.set_api_key(user_id, service, api_key, additional_config)
        
        if result.get('success'):
            return jsonify({
                'message': result['message'],
                'service': service,
                'masked_key': api_key_manager.get_masked_key(user_id, service)
            }), 200
        else:
            return jsonify({
                'error': result.get('error', 'Erro ao configurar API key')
            }), 400
            
    except Exception as e:
        return jsonify({
            'error': 'Erro interno do servidor',
            'details': str(e)
        }), 500

@auth_bp.route('/api-keys/<service>/test', methods=['POST'])
@login_required
def test_api_key(service):
    """Testar API key"""
    try:
        user_id = request.current_user
        result = api_key_manager.test_api_key(user_id, service)
        
        if result['success']:
            return jsonify(result), 200
        else:
            return jsonify(result), 400
            
    except Exception as e:
        return jsonify({
            'error': 'Erro ao testar API key',
            'details': str(e)
        }), 500

@auth_bp.route('/api-keys/<service>', methods=['DELETE'])
@login_required
def remove_api_key(service):
    """Remover API key"""
    try:
        user_id = request.current_user
        success = api_key_manager.remove_api_key(user_id, service)
        
        if success:
            return jsonify({
                'message': f'API key para {service} removida com sucesso'
            }), 200
        else:
            return jsonify({
                'error': 'Erro ao remover API key'
            }), 400
            
    except Exception as e:
        return jsonify({
            'error': 'Erro interno do servidor',
            'details': str(e)
        }), 500

@auth_bp.route('/api-keys/bulk', methods=['POST'])
@login_required
def bulk_configure_api_keys():
    """Configurar múltiplas API keys"""
    try:
        user_id = request.current_user
        data = request.get_json()
        
        if not data or 'keys' not in data:
            return jsonify({
                'error': 'Configuração de chaves é obrigatória'
            }), 400
        
        results = api_key_manager.bulk_configure_keys(user_id, data['keys'])
        
        return jsonify({
            'message': 'Configuração em lote processada',
            'results': results
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': 'Erro ao configurar chaves em lote',
            'details': str(e)
        }), 500

@auth_bp.route('/api-keys/export', methods=['GET'])
@login_required
def export_api_config():
    """Exportar configuração de API keys"""
    try:
        user_id = request.current_user
        include_keys = request.args.get('include_keys', 'false').lower() == 'true'
        
        # Verificar permissão para exportar com chaves
        if include_keys and not auth_manager.check_permission(user_id, 'admin'):
            return jsonify({
                'error': 'Permissão negada para exportar chaves completas'
            }), 403
        
        export_data = api_key_manager.export_config(user_id, include_keys)
        
        return jsonify(export_data), 200
        
    except Exception as e:
        return jsonify({
            'error': 'Erro ao exportar configuração',
            'details': str(e)
        }), 500

@auth_bp.route('/refresh-token', methods=['POST'])
@login_required
def refresh_token():
    """Renovar token de acesso"""
    try:
        # Token atual já foi validado pelo decorator
        user_id = request.current_user
        user = User.query.get(user_id)
        
        if not user or not user.is_active:
            return jsonify({
                'error': 'Usuário inválido ou inativo'
            }), 401
        
        # Gerar novo token
        new_token = auth_manager.create_session(
            user_id=user_id,
            user_data={
                'email': user.email,
                'name': user.name,
                'is_admin': user.is_admin
            }
        )
        
        return jsonify({
            'message': 'Token renovado com sucesso',
            'token': new_token
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': 'Erro ao renovar token',
            'details': str(e)
        }), 500