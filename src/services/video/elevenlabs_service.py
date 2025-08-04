import requests
import json
import os
from typing import Dict, Any, List, Optional
from src.utils.config_manager import config_manager

class ElevenLabsService:
    """Serviço para integração com ElevenLabs"""
    
    def __init__(self):
        self.api_key = config_manager.get_api_key('video', 'elevenlabs')
        self.base_url = "https://api.elevenlabs.io/v1"
        self.default_voice_id = config_manager.get('video.elevenlabs.voice_id', '')
        self.stability = config_manager.get('video.elevenlabs.stability', 0.5)
    
    def is_configured(self) -> bool:
        """Verificar se o serviço está configurado"""
        return bool(self.api_key)
    
    def is_enabled(self) -> bool:
        """Verificar se o serviço está habilitado"""
        return config_manager.is_service_enabled('video', 'elevenlabs')
    
    def text_to_speech(self, text: str, voice_id: str = None, output_path: str = None) -> Dict[str, Any]:
        """Converter texto em áudio"""
        if not self.is_configured() or not self.is_enabled():
            return {
                'success': False,
                'error': 'ElevenLabs não está configurado ou habilitado'
            }
        
        try:
            voice_id = voice_id or self.default_voice_id
            if not voice_id:
                return {
                    'success': False,
                    'error': 'Voice ID não configurado'
                }
            
            headers = {
                'xi-api-key': self.api_key,
                'Content-Type': 'application/json'
            }
            
            payload = {
                'text': text,
                'model_id': 'eleven_monolingual_v1',
                'voice_settings': {
                    'stability': self.stability,
                    'similarity_boost': 0.5
                }
            }
            
            response = requests.post(
                f"{self.base_url}/text-to-speech/{voice_id}",
                headers=headers,
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                # Salvar áudio
                if not output_path:
                    import uuid
                    output_path = f"src/static/assets/audio/{uuid.uuid4()}.mp3"
                
                os.makedirs(os.path.dirname(output_path), exist_ok=True)
                
                with open(output_path, 'wb') as f:
                    f.write(response.content)
                
                return {
                    'success': True,
                    'audio_path': output_path,
                    'size': len(response.content),
                    'duration': self._estimate_duration(text)
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
    
    def get_voices(self) -> Dict[str, Any]:
        """Listar vozes disponíveis"""
        if not self.is_configured():
            return {
                'success': False,
                'error': 'ElevenLabs não está configurado'
            }
        
        try:
            headers = {
                'xi-api-key': self.api_key,
                'Content-Type': 'application/json'
            }
            
            response = requests.get(
                f"{self.base_url}/voices",
                headers=headers,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                return {
                    'success': True,
                    'voices': data.get('voices', [])
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
    
    def get_voice(self, voice_id: str) -> Dict[str, Any]:
        """Obter detalhes de uma voz específica"""
        if not self.is_configured():
            return {
                'success': False,
                'error': 'ElevenLabs não está configurado'
            }
        
        try:
            headers = {
                'xi-api-key': self.api_key,
                'Content-Type': 'application/json'
            }
            
            response = requests.get(
                f"{self.base_url}/voices/{voice_id}",
                headers=headers,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                return {
                    'success': True,
                    'voice': data
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
    
    def clone_voice(self, name: str, description: str, audio_files: List[str]) -> Dict[str, Any]:
        """Clonar voz a partir de arquivos de áudio"""
        if not self.is_configured() or not self.is_enabled():
            return {
                'success': False,
                'error': 'ElevenLabs não está configurado ou habilitado'
            }
        
        try:
            headers = {
                'xi-api-key': self.api_key
            }
            
            files = []
            for i, audio_file in enumerate(audio_files):
                if os.path.exists(audio_file):
                    files.append(('files', (f'audio_{i}.mp3', open(audio_file, 'rb'), 'audio/mpeg')))
            
            data = {
                'name': name,
                'description': description
            }
            
            response = requests.post(
                f"{self.base_url}/voices/add",
                headers=headers,
                data=data,
                files=files,
                timeout=60
            )
            
            # Fechar arquivos
            for _, file_tuple in files:
                file_tuple[1].close()
            
            if response.status_code == 200:
                data = response.json()
                return {
                    'success': True,
                    'voice_id': data.get('voice_id'),
                    'voice': data
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
    
    def delete_voice(self, voice_id: str) -> Dict[str, Any]:
        """Deletar voz"""
        if not self.is_configured():
            return {
                'success': False,
                'error': 'ElevenLabs não está configurado'
            }
        
        try:
            headers = {
                'xi-api-key': self.api_key,
                'Content-Type': 'application/json'
            }
            
            response = requests.delete(
                f"{self.base_url}/voices/{voice_id}",
                headers=headers,
                timeout=10
            )
            
            if response.status_code == 200:
                return {
                    'success': True,
                    'message': 'Voz deletada com sucesso'
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
                'error': 'ElevenLabs não está configurado'
            }
        
        try:
            headers = {
                'xi-api-key': self.api_key,
                'Content-Type': 'application/json'
            }
            
            response = requests.get(
                f"{self.base_url}/user/subscription",
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
    
    def _estimate_duration(self, text: str) -> float:
        """Estimar duração do áudio baseado no texto"""
        # Estimativa: ~150 palavras por minuto
        words = len(text.split())
        return (words / 150) * 60
    
    def test_connection(self) -> Dict[str, Any]:
        """Testar conexão com ElevenLabs"""
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
            
            # Testar listagem de vozes
            result = self.get_voices()
            
            response_time = time.time() - start_time
            
            if result['success']:
                return {
                    'connected': True,
                    'message': 'Conexão com ElevenLabs estabelecida com sucesso',
                    'response_time': round(response_time, 2),
                    'voices_available': len(result.get('voices', []))
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
elevenlabs_service = ElevenLabsService()