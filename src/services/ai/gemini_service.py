import os
import json
import google.generativeai as genai
from typing import Dict, Optional, Any, List, Generator
import logging

logger = logging.getLogger(__name__)

class GeminiService:
    """Serviço para integração com Google Gemini AI"""
    
    def __init__(self):
        self.api_key = os.getenv('GEMINI_API_KEY')
        self.model_name = os.getenv('GEMINI_MODEL', 'gemini-pro')
        self.max_tokens = int(os.getenv('GEMINI_MAX_TOKENS', 4000))
        self.temperature = float(os.getenv('GEMINI_TEMPERATURE', 0.7))
        
        if self.api_key:
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel(self.model_name)
        else:
            self.model = None
            logger.warning("Gemini API key not configured")
    
    def is_available(self) -> bool:
        """Verificar se o serviço está disponível"""
        return bool(self.api_key and self.model)
    
    def generate_text(self, prompt: str, **kwargs) -> Dict[str, Any]:
        """Gerar texto usando Gemini"""
        if not self.is_available():
            return {
                'success': False,
                'error': 'Gemini service not available'
            }
        
        try:
            # Configuração da geração
            generation_config = genai.types.GenerationConfig(
                max_output_tokens=kwargs.get('max_tokens', self.max_tokens),
                temperature=kwargs.get('temperature', self.temperature),
                top_p=kwargs.get('top_p', 0.8),
                top_k=kwargs.get('top_k', 40)
            )
            
            # Gerar resposta
            response = self.model.generate_content(
                prompt,
                generation_config=generation_config
            )
            
            if response.text:
                return {
                    'success': True,
                    'content': response.text,
                    'model': self.model_name,
                    'tokens_used': len(response.text.split()) * 1.3  # Estimativa
                }
            else:
                return {
                    'success': False,
                    'error': 'No content generated'
                }
                
        except Exception as e:
            logger.error(f"Erro no Gemini: {str(e)}")
            return {
                'success': False,
                'error': f'Gemini API error: {str(e)}'
            }
    
    def generate_stream(self, prompt: str, **kwargs) -> Generator[str, None, None]:
        """Gerar texto em streaming"""
        if not self.is_available():
            yield json.dumps({
                'error': 'Gemini service not available'
            })
            return
        
        try:
            # Configuração da geração
            generation_config = genai.types.GenerationConfig(
                max_output_tokens=kwargs.get('max_tokens', self.max_tokens),
                temperature=kwargs.get('temperature', self.temperature),
                top_p=kwargs.get('top_p', 0.8),
                top_k=kwargs.get('top_k', 40)
            )
            
            # Gerar resposta em streaming
            response = self.model.generate_content(
                prompt,
                generation_config=generation_config,
                stream=True
            )
            
            for chunk in response:
                if chunk.text:
                    yield json.dumps({
                        'content': chunk.text,
                        'model': self.model_name
                    })
                    
        except Exception as e:
            logger.error(f"Erro no streaming Gemini: {str(e)}")
            yield json.dumps({
                'error': f'Gemini streaming error: {str(e)}'
            })
    
    def enhance_prompt(self, simple_prompt: str, style_options: Dict = None) -> Dict[str, Any]:
        """Aprimorar prompt simples"""
        if not self.is_available():
            return {
                'success': False,
                'error': 'Gemini service not available'
            }
        
        # Opções de estilo padrão
        if not style_options:
            style_options = {
                'animation_style': 'realista',
                'writing_tone': 'profissional',
                'creativity_level': 'moderado'
            }
        
        enhancement_prompt = f"""
        Como especialista em prompts para IA, aprimore o seguinte prompt simples tornando-o mais detalhado e eficaz:

        PROMPT ORIGINAL: "{simple_prompt}"

        CONFIGURAÇÕES DE ESTILO:
        - Estilo de animação: {style_options.get('animation_style', 'realista')}
        - Tom de escrita: {style_options.get('writing_tone', 'profissional')}
        - Nível de criatividade: {style_options.get('creativity_level', 'moderado')}

        INSTRUÇÕES:
        1. Mantenha a intenção original do prompt
        2. Adicione detalhes técnicos relevantes
        3. Inclua especificações de qualidade
        4. Otimize para geração de vídeo/imagem
        5. Use linguagem clara e objetiva

        RETORNE APENAS O PROMPT APRIMORADO, SEM EXPLICAÇÕES ADICIONAIS:
        """
        
        try:
            response = self.model.generate_content(enhancement_prompt)
            
            if response.text:
                enhanced_prompt = response.text.strip()
                
                return {
                    'success': True,
                    'original_prompt': simple_prompt,
                    'enhanced_prompt': enhanced_prompt,
                    'style_options': style_options,
                    'model': self.model_name
                }
            else:
                return {
                    'success': False,
                    'error': 'No enhanced prompt generated'
                }
                
        except Exception as e:
            logger.error(f"Erro no enhancement: {str(e)}")
            return {
                'success': False,
                'error': f'Prompt enhancement error: {str(e)}'
            }
    
    def analyze_content(self, content: str, analysis_type: str = 'general') -> Dict[str, Any]:
        """Analisar conteúdo"""
        if not self.is_available():
            return {
                'success': False,
                'error': 'Gemini service not available'
            }
        
        analysis_prompts = {
            'general': f"Analise o seguinte conteúdo e forneça insights: {content}",
            'sentiment': f"Analise o sentimento do seguinte texto: {content}",
            'keywords': f"Extraia palavras-chave importantes do seguinte conteúdo: {content}",
            'summary': f"Resuma o seguinte conteúdo de forma concisa: {content}"
        }
        
        prompt = analysis_prompts.get(analysis_type, analysis_prompts['general'])
        
        return self.generate_text(prompt)
    
    def test_connection(self) -> Dict[str, Any]:
        """Testar conexão com a API"""
        if not self.api_key:
            return {
                'success': False,
                'error': 'API key not configured'
            }
        
        try:
            # Teste simples
            test_result = self.generate_text("Diga apenas 'OK' se você está funcionando.")
            
            if test_result['success']:
                return {
                    'success': True,
                    'message': 'Gemini connection successful',
                    'model': self.model_name,
                    'response': test_result.get('content', '')
                }
            else:
                return test_result
                
        except Exception as e:
            return {
                'success': False,
                'error': f'Connection test failed: {str(e)}'
            }

# Instância global
gemini_service = GeminiService()