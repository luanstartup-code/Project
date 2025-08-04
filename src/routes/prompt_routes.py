from flask import Blueprint, request, jsonify
from src.utils.auth_manager import login_required
from src.services.chat_service import chat_service
from src.services.ai.gemini_service import gemini_service
import logging

logger = logging.getLogger(__name__)

prompt_bp = Blueprint('prompt', __name__)

@prompt_bp.route('/enhance', methods=['POST'])
@login_required
def enhance_prompt():
    """Aprimorar prompt simples"""
    try:
        data = request.get_json()
        
        if not data or 'prompt' not in data:
            return jsonify({
                'error': 'Prompt é obrigatório'
            }), 400
        
        simple_prompt = data['prompt'].strip()
        if not simple_prompt:
            return jsonify({
                'error': 'Prompt não pode estar vazio'
            }), 400
        
        # Opções de estilo
        style_options = {
            'animation_style': data.get('animation_style', 'realista'),
            'writing_tone': data.get('writing_tone', 'profissional'),
            'creativity_level': data.get('creativity_level', 'moderado')
        }
        
        # Aprimorar prompt
        result = chat_service.enhance_prompt(simple_prompt, style_options)
        
        if result['success']:
            return jsonify({
                'success': True,
                'data': result
            }), 200
        else:
            return jsonify({
                'error': result.get('error', 'Erro ao aprimorar prompt')
            }), 500
            
    except Exception as e:
        logger.error(f"Erro ao aprimorar prompt: {str(e)}")
        return jsonify({
            'error': 'Erro interno do servidor'
        }), 500

@prompt_bp.route('/styles', methods=['GET'])
@login_required
def get_style_options():
    """Obter opções de estilo disponíveis"""
    try:
        style_options = {
            'animation_styles': [
                {
                    'id': 'realista',
                    'name': 'Realista',
                    'description': 'Estilo fotorrealista com alta qualidade'
                },
                {
                    'id': 'cartoon',
                    'name': 'Cartoon',
                    'description': 'Estilo cartoon colorido e vibrante'
                },
                {
                    'id': 'anime',
                    'name': 'Anime',
                    'description': 'Estilo anime japonês'
                },
                {
                    'id': 'sketch',
                    'name': 'Sketch',
                    'description': 'Estilo esboço/desenho à mão'
                },
                {
                    'id': 'oil_painting',
                    'name': 'Pintura a Óleo',
                    'description': 'Estilo pintura a óleo clássica'
                },
                {
                    'id': 'watercolor',
                    'name': 'Aquarela',
                    'description': 'Estilo aquarela suave'
                },
                {
                    'id': 'digital_art',
                    'name': 'Arte Digital',
                    'description': 'Arte digital moderna'
                },
                {
                    'id': 'cyberpunk',
                    'name': 'Cyberpunk',
                    'description': 'Estilo futurista cyberpunk'
                }
            ],
            'writing_tones': [
                {
                    'id': 'profissional',
                    'name': 'Profissional',
                    'description': 'Tom formal e técnico'
                },
                {
                    'id': 'casual',
                    'name': 'Casual',
                    'description': 'Tom descontraído e amigável'
                },
                {
                    'id': 'entusiasmado',
                    'name': 'Entusiasmado',
                    'description': 'Tom energético e motivacional'
                },
                {
                    'id': 'poetico',
                    'name': 'Poético',
                    'description': 'Tom artístico e expressivo'
                },
                {
                    'id': 'tecnico',
                    'name': 'Técnico',
                    'description': 'Tom preciso e detalhado'
                },
                {
                    'id': 'narrativo',
                    'name': 'Narrativo',
                    'description': 'Tom storytelling'
                }
            ],
            'creativity_levels': [
                {
                    'id': 'conservador',
                    'name': 'Conservador',
                    'description': 'Abordagem segura e tradicional'
                },
                {
                    'id': 'moderado',
                    'name': 'Moderado',
                    'description': 'Equilíbrio entre criatividade e praticidade'
                },
                {
                    'id': 'criativo',
                    'name': 'Criativo',
                    'description': 'Abordagem inovadora e única'
                },
                {
                    'id': 'experimental',
                    'name': 'Experimental',
                    'description': 'Máxima criatividade e experimentação'
                }
            ]
        }
        
        return jsonify({
            'success': True,
            'data': style_options
        }), 200
        
    except Exception as e:
        logger.error(f"Erro ao obter opções de estilo: {str(e)}")
        return jsonify({
            'error': 'Erro interno do servidor'
        }), 500

