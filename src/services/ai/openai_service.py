import openai
import json
from typing import Dict, Any, Optional, Generator
from src.utils.config_manager import config_manager

class OpenAIService:
    """Serviço para integração com OpenAI"""
    
    def __init__(self):
        self.api_key = config_manager.get_api_key('ai', 'openai')
        self.model = config_manager.get('ai.openai.model', 'gpt-4')
        self.max_tokens = config_manager.get('ai.openai.max_tokens', 4000)
        self.temperature = config_manager.get('ai.openai.temperature', 0.7)
        
        if self.api_key:
            openai.api_key = self.api_key
    
    def is_configured(self) -> bool:
        """Verificar se o serviço está configurado"""
        return bool(self.api_key)
    
    def is_enabled(self) -> bool:
        """Verificar se o serviço está habilitado"""
        return config_manager.is_service_enabled('ai', 'openai')
    
    def chat_completion(self, messages: list, stream: bool = False) -> Dict[str, Any]:
        """Completar chat com GPT"""
        if not self.is_configured() or not self.is_enabled():
            raise Exception("OpenAI não está configurado ou habilitado")
        
        try:
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=messages,
                max_tokens=self.max_tokens,
                temperature=self.temperature,
                stream=stream
            )
            
            if stream:
                return response
            else:
                return {
                    'content': response.choices[0].message.content,
                    'usage': response.usage.to_dict() if response.usage else None,
                    'model': response.model
                }
                
        except openai.error.AuthenticationError:
            raise Exception("API key inválida")
        except openai.error.RateLimitError:
            raise Exception("Rate limit excedido")
        except openai.error.APIError as e:
            raise Exception(f"Erro da API OpenAI: {str(e)}")
        except Exception as e:
            raise Exception(f"Erro inesperado: {str(e)}")
    
    def chat_completion_stream(self, messages: list) -> Generator[str, None, None]:
        """Completar chat com streaming"""
        if not self.is_configured() or not self.is_enabled():
            raise Exception("OpenAI não está configurado ou habilitado")
        
        try:
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=messages,
                max_tokens=self.max_tokens,
                temperature=self.temperature,
                stream=True
            )
            
            for chunk in response:
                if chunk.choices[0].delta.content:
                    yield chunk.choices[0].delta.content
                    
        except openai.error.AuthenticationError:
            raise Exception("API key inválida")
        except openai.error.RateLimitError:
            raise Exception("Rate limit excedido")
        except openai.error.APIError as e:
            raise Exception(f"Erro da API OpenAI: {str(e)}")
        except Exception as e:
            raise Exception(f"Erro inesperado: {str(e)}")
    
    def generate_image(self, prompt: str, size: str = "1024x1024", quality: str = "standard") -> str:
        """Gerar imagem com DALL-E"""
        if not self.is_configured() or not self.is_enabled():
            raise Exception("OpenAI não está configurado ou habilitado")
        
        try:
            response = openai.Image.create(
                prompt=prompt,
                size=size,
                quality=quality
            )
            
            return response.data[0].url
            
        except openai.error.AuthenticationError:
            raise Exception("API key inválida")
        except openai.error.RateLimitError:
            raise Exception("Rate limit excedido")
        except openai.error.APIError as e:
            raise Exception(f"Erro da API OpenAI: {str(e)}")
        except Exception as e:
            raise Exception(f"Erro inesperado: {str(e)}")
    
    def transcribe_audio(self, audio_file_path: str) -> str:
        """Transcrever áudio com Whisper"""
        if not self.is_configured() or not self.is_enabled():
            raise Exception("OpenAI não está configurado ou habilitado")
        
        try:
            with open(audio_file_path, "rb") as audio_file:
                response = openai.Audio.transcribe(
                    model="whisper-1",
                    file=audio_file
                )
            
            return response.text
            
        except openai.error.AuthenticationError:
            raise Exception("API key inválida")
        except openai.error.RateLimitError:
            raise Exception("Rate limit excedido")
        except openai.error.APIError as e:
            raise Exception(f"Erro da API OpenAI: {str(e)}")
        except Exception as e:
            raise Exception(f"Erro inesperado: {str(e)}")
    
    def test_connection(self) -> Dict[str, Any]:
        """Testar conexão com OpenAI"""
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
            
            # Teste simples
            response = self.chat_completion([
                {"role": "user", "content": "Diga apenas 'OK' se você está funcionando."}
            ])
            
            response_time = time.time() - start_time
            
            if response['content'].strip().lower() in ['ok', 'ok.', 'ok!']:
                return {
                    'connected': True,
                    'message': 'Conexão com OpenAI estabelecida com sucesso',
                    'response_time': round(response_time, 2)
                }
            else:
                return {
                    'connected': False,
                    'message': 'Resposta inesperada da API',
                    'response_time': round(response_time, 2)
                }
                
        except Exception as e:
            return {
                'connected': False,
                'message': str(e),
                'response_time': 0
            }

# Instância global
openai_service = OpenAIService()