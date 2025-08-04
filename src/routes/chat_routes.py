from flask import Blueprint, request, jsonify, Response, stream_template
from src.services.chat_service import chat_service
from src.utils.auth_manager import login_required
import json
import logging

logger = logging.getLogger(__name__)

chat_bp = Blueprint('chat', __name__)

@chat_bp.route('/send', methods=['POST'])
@login_required
def send_message():
    """Enviar mensagem para o chat"""
    try:
        data = request.get_json()
        user_id = request.current_user
        
        if not data or 'message' not in data:
            return jsonify({
                'error': 'Mensagem é obrigatória'
            }), 400
        
        message = data['message'].strip()
        if not message:
            return jsonify({
                'error': 'Mensagem não pode estar vazia'
            }), 400
        
        conversation_id = data.get('conversation_id')
        prefer_model = data.get('prefer_model', 'openai')
        
        # Configurações opcionais
        options = {
            'max_tokens': data.get('max_tokens', 4000),
            'temperature': data.get('temperature', 0.7),
            'top_p': data.get('top_p', 1.0)
        }
        
        # Enviar mensagem
        result = chat_service.send_message(
            message=message,
            user_id=user_id,
            conversation_id=conversation_id,
            prefer_model=prefer_model,
            **options
        )
        
        if result['success']:
            return jsonify({
                'success': True,
                'data': result
            }), 200
        else:
            return jsonify({
                'error': result.get('error', 'Erro ao enviar mensagem')
            }), 500
            
    except Exception as e:
        logger.error(f"Erro ao enviar mensagem: {str(e)}")
        return jsonify({
            'error': 'Erro interno do servidor'
        }), 500

@chat_bp.route('/stream', methods=['POST'])
@login_required
def send_message_stream():
    """Enviar mensagem com streaming"""
    try:
        data = request.get_json()
        user_id = request.current_user
        
        if not data or 'message' not in data:
            return jsonify({
                'error': 'Mensagem é obrigatória'
            }), 400
        
        message = data['message'].strip()
        if not message:
            return jsonify({
                'error': 'Mensagem não pode estar vazia'
            }), 400
        
        conversation_id = data.get('conversation_id')
        prefer_model = data.get('prefer_model', 'openai')
        
        # Configurações opcionais
        options = {
            'max_tokens': data.get('max_tokens', 4000),
            'temperature': data.get('temperature', 0.7)
        }
        
        def generate():
            try:
                for chunk in chat_service.send_message_stream(
                    message=message,
                    user_id=user_id,
                    conversation_id=conversation_id,
                    prefer_model=prefer_model,
                    **options
                ):
                    yield f"data: {chunk}\n\n"
                
                # Sinal de fim
                yield f"data: {json.dumps({'done': True})}\n\n"
                
            except Exception as e:
                logger.error(f"Erro no streaming: {str(e)}")
                yield f"data: {json.dumps({'error': str(e)})}\n\n"
        
        return Response(
            generate(),
            mimetype='text/plain',
            headers={
                'Cache-Control': 'no-cache',
                'Connection': 'keep-alive',
                'X-Accel-Buffering': 'no'
            }
        )
        
    except Exception as e:
        logger.error(f"Erro ao iniciar streaming: {str(e)}")
        return jsonify({
            'error': 'Erro interno do servidor'
        }), 500

@chat_bp.route('/conversations', methods=['GET'])
@login_required
def list_conversations():
    """Listar conversas do usuário"""
    try:
        user_id = request.current_user
        
        # Por enquanto, retornar conversas ativas do serviço
        conversations = []
        for conv_id, conv_data in chat_service.conversations.items():
            if conv_data['user_id'] == user_id:
                # Obter última mensagem
                last_message = None
                if conv_data['messages']:
                    last_message = conv_data['messages'][-1]
                
                conversations.append({
                    'id': conv_id,
                    'created_at': conv_data['created_at'],
                    'message_count': len(conv_data['messages']),
                    'last_message': last_message,
                    'title': last_message['content'][:50] + '...' if last_message and len(last_message['content']) > 50 else last_message['content'] if last_message else 'Nova conversa'
                })
        
        # Ordenar por data de criação (mais recentes primeiro)
        conversations.sort(key=lambda x: x['created_at'], reverse=True)
        
        return jsonify({
            'success': True,
            'conversations': conversations
        }), 200
        
    except Exception as e:
        logger.error(f"Erro ao listar conversas: {str(e)}")
        return jsonify({
            'error': 'Erro interno do servidor'
        }), 500

