import requests
import json
import time
from typing import Dict, Any, Optional
from src.utils.config_manager import config_manager

class RunwayService:
    """Serviço para integração com Runway ML"""
    
    def __init__(self):
        self.api_key = config_manager.get_api_key('video', 'runway')
        self.base_url = "https://api.runwayml.com/v1"
        self.model = config_manager.get('video.runway.model', 'gen-3')
        self.quality = config_manager.get('video.runway.quality', 'high')
    
    def is_configured(self) -> bool:
        """Verificar se o serviço está configurado"""
        return bool(self.api_key)
    
    def is_enabled(self) -> bool:
        """Verificar se o serviço está habilitado"""
        return config_manager.is_service_enabled('video', 'runway')
    
    def generate_video(self, prompt: str, duration: int = 5, resolution: str = "1920x1080") -> Dict[str, Any]:
        """Gerar vídeo com Runway ML"""
        if not self.is_configured() or not self.is_enabled():
            return {
                'success': False,
                'error': 'Runway ML não está configurado ou habilitado'
            }
        
        try:
            headers = {
                'Authorization': f'Bearer {self.api_key}',
                'Content-Type': 'application/json'
            }
            
            payload = {
                'prompt': prompt,
                'model': self.model,
                'duration': duration,
                'resolution': resolution,
                'quality': self.quality
            }
            
            response = requests.post(
                f"{self.base_url}/video/generations",
                headers=headers,
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                return {
                    'success': True,
                    'generation_id': data.get('id'),
                    'status': 'processing',
                    'estimated_time': data.get('estimated_time', 60)
                }
            else:
                return {
                    'success': False,
                    'error': f'Erro da API: {response.status_code}',
                    'details': response.text
                }
                
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def get_generation_status(self, generation_id: str) -> Dict[str, Any]:
        """Obter status da geração"""
        if not self.is_configured():
            return {
                'success': False,
                'error': 'Runway ML não está configurado'
            }
        
        try:
            headers = {
                'Authorization': f'Bearer {self.api_key}',
                'Content-Type': 'application/json'
            }
            
            response = requests.get(
                f"{self.base_url}/video/generations/{generation_id}",
                headers=headers,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                return {
                    'success': True,
                    'status': data.get('status'),
                    'video_url': data.get('video_url'),
                    'progress': data.get('progress', 0),
                    'error': data.get('error')
                }
            else:
                return {
                    'success': False,
                    'error': f'Erro da API: {response.status_code}'
                }
                
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def download_video(self, video_url: str, local_path: str) -> Dict[str, Any]:
        """Download do vídeo gerado"""
        try:
            headers = {
                'Authorization': f'Bearer {self.api_key}'
            }
            
            response = requests.get(video_url, headers=headers, stream=True)
            
            if response.status_code == 200:
                with open(local_path, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)
                
                return {
                    'success': True,
                    'local_path': local_path,
                    'size': len(response.content)
                }
            else:
                return {
                    'success': False,
                    'error': f'Erro no download: {response.status_code}'
                }
                
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def list_models(self) -> Dict[str, Any]:
        """Listar modelos disponíveis"""
        if not self.is_configured():
            return {
                'success': False,
                'error': 'Runway ML não está configurado'
            }
        
        try:
            headers = {
                'Authorization': f'Bearer {self.api_key}',
                'Content-Type': 'application/json'
            }
            
            response = requests.get(
                f"{self.base_url}/models",
                headers=headers,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                return {
                    'success': True,
                    'models': data.get('models', [])
                }
            else:
                return {
                    'success': False,
                    'error': f'Erro da API: {response.status_code}'
                }
                
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def get_usage(self) -> Dict[str, Any]:
        """Obter informações de uso"""
        if not self.is_configured():
            return {
                'success': False,
                'error': 'Runway ML não está configurado'
            }
        
        try:
            headers = {
                'Authorization': f'Bearer {self.api_key}',
                'Content-Type': 'application/json'
            }
            
            response = requests.get(
                f"{self.base_url}/usage",
                headers=headers,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                return {
                    'success': True,
                    'usage': data
                }
            else:
                return {
                    'success': False,
                    'error': f'Erro da API: {response.status_code}'
                }
                
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def test_connection(self) -> Dict[str, Any]:
        """Testar conexão com Runway ML"""
        try:
            if not self.is_configured():
                return {
                    'connected': False,
                    'message': 'API key não configurada',
                    'response_time': 0
                }
            
            if not self.is_enabled():
                return {
                    'connected': False,
                    'message': 'Serviço desabilitado',
                    'response_time': 0
                }
            
            import time
            start_time = time.time()
            
            # Testar listagem de modelos
            result = self.list_models()
            
            response_time = time.time() - start_time
            
            if result['success']:
                return {
                    'connected': True,
                    'message': 'Conexão com Runway ML estabelecida com sucesso',
                    'response_time': round(response_time, 2),
                    'models_available': len(result.get('models', []))
                }
            else:
                return {
                    'connected': False,
                    'message': result['error'],
                    'response_time': round(response_time, 2)
                }
                
        except Exception as e:
            return {
                'connected': False,
                'message': str(e),
                'response_time': 0
            }

# Instância global
runway_service = RunwayService()