@prompt_bp.route('/test-apis', methods=['GET'])
@login_required
def test_apis():
    """Testar status das APIs de IA"""
    try:
        user_id = request.current_user
        
        results = {
            'openai': {
                'available': chat_service.is_openai_available(),
                'model': chat_service.openai_model,
                'status': 'not_tested'
            },
            'gemini': {
                'available': gemini_service.is_available(),
                'model': gemini_service.model_name if gemini_service.is_available() else None,
                'status': 'not_tested'
            }
        }
        
        # Testar OpenAI
        if results['openai']['available']:
            try:
                openai_test = chat_service.send_message(
                    "Diga apenas 'OK OpenAI'",
                    user_id=user_id,
                    conversation_id=f"test_openai_{user_id}",
                    prefer_model="openai"
                )
                results['openai']['status'] = 'success' if openai_test['success'] else 'error'
                results['openai']['test_response'] = openai_test.get('content', openai_test.get('error'))
            except Exception as e:
                results['openai']['status'] = 'error'
                results['openai']['test_response'] = str(e)
        
        # Testar Gemini
        if results['gemini']['available']:
            try:
                gemini_test = gemini_service.test_connection()
                results['gemini']['status'] = 'success' if gemini_test['success'] else 'error'
                results['gemini']['test_response'] = gemini_test.get('response', gemini_test.get('error'))
            except Exception as e:
                results['gemini']['status'] = 'error'
                results['gemini']['test_response'] = str(e)
        
        # Status geral
        overall_status = 'success' if any(
            api['status'] == 'success' for api in results.values()
        ) else 'error'
        
        return jsonify({
            'success': True,
            'overall_status': overall_status,
            'apis': results,
            'fallback_available': results['gemini']['status'] == 'success'
        }), 200
        
    except Exception as e:
        logger.error(f"Erro ao testar APIs: {str(e)}")
        return jsonify({
            'error': 'Erro interno do servidor'
        }), 500

@prompt_bp.route('/templates', methods=['GET'])
@login_required
def get_prompt_templates():
    """Obter templates de prompt pré-definidos"""
    try:
        templates = {
            'video_generation': [
                {
                    'id': 'product_demo',
                    'name': 'Demo de Produto',
                    'template': 'Crie um vídeo demonstrativo do produto {product_name} mostrando suas principais funcionalidades de forma {tone}',
                    'variables': ['product_name', 'tone'],
                    'category': 'marketing'
                },
                {
                    'id': 'tutorial',
                    'name': 'Tutorial',
                    'template': 'Desenvolva um tutorial passo a passo sobre {topic} com estilo {style} e duração de {duration}',
                    'variables': ['topic', 'style', 'duration'],
                    'category': 'educacional'
                },
                {
                    'id': 'storytelling',
                    'name': 'Storytelling',
                    'template': 'Conte uma história envolvente sobre {theme} no estilo {narrative_style} com tom {emotion}',
                    'variables': ['theme', 'narrative_style', 'emotion'],
                    'category': 'criativo'
                }
            ],
            'avatar_creation': [
                {
                    'id': 'professional',
                    'name': 'Avatar Profissional',
                    'template': 'Crie um avatar profissional para {profession} com aparência {appearance} e estilo {style}',
                    'variables': ['profession', 'appearance', 'style'],
                    'category': 'profissional'
                },
                {
                    'id': 'character',
                    'name': 'Personagem',
                    'template': 'Desenvolva um personagem {character_type} com personalidade {personality} e visual {visual_style}',
                    'variables': ['character_type', 'personality', 'visual_style'],
                    'category': 'personagem'
                }
            ],
            'content_creation': [
                {
                    'id': 'social_media',
                    'name': 'Conteúdo Social Media',
                    'template': 'Gere conteúdo para {platform} sobre {topic} com tom {tone} e CTA {call_to_action}',
                    'variables': ['platform', 'topic', 'tone', 'call_to_action'],
                    'category': 'marketing'
                },
                {
                    'id': 'blog_post',
                    'name': 'Post de Blog',
                    'template': 'Escreva um artigo sobre {subject} com foco em {target_audience} e tom {writing_style}',
                    'variables': ['subject', 'target_audience', 'writing_style'],
                    'category': 'conteudo'
                }
            ]
        }
        
        return jsonify({
            'success': True,
            'data': templates
        }), 200
        
    except Exception as e:
        logger.error(f"Erro ao obter templates: {str(e)}")
        return jsonify({
            'error': 'Erro interno do servidor'
        }), 500

@prompt_bp.route('/analyze', methods=['POST'])
@login_required
def analyze_prompt():
    """Analisar prompt para sugestões de melhoria"""
    try:
        data = request.get_json()
        
        if not data or 'prompt' not in data:
            return jsonify({
                'error': 'Prompt é obrigatório'
            }), 400
        
        prompt = data['prompt'].strip()
        analysis_type = data.get('analysis_type', 'general')
        
        if not prompt:
            return jsonify({
                'error': 'Prompt não pode estar vazio'
            }), 400
        
        # Analisar com Gemini
        if gemini_service.is_available():
            result = gemini_service.analyze_content(prompt, analysis_type)
            
            # Adicionar métricas básicas
            metrics = {
                'length': len(prompt),
                'word_count': len(prompt.split()),
                'sentences': len([s for s in prompt.split('.') if s.strip()]),
                'complexity_score': min(10, len(prompt.split()) / 10)  # Score simples
            }
            
            if result['success']:
                return jsonify({
                    'success': True,
                    'analysis': result['content'],
                    'metrics': metrics,
                    'suggestions': [
                        'Adicione mais detalhes específicos',
                        'Inclua o contexto desejado',
                        'Especifique o estilo visual',
                        'Defina a duração ou formato'
                    ]
                }), 200
            else:
                return jsonify({
                    'error': result.get('error', 'Erro na análise')
                }), 500
        else:
            return jsonify({
                'error': 'Serviço de análise não disponível'
            }), 503
            
    except Exception as e:
        logger.error(f"Erro ao analisar prompt: {str(e)}")
        return jsonify({
            'error': 'Erro interno do servidor'
        }), 500