from flask import Blueprint, request, jsonify
from src.services.workflow.project_manager import project_manager
from src.services.video.avatar_processor import avatar_processor
from src.services.video.elevenlabs_service import elevenlabs_service
from src.models.scene import Project, Scene
from src.models.avatar import Avatar
from src.database.config import db

project_bp = Blueprint('project', __name__)

@project_bp.route('/', methods=['GET'])
def get_projects():
    """Listar todos os projetos"""
    try:
        result = project_manager.list_projects()
        
        if result['success']:
            return jsonify({
                'success': True,
                'data': result['projects']
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': result['error']
            }), 500
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@project_bp.route('/<int:project_id>', methods=['GET'])
def get_project(project_id):
    """Obter projeto específico"""
    try:
        result = project_manager.get_project(project_id)
        
        if result['success']:
            return jsonify({
                'success': True,
                'data': result['project']
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': result['error']
            }), 404
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@project_bp.route('/', methods=['POST'])
def create_project():
    """Criar novo projeto"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'error': 'Nenhum dado fornecido'
            }), 400
        
        title = data.get('title', '').strip()
        if not title:
            return jsonify({
                'success': False,
                'error': 'Título é obrigatório'
            }), 400
        
        description = data.get('description', '')
        template = data.get('template', 'default')
        
        result = project_manager.create_project(title, description, template)
        
        if result['success']:
            return jsonify({
                'success': True,
                'message': 'Projeto criado com sucesso',
                'data': result['project']
            }), 201
        else:
            return jsonify({
                'success': False,
                'error': result['error']
            }), 400
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@project_bp.route('/<int:project_id>', methods=['PUT'])
def update_project(project_id):
    """Atualizar projeto"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'error': 'Nenhum dado fornecido'
            }), 400
        
        result = project_manager.update_project(project_id, data)
        
        if result['success']:
            return jsonify({
                'success': True,
                'message': 'Projeto atualizado com sucesso',
                'data': result['project']
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': result['error']
            }), 404
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@project_bp.route('/<int:project_id>', methods=['DELETE'])
def delete_project(project_id):
    """Deletar projeto"""
    try:
        result = project_manager.delete_project(project_id)
        
        if result['success']:
            return jsonify({
                'success': True,
                'message': result['message']
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': result['error']
            }), 404
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@project_bp.route('/<int:project_id>/scenes', methods=['GET'])
def get_project_scenes(project_id):
    """Obter cenas de um projeto"""
    try:
        project = Project.query.get(project_id)
        if not project:
            return jsonify({
                'success': False,
                'error': 'Projeto não encontrado'
            }), 404
        
        scenes = Scene.query.filter_by(project_id=project_id).order_by(Scene.order).all()
        
        return jsonify({
            'success': True,
            'data': [scene.to_dict() for scene in scenes]
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@project_bp.route('/<int:project_id>/scenes', methods=['POST'])
def add_scene(project_id):
    """Adicionar cena ao projeto"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'error': 'Nenhum dado fornecido'
            }), 400
        
        result = project_manager.add_scene(project_id, data)
        
        if result['success']:
            return jsonify({
                'success': True,
                'message': 'Cena adicionada com sucesso',
                'data': result['scene']
            }), 201
        else:
            return jsonify({
                'success': False,
                'error': result['error']
            }), 400
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@project_bp.route('/scenes/<int:scene_id>', methods=['GET'])
def get_scene(scene_id):
    """Obter cena específica"""
    try:
        scene = Scene.query.get(scene_id)
        if not scene:
            return jsonify({
                'success': False,
                'error': 'Cena não encontrada'
            }), 404
        
        return jsonify({
            'success': True,
            'data': scene.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@project_bp.route('/scenes/<int:scene_id>', methods=['PUT'])
def update_scene(scene_id):
    """Atualizar cena"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'error': 'Nenhum dado fornecido'
            }), 400
        
        result = project_manager.update_scene(scene_id, data)
        
        if result['success']:
            return jsonify({
                'success': True,
                'message': 'Cena atualizada com sucesso',
                'data': result['scene']
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': result['error']
            }), 404
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@project_bp.route('/scenes/<int:scene_id>', methods=['DELETE'])
def delete_scene(scene_id):
    """Deletar cena"""
    try:
        result = project_manager.delete_scene(scene_id)
        
        if result['success']:
            return jsonify({
                'success': True,
                'message': result['message']
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': result['error']
            }), 404
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@project_bp.route('/<int:project_id>/scenes/reorder', methods=['PUT'])
def reorder_scenes(project_id):
    """Reordenar cenas"""
    try:
        data = request.get_json()
        
        if not data or 'scene_orders' not in data:
            return jsonify({
                'success': False,
                'error': 'Dados de reordenação não fornecidos'
            }), 400
        
        result = project_manager.reorder_scenes(project_id, data['scene_orders'])
        
        if result['success']:
            return jsonify({
                'success': True,
                'message': result['message']
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': result['error']
            }), 400
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@project_bp.route('/scenes/<int:scene_id>/generate', methods=['POST'])
def generate_scene(scene_id):
    """Gerar vídeo para uma cena"""
    try:
        result = project_manager.generate_scene(scene_id)
        
        if result['success']:
            return jsonify({
                'success': True,
                'message': 'Geração de cena iniciada',
                'data': result
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': result['error']
            }), 400
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@project_bp.route('/scenes/<int:scene_id>/status', methods=['GET'])
def get_scene_status(scene_id):
    """Obter status da geração da cena"""
    try:
        result = project_manager.get_scene_status(scene_id)
        
        if result['success']:
            return jsonify({
                'success': True,
                'data': result
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': result['error']
            }), 404
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@project_bp.route('/<int:project_id>/generate', methods=['POST'])
def generate_project_video(project_id):
    """Gerar vídeo final do projeto"""
    try:
        result = project_manager.generate_project_video(project_id)
        
        if result['success']:
            return jsonify({
                'success': True,
                'message': 'Geração do projeto iniciada',
                'data': result
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': result['error']
            }), 400
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@project_bp.route('/resources/avatars', methods=['GET'])
def get_available_avatars():
    """Obter avatares disponíveis"""
    try:
        result = avatar_processor.list_avatars()
        
        if result['success']:
            # Filtrar apenas avatares prontos
            ready_avatars = [avatar for avatar in result['avatars'] if avatar['status'] == 'completed']
            return jsonify({
                'success': True,
                'data': ready_avatars
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': result['error']
            }), 500
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@project_bp.route('/resources/voices', methods=['GET'])
def get_available_voices():
    """Obter vozes disponíveis"""
    try:
        result = elevenlabs_service.get_voices()
        
        if result['success']:
            return jsonify({
                'success': True,
                'data': result['voices']
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': result['error']
            }), 500
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@project_bp.route('/templates', methods=['GET'])
def get_templates():
    """Obter templates disponíveis"""
    try:
        templates = [
            {
                'id': 'default',
                'name': 'Template Padrão',
                'description': 'Template básico para vídeos',
                'scenes': 3,
                'duration': 15
            },
            {
                'id': 'presentation',
                'name': 'Apresentação',
                'description': 'Template para apresentações',
                'scenes': 5,
                'duration': 30
            },
            {
                'id': 'story',
                'name': 'História',
                'description': 'Template para contar histórias',
                'scenes': 7,
                'duration': 60
            },
            {
                'id': 'marketing',
                'name': 'Marketing',
                'description': 'Template para vídeos de marketing',
                'scenes': 4,
                'duration': 20
            }
        ]
        
        return jsonify({
            'success': True,
            'data': templates
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500