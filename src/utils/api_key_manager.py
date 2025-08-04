import os
import json
import base64
from cryptography.fernet import Fernet
from typing import Dict, Optional, Any, List
from datetime import datetime
import secrets
import re

class APIKeyManager:
    """Gerenciador seguro de API Keys"""
    
    def __init__(self):
        self.secret_key = os.getenv('JWT_SECRET_KEY', secrets.token_urlsafe(32))
        # Gerar chave de criptografia consistente baseada na secret key
        key = base64.urlsafe_b64encode(self.secret_key.encode()[:32].ljust(32, b'0'))
        self.cipher = Fernet(key)
        
        # Configurações padrão para APIs
        self.api_configs = {
            'openai': {
                'name': 'OpenAI',
                'key_pattern': r'^sk-[A-Za-z0-9]{20,}$',
                'required_fields': ['api_key'],
                'optional_fields': ['model', 'max_tokens', 'temperature'],
                'test_endpoint': 'https://api.openai.com/v1/models'
            },
            'anthropic': {
                'name': 'Anthropic',
                'key_pattern': r'^sk-ant-[A-Za-z0-9\-_]{20,}$',
                'required_fields': ['api_key'],
                'optional_fields': ['model', 'max_tokens'],
                'test_endpoint': 'https://api.anthropic.com/v1/messages'
            },
            'heygen': {
                'name': 'HeyGen',
                'key_pattern': r'^[A-Za-z0-9]{20,}$',
                'required_fields': ['api_key'],
                'optional_fields': ['avatar_quality', 'voice_cloning'],
                'test_endpoint': 'https://api.heygen.com/v1/avatars'
            },
            'runway': {
                'name': 'Runway ML',
                'key_pattern': r'^[A-Za-z0-9\-_]{20,}$',
                'required_fields': ['api_key'],
                'optional_fields': ['model', 'quality'],
                'test_endpoint': 'https://api.runwayml.com/v1/models'
            },
            'elevenlabs': {
                'name': 'ElevenLabs',
                'key_pattern': r'^[A-Za-z0-9]{20,}$',
                'required_fields': ['api_key', 'voice_id'],
                'optional_fields': ['stability'],
                'test_endpoint': 'https://api.elevenlabs.io/v1/voices'
            }
        }
    
    def encrypt_key(self, api_key: str) -> str:
        """Criptografar API key"""
        if not api_key:
            return ""
        return self.cipher.encrypt(api_key.encode()).decode()
    
    def decrypt_key(self, encrypted_key: str) -> str:
        """Descriptografar API key"""
        if not encrypted_key:
            return ""
        try:
            return self.cipher.decrypt(encrypted_key.encode()).decode()
        except Exception:
            return ""
    
    def validate_api_key(self, service: str, api_key: str) -> Dict[str, Any]:
        """Validar formato da API key"""
        if service not in self.api_configs:
            return {
                'valid': False,
                'error': f'Serviço {service} não suportado'
            }
        
        config = self.api_configs[service]
        pattern = config['key_pattern']
        
        if not re.match(pattern, api_key):
            return {
                'valid': False,
                'error': f'Formato de API key inválido para {config["name"]}'
            }
        
        return {'valid': True}
    
    def set_api_key(self, user_id: str, service: str, api_key: str, additional_config: Dict = None) -> Dict[str, Any]:
        """Definir API key para um serviço"""
        # Validar formato
        validation = self.validate_api_key(service, api_key)
        if not validation['valid']:
            return validation
        
        # Criptografar chave
        encrypted_key = self.encrypt_key(api_key)
        
        # Preparar configuração
        config_data = {
            'api_key': encrypted_key,
            'service': service,
            'user_id': user_id,
            'created_at': datetime.utcnow().isoformat(),
            'updated_at': datetime.utcnow().isoformat(),
            'status': 'active'
        }
        
        if additional_config:
            config_data.update(additional_config)
        
        # Salvar configuração (aqui você implementaria a persistência)
        success = self._save_user_config(user_id, service, config_data)
        
        return {
            'success': success,
            'message': f'API key para {service} configurada com sucesso' if success else 'Erro ao salvar configuração'
        }
    
    def get_api_key(self, user_id: str, service: str) -> Optional[str]:
        """Obter API key descriptografada"""
        config = self._load_user_config(user_id, service)
        if config and 'api_key' in config:
            return self.decrypt_key(config['api_key'])
        return None
    
    def get_service_config(self, user_id: str, service: str) -> Optional[Dict]:
        """Obter configuração completa do serviço"""
        config = self._load_user_config(user_id, service)
        if config:
            # Descriptografar a API key
            if 'api_key' in config:
                config['api_key'] = self.decrypt_key(config['api_key'])
            return config
        return None
    
    def list_configured_services(self, user_id: str) -> List[Dict]:
        """Listar serviços configurados para o usuário"""
        services = []
        for service_id, service_config in self.api_configs.items():
            user_config = self._load_user_config(user_id, service_id)
            
            service_info = {
                'id': service_id,
                'name': service_config['name'],
                'configured': bool(user_config),
                'status': user_config.get('status', 'inactive') if user_config else 'inactive',
                'last_updated': user_config.get('updated_at') if user_config else None
            }
            services.append(service_info)
        
        return services
    
    def test_api_key(self, user_id: str, service: str) -> Dict[str, Any]:
        """Testar se a API key está funcionando"""
        api_key = self.get_api_key(user_id, service)
        if not api_key:
            return {
                'success': False,
                'error': 'API key não encontrada'
            }
        
        # Aqui você implementaria testes específicos para cada API
        # Por enquanto, retorna sucesso se a chave existe
        return {
            'success': True,
            'message': f'API key para {service} está configurada'
        }
    
    def remove_api_key(self, user_id: str, service: str) -> bool:
        """Remover API key"""
        return self._delete_user_config(user_id, service)
    
    def get_masked_key(self, user_id: str, service: str) -> Optional[str]:
        """Obter API key mascarada para exibição"""
        api_key = self.get_api_key(user_id, service)
        if api_key:
            if len(api_key) > 8:
                return api_key[:4] + '*' * (len(api_key) - 8) + api_key[-4:]
            return '*' * len(api_key)
        return None
    
    def bulk_configure_keys(self, user_id: str, keys_config: Dict[str, Dict]) -> Dict[str, Any]:
        """Configurar múltiplas API keys de uma vez"""
        results = {}
        for service, config in keys_config.items():
            if 'api_key' in config:
                result = self.set_api_key(
                    user_id, 
                    service, 
                    config['api_key'], 
                    {k: v for k, v in config.items() if k != 'api_key'}
                )
                results[service] = result
            else:
                results[service] = {
                    'success': False,
                    'error': 'API key não fornecida'
                }
        
        return results
    
    def export_config(self, user_id: str, include_keys: bool = False) -> Dict:
        """Exportar configuração do usuário"""
        export_data = {
            'user_id': user_id,
            'exported_at': datetime.utcnow().isoformat(),
            'services': {}
        }
        
        for service_id in self.api_configs.keys():
            config = self._load_user_config(user_id, service_id)
            if config:
                export_config = config.copy()
                if not include_keys:
                    # Mascarar a API key
                    if 'api_key' in export_config:
                        decrypted = self.decrypt_key(export_config['api_key'])
                        export_config['api_key'] = self.get_masked_key(user_id, service_id)
                else:
                    # Descriptografar para export completo
                    if 'api_key' in export_config:
                        export_config['api_key'] = self.decrypt_key(export_config['api_key'])
                
                export_data['services'][service_id] = export_config
        
        return export_data
    
    def _save_user_config(self, user_id: str, service: str, config: Dict) -> bool:
        """Salvar configuração do usuário (implementar persistência)"""
        # TODO: Implementar salvamento em banco de dados ou arquivo
        # Por enquanto, salva em arquivo JSON
        try:
            config_file = f"user_configs/{user_id}_{service}.json"
            os.makedirs(os.path.dirname(config_file), exist_ok=True)
            
            with open(config_file, 'w') as f:
                json.dump(config, f, indent=2)
            return True
        except Exception as e:
            print(f"Erro ao salvar configuração: {e}")
            return False
    
    def _load_user_config(self, user_id: str, service: str) -> Optional[Dict]:
        """Carregar configuração do usuário"""
        try:
            config_file = f"user_configs/{user_id}_{service}.json"
            if os.path.exists(config_file):
                with open(config_file, 'r') as f:
                    return json.load(f)
        except Exception as e:
            print(f"Erro ao carregar configuração: {e}")
        return None
    
    def _delete_user_config(self, user_id: str, service: str) -> bool:
        """Deletar configuração do usuário"""
        try:
            config_file = f"user_configs/{user_id}_{service}.json"
            if os.path.exists(config_file):
                os.remove(config_file)
            return True
        except Exception:
            return False

# Instância global
api_key_manager = APIKeyManager()