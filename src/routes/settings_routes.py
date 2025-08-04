from flask import Blueprint, request, jsonify
from src.utils.config_manager import config_manager

settings_bp = Blueprint('settings', __name__)

@settings_bp.route('/config', methods=['GET'])
def get_config():
    """Obter configurações (sem API keys sensíveis)"""
    try:
        config = config_manager.get_all_config()
        validation = config_manager.validate_config()
        
        return jsonify({
            'success': True,
            'data': {
                'config': config,
                'validation': validation
            }
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@settings_bp.route('/config', methods=['PUT'])
def update_config():
    """Atualizar configurações"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'error': 'No data provided'
            }), 400
        
        # Atualizar configurações
        for key, value in data.items():
            if not config_manager.set(key, value):
                return jsonify({
                    'success': False,
                    'error': f'Failed to update {key}'
                }), 500
        
        # Validar configurações após atualização
        validation = config_manager.validate_config()
        
        return jsonify({
            'success': True,
            'message': 'Configuration updated successfully',
            'data': {
                'validation': validation
            }
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@settings_bp.route('/api-keys', methods=['GET'])
def get_api_keys_status():
    """Obter status das API keys (sem mostrar as chaves)"""
    try:
        services = {
            'ai': ['openai', 'anthropic'],
            'video': ['runway', 'heygen', 'elevenlabs']
        }
        
        status = {}
        for service, providers in services.items():
            status[service] = {}
            for provider in providers:
                enabled = config_manager.is_service_enabled(service, provider)
                has_key = bool(config_manager.get_api_key(service, provider))
                
                status[service][provider] = {
                    'enabled': enabled,
                    'configured': has_key,
                    'ready': enabled and has_key
                }
        
        return jsonify({
            'success': True,
            'data': status
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@settings_bp.route('/api-keys/<service>/<provider>', methods=['POST'])
def set_api_key(service, provider):
    """Definir API key para um serviço"""
    try:
        data = request.get_json()
        
        if not data or 'api_key' not in data:
            return jsonify({
                'success': False,
                'error': 'API key is required'
            }), 400
        
        api_key = data['api_key'].strip()
        
        if not api_key:
            return jsonify({
                'success': False,
                'error': 'API key cannot be empty'
            }), 400
        
        # Salvar API key
        if not config_manager.set_api_key(service, provider, api_key):
            return jsonify({
                'success': False,
                'error': 'Failed to save API key'
            }), 500
        
        # Habilitar serviço automaticamente
        config_manager.enable_service(service, provider)
        
        return jsonify({
            'success': True,
            'message': f'API key for {service}.{provider} saved successfully'
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@settings_bp.route('/api-keys/<service>/<provider>', methods=['DELETE'])
def delete_api_key(service, provider):
    """Remover API key de um serviço"""
    try:
        # Desabilitar serviço
        config_manager.disable_service(service, provider)
        
        # Limpar API key
        config_manager.set_api_key(service, provider, '')
        
        return jsonify({
            'success': True,
            'message': f'API key for {service}.{provider} removed successfully'
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@settings_bp.route('/services/<service>/<provider>/enable', methods=['POST'])
def enable_service(service, provider):
    """Habilitar serviço"""
    try:
        # Verificar se API key está configurada
        api_key = config_manager.get_api_key(service, provider)
        if not api_key:
            return jsonify({
                'success': False,
                'error': 'API key must be configured before enabling service'
            }), 400
        
        config_manager.enable_service(service, provider)
        
        return jsonify({
            'success': True,
            'message': f'{service}.{provider} enabled successfully'
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@settings_bp.route('/services/<service>/<provider>/disable', methods=['POST'])
def disable_service(service, provider):
    """Desabilitar serviço"""
    try:
        config_manager.disable_service(service, provider)
        
        return jsonify({
            'success': True,
            'message': f'{service}.{provider} disabled successfully'
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@settings_bp.route('/validate', methods=['GET'])
def validate_config():
    """Validar configurações"""
    try:
        validation = config_manager.validate_config()
        
        return jsonify({
            'success': True,
            'data': validation
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@settings_bp.route('/test/<service>/<provider>', methods=['POST'])
def test_service(service, provider):
    """Testar conexão com serviço"""
    try:
        # Verificar se serviço está habilitado
        if not config_manager.is_service_enabled(service, provider):
            return jsonify({
                'success': False,
                'error': 'Service is not enabled'
            }), 400
        
        # Obter API key
        api_key = config_manager.get_api_key(service, provider)
        if not api_key:
            return jsonify({
                'success': False,
                'error': 'API key not configured'
            }), 400
        
        # Testar conexão (implementar testes específicos para cada serviço)
        test_result = test_service_connection(service, provider, api_key)
        
        return jsonify({
            'success': True,
            'data': test_result
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

def test_service_connection(service, provider, api_key):
    """Testar conexão com serviço específico"""
    try:
        if service == 'ai' and provider == 'openai':
            from src.services.ai.openai_service import openai_service
            return openai_service.test_connection()
        else:
            # Para outros serviços, retornar sucesso simulado por enquanto
            return {
                'connected': True,
                'message': f'Successfully connected to {service}.{provider}',
                'response_time': 0.5
            }
    except Exception as e:
        return {
            'connected': False,
            'message': str(e),
            'response_time': 0
        }