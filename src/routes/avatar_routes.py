from flask import Blueprint, request, jsonify
from src.services.video.avatar_processor import avatar_processor
from src.services.storage.file_manager import file_manager
from src.models.avatar import Avatar, AvatarPhoto
from src.database.config import db

avatar_bp = Blueprint('avatar', __name__)

@avatar_bp.route('/', methods=['GET'])
def get_avatars():
    """Listar todos os avatares"""
    try:
        result = avatar_processor.list_avatars()
        
        if result['success']:
            return jsonify({
                'success': True,
                'data': result['avatars']
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

@avatar_bp.route('/<int:avatar_id>', methods=['GET'])
def get_avatar(avatar_id):
    """Obter avatar específico"""
    try:
        result = avatar_processor.get_avatar_status(avatar_id)
        
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

@avatar_bp.route('/', methods=['POST'])
def create_avatar():
    """Criar novo avatar"""
    try:
        # Verificar se há arquivos
        if 'photos' not in request.files:
            return jsonify({
                'success': False,
                'error': 'Nenhuma foto fornecida'
            }), 400
        
        photos = request.files.getlist('photos')
        if not photos or all(photo.filename == '' for photo in photos):
            return jsonify({
                'success': False,
                'error': 'Nenhuma foto selecionada'
            }), 400
        
        # Obter dados do formulário
        name = request.form.get('name', 'Novo Avatar')
        description = request.form.get('description', '')
        
        # Validar nome
        if not name or len(name.strip()) == 0:
            return jsonify({
                'success': False,
                'error': 'Nome é obrigatório'
            }), 400
        
        # Criar avatar
        result = avatar_processor.create_avatar_from_photos(photos, name, description)
        
        if result['success']:
            return jsonify({
                'success': True,
                'message': result['message'],
                'data': {
                    'avatar_id': result['avatar_id']
                }
            }), 201
        else:
            return jsonify({
                'success': False,
                'error': result['error'],
                'details': result.get('details', [])
            }), 400
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@avatar_bp.route('/<int:avatar_id>', methods=['PUT'])
def update_avatar(avatar_id):
    """Atualizar avatar"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'error': 'Nenhum dado fornecido'
            }), 400
        
        # Validar campos permitidos
        allowed_fields = ['name', 'description', 'quality']
        updates = {k: v for k, v in data.items() if k in allowed_fields}
        
        if not updates:
            return jsonify({
                'success': False,
                'error': 'Nenhum campo válido para atualização'
            }), 400
        
        result = avatar_processor.update_avatar(avatar_id, updates)
        
        if result['success']:
            return jsonify({
                'success': True,
                'message': 'Avatar atualizado com sucesso',
                'data': result['avatar']
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

@avatar_bp.route('/<int:avatar_id>', methods=['DELETE'])
def delete_avatar(avatar_id):
    """Deletar avatar"""
    try:
        result = avatar_processor.delete_avatar(avatar_id)
        
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

@avatar_bp.route('/<int:avatar_id>/status', methods=['GET'])
def get_avatar_status(avatar_id):
    """Obter status do processamento do avatar"""
    try:
        avatar = Avatar.query.get(avatar_id)
        if not avatar:
            return jsonify({
                'success': False,
                'error': 'Avatar não encontrado'
            }), 404
        
        return jsonify({
            'success': True,
            'data': {
                'id': avatar.id,
                'name': avatar.name,
                'status': avatar.status,
                'heygen_id': avatar.heygen_id,
                'quality': avatar.quality,
                'created_at': avatar.created_at.isoformat() if avatar.created_at else None,
                'updated_at': avatar.updated_at.isoformat() if avatar.updated_at else None
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@avatar_bp.route('/upload', methods=['POST'])
def upload_photo():
    """Upload de foto individual"""
    try:
        if 'photo' not in request.files:
            return jsonify({
                'success': False,
                'error': 'Nenhuma foto fornecida'
            }), 400
        
        photo = request.files['photo']
        if photo.filename == '':
            return jsonify({
                'success': False,
                'error': 'Nenhuma foto selecionada'
            }), 400
        
        # Salvar arquivo
        result = file_manager.save_file(photo, 'avatars')
        
        if result['success']:
            return jsonify({
                'success': True,
                'message': 'Foto enviada com sucesso',
                'data': {
                    'filename': result['filename'],
                    'url': result['url'],
                    'size': result['size'],
                    'mime_type': result['mime_type']
                }
            }), 201
        else:
            return jsonify({
                'success': False,
                'error': 'Erro ao salvar foto',
                'details': result['errors']
            }), 400
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@avatar_bp.route('/validate', methods=['POST'])
def validate_photos():
    """Validar fotos antes do upload"""
    try:
        if 'photos' not in request.files:
            return jsonify({
                'success': False,
                'error': 'Nenhuma foto fornecida'
            }), 400
        
        photos = request.files.getlist('photos')
        if not photos:
            return jsonify({
                'success': False,
                'error': 'Nenhuma foto selecionada'
            }), 400
        
        validation_results = []
        all_valid = True
        
        for photo in photos:
            if photo.filename == '':
                continue
                
            validation = file_manager.validate_file(photo)
            validation_results.append({
                'filename': photo.filename,
                'valid': validation['valid'],
                'errors': validation['errors'],
                'warnings': validation['warnings']
            })
            
            if not validation['valid']:
                all_valid = False
        
        return jsonify({
            'success': True,
            'data': {
                'all_valid': all_valid,
                'results': validation_results
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@avatar_bp.route('/test', methods=['POST'])
def test_avatar_service():
    """Testar serviço de avatar"""
    try:
        result = avatar_processor.test_connection()
        
        return jsonify({
            'success': True,
            'data': result
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500