import os
import json
import openai
from typing import Dict, Optional, Any, List, Generator
from datetime import datetime
import logging
from src.services.ai.gemini_service import gemini_service

logger = logging.getLogger(__name__)

class ChatService:
    """Serviço de chat com IA - OpenAI com fallback para Gemini"""
    
    def __init__(self):
        # Configuração OpenAI
        self.openai_api_key = os.getenv('OPENAI_API_KEY')
        self.openai_model = os.getenv('OPENAI_MODEL', 'gpt-4')
        self.max_tokens = int(os.getenv('OPENAI_MAX_TOKENS', 4000))
        self.temperature = float(os.getenv('OPENAI_TEMPERATURE', 0.7))
        
        if self.openai_api_key:
            openai.api_key = self.openai_api_key
        
        # Sistema de fallback
        self.fallback_enabled = True
        
        # Histórico de conversas
        self.conversations = {}
    
    def is_openai_available(self) -> bool:
        """Verificar se OpenAI está disponível"""
        return bool(self.openai_api_key)
    
    def get_available_models(self) -> List[str]:
        """Obter modelos disponíveis"""
        models = []
        
        if self.is_openai_available():
            models.append('OpenAI GPT-4')
        
        if gemini_service.is_available():
            models.append('Google Gemini Pro')
        
        return models
    
    def send_message(self, 
                    message: str, 
                    user_id: str = "default",
                    conversation_id: str = None,
                    prefer_model: str = "openai",
                    **kwargs) -> Dict[str, Any]:
        """Enviar mensagem com sistema de fallback"""
        
        # Configurar conversa
        if not conversation_id:
            conversation_id = f"{user_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        # Inicializar conversa se não existir
        if conversation_id not in self.conversations:
            self.conversations[conversation_id] = {
                'user_id': user_id,
                'created_at': datetime.now().isoformat(),
                'messages': []
            }
        
        # Adicionar mensagem do usuário ao histórico
        self.conversations[conversation_id]['messages'].append({
            'role': 'user',
            'content': message,
            'timestamp': datetime.now().isoformat()
        })
        
        # Tentar OpenAI primeiro (se preferido e disponível)
        if prefer_model == "openai" and self.is_openai_available():
            try:
                result = self._send_openai_message(message, conversation_id, **kwargs)
                if result['success']:
                    # Adicionar resposta ao histórico
                    self.conversations[conversation_id]['messages'].append({
                        'role': 'assistant',
                        'content': result['content'],
                        'model': 'OpenAI',
                        'timestamp': datetime.now().isoformat()
                    })
                    return result
            except Exception as e:
                logger.warning(f"OpenAI falhou: {str(e)}")
                
                # Usar Gemini como fallback
                if self.fallback_enabled and gemini_service.is_available():
                    logger.info("Usando Gemini como fallback")
                    return self._send_gemini_message(message, conversation_id, **kwargs)
        
        # Usar Gemini diretamente ou como fallback
        elif gemini_service.is_available():
            result = self._send_gemini_message(message, conversation_id, **kwargs)
            if result['success']:
                # Adicionar resposta ao histórico
                self.conversations[conversation_id]['messages'].append({
                    'role': 'assistant',
                    'content': result['content'],
                    'model': 'Gemini',
                    'timestamp': datetime.now().isoformat()
                })
            return result
        
        # Nenhum serviço disponível
        return {
            'success': False,
            'error': 'Nenhum serviço de IA disponível',
            'conversation_id': conversation_id
        }
    
    def _send_openai_message(self, message: str, conversation_id: str, **kwargs) -> Dict[str, Any]:
        """Enviar mensagem via OpenAI"""
        try:
            # Preparar mensagens com contexto
            messages = self._prepare_openai_messages(conversation_id, message)
            
            response = openai.ChatCompletion.create(
                model=kwargs.get('model', self.openai_model),
                messages=messages,
                max_tokens=kwargs.get('max_tokens', self.max_tokens),
                temperature=kwargs.get('temperature', self.temperature),
                top_p=kwargs.get('top_p', 1.0),
                frequency_penalty=kwargs.get('frequency_penalty', 0),
                presence_penalty=kwargs.get('presence_penalty', 0)
            )
            
            content = response.choices[0].message.content
            
            return {
                'success': True,
                'content': content,
                'model': 'OpenAI',
                'conversation_id': conversation_id,
                'tokens_used': response.usage.total_tokens,
                'finish_reason': response.choices[0].finish_reason
            }
            
        except Exception as e:
            logger.error(f"Erro OpenAI: {str(e)}")
            return {
                'success': False,
                'error': f'OpenAI error: {str(e)}',
                'conversation_id': conversation_id
            }
    
    def _send_gemini_message(self, message: str, conversation_id: str, **kwargs) -> Dict[str, Any]:
        """Enviar mensagem via Gemini"""
        try:
            # Preparar prompt com contexto
            context_prompt = self._prepare_gemini_context(conversation_id, message)
            
            result = gemini_service.generate_text(
                context_prompt,
                max_tokens=kwargs.get('max_tokens', self.max_tokens),
                temperature=kwargs.get('temperature', self.temperature)
            )
            
            if result['success']:
                result['conversation_id'] = conversation_id
                result['model'] = 'Gemini (Fallback)' if kwargs.get('is_fallback') else 'Gemini'
            
            return result
            
        except Exception as e:
            logger.error(f"Erro Gemini: {str(e)}")
            return {
                'success': False,
                'error': f'Gemini error: {str(e)}',
                'conversation_id': conversation_id
            }
    
    def _prepare_openai_messages(self, conversation_id: str, current_message: str) -> List[Dict]:
        """Preparar mensagens para OpenAI com contexto"""
        messages = [
            {
                "role": "system",
                "content": "Você é um assistente de IA especializado em criação de conteúdo para vídeos, avatares e projetos criativos. Seja útil, criativo e detalhado em suas respostas."
            }
        ]
        
        # Adicionar histórico da conversa (últimas 10 mensagens)
        if conversation_id in self.conversations:
            recent_messages = self.conversations[conversation_id]['messages'][-10:]
            for msg in recent_messages:
                if msg['role'] in ['user', 'assistant']:
                    messages.append({
                        "role": msg['role'],
                        "content": msg['content']
                    })
        
        # Adicionar mensagem atual
        messages.append({
            "role": "user",
            "content": current_message
        })
        
        return messages
    
    def _prepare_gemini_context(self, conversation_id: str, current_message: str) -> str:
        """Preparar contexto para Gemini"""
        context = "Você é um assistente de IA especializado em criação de conteúdo para vídeos, avatares e projetos criativos. Seja útil, criativo e detalhado em suas respostas.\n\n"
        
        # Adicionar histórico da conversa
        if conversation_id in self.conversations:
            recent_messages = self.conversations[conversation_id]['messages'][-8:]
            for msg in recent_messages:
                if msg['role'] == 'user':
                    context += f"Usuário: {msg['content']}\n"
                elif msg['role'] == 'assistant':
                    context += f"Assistente: {msg['content']}\n"
        
        # Adicionar mensagem atual
        context += f"Usuário: {current_message}\nAssistente:"
        
        return context
    
    def send_message_stream(self, 
                           message: str, 
                           user_id: str = "default",
                           conversation_id: str = None,
                           prefer_model: str = "openai",
                           **kwargs) -> Generator[str, None, None]:
        """Enviar mensagem com streaming"""
        
        if not conversation_id:
            conversation_id = f"{user_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        # Tentar OpenAI streaming primeiro
        if prefer_model == "openai" and self.is_openai_available():
            try:
                yield from self._stream_openai_message(message, conversation_id, **kwargs)
                return
            except Exception as e:
                logger.warning(f"OpenAI streaming falhou: {str(e)}")
                
                # Fallback para Gemini
                if self.fallback_enabled and gemini_service.is_available():
                    yield json.dumps({
                        'info': 'Fallback para Gemini ativado',
                        'model': 'Gemini'
                    })
                    yield from gemini_service.generate_stream(message, **kwargs)
                    return
        
        # Usar Gemini streaming
        elif gemini_service.is_available():
            yield from gemini_service.generate_stream(message, **kwargs)
            return
        
        # Nenhum serviço disponível
        yield json.dumps({
            'error': 'Nenhum serviço de IA disponível para streaming'
        })
    
    def _stream_openai_message(self, message: str, conversation_id: str, **kwargs) -> Generator[str, None, None]:
        """Streaming OpenAI"""
        try:
            messages = self._prepare_openai_messages(conversation_id, message)
            
            response = openai.ChatCompletion.create(
                model=kwargs.get('model', self.openai_model),
                messages=messages,
                max_tokens=kwargs.get('max_tokens', self.max_tokens),
                temperature=kwargs.get('temperature', self.temperature),
                stream=True
            )
            
            for chunk in response:
                if chunk.choices[0].delta.get('content'):
                    yield json.dumps({
                        'content': chunk.choices[0].delta.content,
                        'model': 'OpenAI'
                    })
                    
        except Exception as e:
            yield json.dumps({
                'error': f'OpenAI streaming error: {str(e)}'
            })
    
    def enhance_prompt(self, simple_prompt: str, style_options: Dict = None) -> Dict[str, Any]:
        """Aprimorar prompt usando IA"""
        # Usar Gemini preferencialmente para enhancement
        if gemini_service.is_available():
            return gemini_service.enhance_prompt(simple_prompt, style_options)
        
        # Fallback para OpenAI
        elif self.is_openai_available():
            return self._enhance_prompt_openai(simple_prompt, style_options)
        
        return {
            'success': False,
            'error': 'Nenhum serviço de IA disponível para aprimoramento'
        }
    
    def _enhance_prompt_openai(self, simple_prompt: str, style_options: Dict = None) -> Dict[str, Any]:
        """Aprimorar prompt usando OpenAI"""
        if not style_options:
            style_options = {
                'animation_style': 'realista',
                'writing_tone': 'profissional',
                'creativity_level': 'moderado'
            }
        
        enhancement_prompt = f"""
        Como especialista em prompts para IA, aprimore o seguinte prompt simples:

        PROMPT ORIGINAL: "{simple_prompt}"

        CONFIGURAÇÕES:
        - Estilo: {style_options.get('animation_style', 'realista')}
        - Tom: {style_options.get('writing_tone', 'profissional')}
        - Criatividade: {style_options.get('creativity_level', 'moderado')}

        Retorne apenas o prompt aprimorado:
        """
        
        try:
            response = openai.ChatCompletion.create(
                model=self.openai_model,
                messages=[{"role": "user", "content": enhancement_prompt}],
                max_tokens=500,
                temperature=0.7
            )
            
            enhanced_prompt = response.choices[0].message.content.strip()
            
            return {
                'success': True,
                'original_prompt': simple_prompt,
                'enhanced_prompt': enhanced_prompt,
                'style_options': style_options,
                'model': 'OpenAI'
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': f'OpenAI enhancement error: {str(e)}'
            }
    
    def get_conversation_history(self, conversation_id: str) -> Dict[str, Any]:
        """Obter histórico da conversa"""
        if conversation_id in self.conversations:
            return {
                'success': True,
                'conversation': self.conversations[conversation_id]
            }
        else:
            return {
                'success': False,
                'error': 'Conversa não encontrada'
            }
    
    def clear_conversation(self, conversation_id: str) -> Dict[str, Any]:
        """Limpar conversa"""
        if conversation_id in self.conversations:
            del self.conversations[conversation_id]
            return {
                'success': True,
                'message': 'Conversa limpa com sucesso'
            }
        else:
            return {
                'success': False,
                'error': 'Conversa não encontrada'
            }
    
    def get_service_status(self) -> Dict[str, Any]:
        """Status dos serviços"""
        return {
            'openai': {
                'available': self.is_openai_available(),
                'model': self.openai_model
            },
            'gemini': {
                'available': gemini_service.is_available(),
                'model': gemini_service.model_name if gemini_service.is_available() else None
            },
            'fallback_enabled': self.fallback_enabled,
            'active_conversations': len(self.conversations)
        }

# Instância global
chat_service = ChatService()