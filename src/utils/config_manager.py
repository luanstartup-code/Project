import os
import json
from typing import Dict, Any, Optional
from cryptography.fernet import Fernet
import base64

class ConfigManager:
    """Gerenciador de configurações da aplicação"""
    
    def __init__(self):
        self.config_file = 'config.json'
        self.secret_key = os.getenv('SECRET_KEY', 'default-secret-key-change-in-production')
        self.cipher = Fernet(base64.urlsafe_b64encode(self.secret_key.encode()[:32].ljust(32, b'0')))
        
        # Configurações padrão
        self.default_config = {
            'ai': {
                'openai': {
                    'enabled': False,
                    'api_key': '',
                    'model': 'gpt-4',
                    'max_tokens': 4000,
                    'temperature': 0.7
                },
                'anthropic': {
                    'enabled': False,
                    'api_key': '',
                    'model': 'claude-3-sonnet',
                    'max_tokens': 4000
                }
            },
            'video': {
                'runway': {
                    'enabled': False,
                    'api_key': '',
                    'model': 'gen-3',
                    'quality': 'high'
                },
                'heygen': {
                    'enabled': False,
                    'api_key': '',
                    'avatar_quality': 'high',
                    'voice_cloning': True
                },
                'elevenlabs': {
                    'enabled': False,
                    'api_key': '',
                    'voice_id': '',
                    'stability': 0.5
                }
            },
            'storage': {
                'provider': 'local',  # local, s3, cloudinary
                'local_path': 'src/static/assets',
                'max_file_size': 100 * 1024 * 1024,  # 100MB
                'allowed_extensions': ['jpg', 'jpeg', 'png', 'mp4', 'mov', 'avi']
            },
            'app': {
                'debug': False,
                'max_concurrent_jobs': 5,
                'session_timeout': 3600,  # 1 hora
                'rate_limit': {
                    'requests_per_minute': 60,
                    'requests_per_hour': 1000
                }
            }
        }
        
        self.config = self.load_config()
    
    def load_config(self) -> Dict[str, Any]:
        """Carregar configurações do arquivo"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r') as f:
                    config = json.load(f)
                    # Mesclar com configurações padrão
                    return self.merge_configs(self.default_config, config)
            else:
                # Criar arquivo de configuração padrão
                self.save_config(self.default_config)
                return self.default_config
        except Exception as e:
            print(f"Erro ao carregar configurações: {e}")
            return self.default_config
    
    def save_config(self, config: Dict[str, Any]) -> bool:
        """Salvar configurações no arquivo"""
        try:
            with open(self.config_file, 'w') as f:
                json.dump(config, f, indent=2)
            self.config = config
            return True
        except Exception as e:
            print(f"Erro ao salvar configurações: {e}")
            return False
    
    def merge_configs(self, default: Dict[str, Any], custom: Dict[str, Any]) -> Dict[str, Any]:
        """Mesclar configurações customizadas com padrão"""
        result = default.copy()
        
        def merge_dicts(d1, d2):
            for key, value in d2.items():
                if key in d1 and isinstance(d1[key], dict) and isinstance(value, dict):
                    merge_dicts(d1[key], value)
                else:
                    d1[key] = value
        
        merge_dicts(result, custom)
        return result
    
    def get(self, key: str, default: Any = None) -> Any:
        """Obter valor de configuração"""
        keys = key.split('.')
        value = self.config
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        
        return value
    
    def set(self, key: str, value: Any) -> bool:
        """Definir valor de configuração"""
        keys = key.split('.')
        config = self.config
        
        # Navegar até o último nível
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        
        # Definir valor
        config[keys[-1]] = value
        
        return self.save_config(self.config)
    
    def get_api_key(self, service: str, provider: str) -> Optional[str]:
        """Obter API key criptografada"""
        key_path = f"{service}.{provider}.api_key"
        encrypted_key = self.get(key_path)
        
        if encrypted_key:
            try:
                return self.cipher.decrypt(encrypted_key.encode()).decode()
            except Exception:
                return None
        return None
    
    def set_api_key(self, service: str, provider: str, api_key: str) -> bool:
        """Definir API key criptografada"""
        encrypted_key = self.cipher.encrypt(api_key.encode()).decode()
        return self.set(f"{service}.{provider}.api_key", encrypted_key)
    
    def is_service_enabled(self, service: str, provider: str) -> bool:
        """Verificar se serviço está habilitado"""
        return self.get(f"{service}.{provider}.enabled", False)
    
    def enable_service(self, service: str, provider: str) -> bool:
        """Habilitar serviço"""
        return self.set(f"{service}.{provider}.enabled", True)
    
    def disable_service(self, service: str, provider: str) -> bool:
        """Desabilitar serviço"""
        return self.set(f"{service}.{provider}.enabled", False)
    
    def validate_config(self) -> Dict[str, Any]:
        """Validar configurações"""
        errors = []
        warnings = []
        
        # Verificar API keys
        services = {
            'ai': ['openai', 'anthropic'],
            'video': ['runway', 'heygen', 'elevenlabs']
        }
        
        for service, providers in services.items():
            for provider in providers:
                if self.is_service_enabled(service, provider):
                    api_key = self.get_api_key(service, provider)
                    if not api_key:
                        errors.append(f"API key não configurada para {service}.{provider}")
                    elif len(api_key) < 10:
                        warnings.append(f"API key muito curta para {service}.{provider}")
        
        # Verificar storage
        storage_provider = self.get('storage.provider')
        if storage_provider not in ['local', 's3', 'cloudinary']:
            errors.append(f"Provedor de storage inválido: {storage_provider}")
        
        # Verificar limites
        max_file_size = self.get('storage.max_file_size')
        if max_file_size > 500 * 1024 * 1024:  # 500MB
            warnings.append("Tamanho máximo de arquivo muito alto")
        
        return {
            'valid': len(errors) == 0,
            'errors': errors,
            'warnings': warnings
        }
    
    def get_all_config(self) -> Dict[str, Any]:
        """Obter todas as configurações (sem API keys)"""
        config = self.config.copy()
        
        # Remover API keys sensíveis
        services = {
            'ai': ['openai', 'anthropic'],
            'video': ['runway', 'heygen', 'elevenlabs']
        }
        
        for service, providers in services.items():
            for provider in providers:
                if f"{service}.{provider}.api_key" in config:
                    config[f"{service}.{provider}.api_key"] = "***"
        
        return config

# Instância global
config_manager = ConfigManager()