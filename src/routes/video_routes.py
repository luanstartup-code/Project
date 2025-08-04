from flask import Blueprint, request, jsonify, send_file
from src.models.video import Video
from src.services.video_service import VideoService
from src.database.config import db
import os
import threading
import time

video_bp = Blueprint('videos', __name__)
video_service = VideoService()

@video_bp.route('/', methods=['GET'])
def get_videos():
    """Listar todos os vídeos"""
    try:
        videos = Video.query.all()
        return jsonify({
            'success': True,
            'data': [video.to_dict() for video in videos]
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@video_bp.route('/<int:video_id>', methods=['GET'])
def get_video(video_id):
    """Obter vídeo específico"""
    try:
        video = Video.query.get(video_id)
        if not video:
            return jsonify({
                'success': False,
                'error': 'Video not found'
            }), 404
        
        return jsonify({
            'success': True,
            'data': video.to_dict()
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@video_bp.route('/', methods=['POST'])
def create_video():
    """Criar novo vídeo"""
    try:
        data = request.get_json()
        
        # Validação
        if not data or 'title' not in data:
            return jsonify({
                'success': False,
                'error': 'Title is required'
            }), 400
        
        # Validação de tamanho
        if len(data['title']) > 255:
            return jsonify({
                'success': False,
                'error': 'Title too long (max 255 characters)'
            }), 400
        
        if 'description' in data and len(data['description']) > 1000:
            return jsonify({
                'success': False,
                'error': 'Description too long (max 1000 characters)'
            }), 400
        
        # Criar vídeo
        video = Video(
            title=data['title'],
            description=data.get('description', ''),
            status='pending'
        )
        
        db.session.add(video)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Video created successfully',
            'data': video.to_dict()
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@video_bp.route('/<int:video_id>/generate', methods=['POST'])
def generate_video(video_id):
    """Gerar vídeo"""
    try:
        video = Video.query.get(video_id)
        if not video:
            return jsonify({
                'success': False,
                'error': 'Video not found'
            }), 404
        
        # Atualizar status para processing
        video.status = 'processing'
        db.session.commit()
        
        # Iniciar geração do vídeo em background
        def generate_video_background():
            try:
                # Simular geração de vídeo
                time.sleep(5)  # Simular tempo de processamento
                
                # Gerar vídeo simples
                output_path = video_service.generate_simple_video(
                    video_id=video.id,
                    text=video.description or "Vídeo gerado com IA",
                    duration=10
                )
                
                # Atualizar status para completed
                with db.app.app_context():
                    video_record = Video.query.get(video_id)
                    if video_record:
                        video_record.status = 'completed'
                        video_record.file_path = output_path
                        video_record.duration = 10.0
                        db.session.commit()
                        
            except Exception as e:
                # Atualizar status para failed
                with db.app.app_context():
                    video_record = Video.query.get(video_id)
                    if video_record:
                        video_record.status = 'failed'
                        db.session.commit()
                print(f"Erro na geração do vídeo: {e}")
        
        # Executar em thread separada
        thread = threading.Thread(target=generate_video_background)
        thread.daemon = True
        thread.start()
        
        return jsonify({
            'success': True,
            'message': 'Video generation started',
            'data': video.to_dict()
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@video_bp.route('/<int:video_id>/status', methods=['GET'])
def get_video_status(video_id):
    """Obter status do vídeo"""
    try:
        video = Video.query.get(video_id)
        if not video:
            return jsonify({
                'success': False,
                'error': 'Video not found'
            }), 404
        
        return jsonify({
            'success': True,
            'data': video.to_dict()
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@video_bp.route('/<int:video_id>/download', methods=['GET'])
def download_video(video_id):
    """Download do vídeo"""
    try:
        video = Video.query.get(video_id)
        if not video:
            return jsonify({
                'success': False,
                'error': 'Video not found'
            }), 404
        
        if not video.file_path or not os.path.exists(video.file_path):
            return jsonify({
                'success': False,
                'error': 'Video file not found'
            }), 404
        
        return send_file(
            video.file_path,
            as_attachment=True,
            download_name=f'video_{video_id}.txt'
        )
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@video_bp.route('/<int:video_id>', methods=['DELETE'])
def delete_video(video_id):
    """Deletar vídeo"""
    try:
        video = Video.query.get(video_id)
        if not video:
            return jsonify({
                'success': False,
                'error': 'Video not found'
            }), 404
        
        # Remover arquivo se existir
        if video.file_path and os.path.exists(video.file_path):
            os.remove(video.file_path)
        
        db.session.delete(video)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Video deleted successfully'
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500