@chat_bp.route('/conversations/<conversation_id>', methods=['GET'])
@login_required
def get_conversation(conversation_id):
    """Obter conversa específica"""
    try:
        user_id = request.current_user
        
        result = chat_service.get_conversation_history(conversation_id)
        
        if result['success']:
            # Verificar se a conversa pertence ao usuário
            if result['conversation']['user_id'] != user_id:
                return jsonify({
                    'error': 'Acesso negado'
                }), 403
            
            return jsonify({
                'success': True,
                'conversation': result['conversation']
            }), 200
        else:
            return jsonify({
                'error': result.get('error', 'Conversa não encontrada')
            }), 404
            
    except Exception as e:
        logger.error(f"Erro ao obter conversa: {str(e)}")
        return jsonify({
            'error': 'Erro interno do servidor'
        }), 500

@chat_bp.route('/conversations/<conversation_id>', methods=['DELETE'])
@login_required
def delete_conversation(conversation_id):
    """Deletar conversa"""
    try:
        user_id = request.current_user
        
        # Verificar se a conversa pertence ao usuário
        if conversation_id in chat_service.conversations:
            if chat_service.conversations[conversation_id]['user_id'] != user_id:
                return jsonify({
                    'error': 'Acesso negado'
                }), 403
        
        result = chat_service.clear_conversation(conversation_id)
        
        if result['success']:
            return jsonify({
                'success': True,
                'message': result['message']
            }), 200
        else:
            return jsonify({
                'error': result.get('error', 'Erro ao deletar conversa')
            }), 500
            
    except Exception as e:
        logger.error(f"Erro ao deletar conversa: {str(e)}")
        return jsonify({
            'error': 'Erro interno do servidor'
        }), 500

@chat_bp.route('/models', methods=['GET'])
@login_required
def get_available_models():
    """Obter modelos disponíveis"""
    try:
        models = chat_service.get_available_models()
        status = chat_service.get_service_status()
        
        return jsonify({
            'success': True,
            'available_models': models,
            'service_status': status
        }), 200
        
    except Exception as e:
        logger.error(f"Erro ao obter modelos: {str(e)}")
        return jsonify({
            'error': 'Erro interno do servidor'
        }), 500

@chat_bp.route('/enhance-prompt', methods=['POST'])
@login_required
def enhance_prompt():
    """Aprimorar prompt usando IA"""
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

@chat_bp.route('/test', methods=['GET'])
@login_required
def test_chat_services():
    """Testar serviços de chat"""
    try:
        user_id = request.current_user
        test_conversation_id = f"test_{user_id}"
        
        results = {
            'openai': {'available': False, 'test_result': None},
            'gemini': {'available': False, 'test_result': None}
        }
        
        # Testar OpenAI
        if chat_service.is_openai_available():
            results['openai']['available'] = True
            try:
                openai_result = chat_service.send_message(
                    "Responda apenas 'OpenAI funcionando'",
                    user_id=user_id,
                    conversation_id=f"{test_conversation_id}_openai",
                    prefer_model="openai"
                )
                results['openai']['test_result'] = openai_result
            except Exception as e:
                results['openai']['test_result'] = {
                    'success': False,
                    'error': str(e)
                }
        
        # Testar Gemini
        from src.services.ai.gemini_service import gemini_service
        if gemini_service.is_available():
            results['gemini']['available'] = True
            try:
                gemini_result = gemini_service.test_connection()
                results['gemini']['test_result'] = gemini_result
            except Exception as e:
                results['gemini']['test_result'] = {
                    'success': False,
                    'error': str(e)
                }
        
        # Limpar conversas de teste
        chat_service.clear_conversation(f"{test_conversation_id}_openai")
        
        return jsonify({
            'success': True,
            'test_results': results
        }), 200
        
    except Exception as e:
        logger.error(f"Erro ao testar serviços: {str(e)}")
        return jsonify({
            'error': 'Erro interno do servidor'
        }), 500