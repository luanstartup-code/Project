import os
import uuid
import json
from typing import Dict, Any, List, Optional
from datetime import datetime
from src.models.scene import Project, Scene
from src.models.avatar import Avatar
from src.database.config import db
from src.services.video.runway_service import runway_service
from src.services.video.elevenlabs_service import elevenlabs_service
from src.services.storage.file_manager import file_manager

class ProjectManager:
    """Gerenciador de projetos de vídeo"""
    
    def __init__(self):
        self.output_dir = 'src/static/assets/videos'
        os.makedirs(self.output_dir, exist_ok=True)
    
    def create_project(self, title: str, description: str = "", template: str = "default") -> Dict[str, Any]:
        """Criar novo projeto"""
        try:
            project = Project(
                title=title,
                description=description,
                template=template,
                status='draft'
            )
            
            db.session.add(project)
            db.session.commit()
            
            return {
                'success': True,
                'project': project.to_dict()
            }
            
        except Exception as e:
            db.session.rollback()
            return {
                'success': False,
                'error': str(e)
            }
    
    def get_project(self, project_id: int) -> Dict[str, Any]:
        """Obter projeto específico"""
        try:
            project = Project.query.get(project_id)
            if not project:
                return {
                    'success': False,
                    'error': 'Projeto não encontrado'
                }
            
            return {
                'success': True,
                'project': project.to_dict()
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def list_projects(self) -> Dict[str, Any]:
        """Listar todos os projetos"""
        try:
            projects = Project.query.order_by(Project.created_at.desc()).all()
            
            return {
                'success': True,
                'projects': [project.to_dict() for project in projects]
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def update_project(self, project_id: int, updates: Dict[str, Any]) -> Dict[str, Any]:
        """Atualizar projeto"""
        try:
            project = Project.query.get(project_id)
            if not project:
                return {
                    'success': False,
                    'error': 'Projeto não encontrado'
                }
            
            # Atualizar campos permitidos
            allowed_fields = ['title', 'description', 'template', 'resolution', 'fps', 'format']
            for field in allowed_fields:
                if field in updates:
                    setattr(project, field, updates[field])
            
            db.session.commit()
            
            return {
                'success': True,
                'project': project.to_dict()
            }
            
        except Exception as e:
            db.session.rollback()
            return {
                'success': False,
                'error': str(e)
            }
    
    def delete_project(self, project_id: int) -> Dict[str, Any]:
        """Deletar projeto"""
        try:
            project = Project.query.get(project_id)
            if not project:
                return {
                    'success': False,
                    'error': 'Projeto não encontrado'
                }
            
            # Deletar arquivos de vídeo
            if project.final_video_path and os.path.exists(project.final_video_path):
                os.remove(project.final_video_path)
            
            # Deletar cenas e seus arquivos
            for scene in project.scenes:
                if scene.file_path and os.path.exists(scene.file_path):
                    os.remove(scene.file_path)
            
            # Deletar do banco
            db.session.delete(project)
            db.session.commit()
            
            return {
                'success': True,
                'message': 'Projeto deletado com sucesso'
            }
            
        except Exception as e:
            db.session.rollback()
            return {
                'success': False,
                'error': str(e)
            }
    
    def add_scene(self, project_id: int, scene_data: Dict[str, Any]) -> Dict[str, Any]:
        """Adicionar cena ao projeto"""
        try:
            project = Project.query.get(project_id)
            if not project:
                return {
                    'success': False,
                    'error': 'Projeto não encontrado'
                }
            
            # Determinar ordem da cena
            max_order = max([scene.order for scene in project.scenes]) if project.scenes else -1
            new_order = max_order + 1
            
            scene = Scene(
                project_id=project_id,
                title=scene_data.get('title', f'Cena {new_order + 1}'),
                description=scene_data.get('description', ''),
                order=new_order,
                duration=scene_data.get('duration', 5.0),
                background=scene_data.get('background', ''),
                transition=scene_data.get('transition', 'fade'),
                avatar_id=scene_data.get('avatar_id'),
                voice_id=scene_data.get('voice_id'),
                voice_settings=json.dumps(scene_data.get('voice_settings', {})),
                script=scene_data.get('script', ''),
                subtitle=scene_data.get('subtitle', ''),
                ai_prompt=scene_data.get('ai_prompt', ''),
                ai_model=scene_data.get('ai_model', 'gen-3'),
                status='pending'
            )
            
            db.session.add(scene)
            
            # Atualizar contagem de cenas
            project.scene_count = len(project.scenes) + 1
            project.total_duration += scene.duration
            
            db.session.commit()
            
            return {
                'success': True,
                'scene': scene.to_dict()
            }
            
        except Exception as e:
            db.session.rollback()
            return {
                'success': False,
                'error': str(e)
            }
    
    def update_scene(self, scene_id: int, updates: Dict[str, Any]) -> Dict[str, Any]:
        """Atualizar cena"""
        try:
            scene = Scene.query.get(scene_id)
            if not scene:
                return {
                    'success': False,
                    'error': 'Cena não encontrada'
                }
            
            # Atualizar campos permitidos
            allowed_fields = [
                'title', 'description', 'duration', 'background', 'transition',
                'avatar_id', 'voice_id', 'script', 'subtitle', 'ai_prompt', 'ai_model'
            ]
            
            for field in allowed_fields:
                if field in updates:
                    if field == 'voice_settings':
                        setattr(scene, field, json.dumps(updates[field]))
                    else:
                        setattr(scene, field, updates[field])
            
            # Atualizar duração total do projeto
            project = scene.project
            old_duration = scene.duration
            new_duration = updates.get('duration', old_duration)
            project.total_duration = project.total_duration - old_duration + new_duration
            
            db.session.commit()
            
            return {
                'success': True,
                'scene': scene.to_dict()
            }
            
        except Exception as e:
            db.session.rollback()
            return {
                'success': False,
                'error': str(e)
            }
    
    def delete_scene(self, scene_id: int) -> Dict[str, Any]:
        """Deletar cena"""
        try:
            scene = Scene.query.get(scene_id)
            if not scene:
                return {
                    'success': False,
                    'error': 'Cena não encontrada'
                }
            
            project = scene.project
            
            # Deletar arquivo de vídeo da cena
            if scene.file_path and os.path.exists(scene.file_path):
                os.remove(scene.file_path)
            
            # Atualizar duração total
            project.total_duration -= scene.duration
            project.scene_count -= 1
            
            # Reordenar cenas restantes
            remaining_scenes = Scene.query.filter(
                Scene.project_id == project.id,
                Scene.order > scene.order
            ).all()
            
            for remaining_scene in remaining_scenes:
                remaining_scene.order -= 1
            
            # Deletar cena
            db.session.delete(scene)
            db.session.commit()
            
            return {
                'success': True,
                'message': 'Cena deletada com sucesso'
            }
            
        except Exception as e:
            db.session.rollback()
            return {
                'success': False,
                'error': str(e)
            }
    
    def reorder_scenes(self, project_id: int, scene_orders: List[Dict[str, int]]) -> Dict[str, Any]:
        """Reordenar cenas"""
        try:
            project = Project.query.get(project_id)
            if not project:
                return {
                    'success': False,
                    'error': 'Projeto não encontrado'
                }
            
            # Atualizar ordem das cenas
            for order_data in scene_orders:
                scene_id = order_data.get('scene_id')
                new_order = order_data.get('order')
                
                if scene_id and new_order is not None:
                    scene = Scene.query.get(scene_id)
                    if scene and scene.project_id == project_id:
                        scene.order = new_order
            
            db.session.commit()
            
            return {
                'success': True,
                'message': 'Cenas reordenadas com sucesso'
            }
            
        except Exception as e:
            db.session.rollback()
            return {
                'success': False,
                'error': str(e)
            }
    
    def generate_scene(self, scene_id: int) -> Dict[str, Any]:
        """Gerar vídeo para uma cena"""
        try:
            scene = Scene.query.get(scene_id)
            if not scene:
                return {
                    'success': False,
                    'error': 'Cena não encontrada'
                }
            
            # Atualizar status
            scene.status = 'processing'
            db.session.commit()
            
            # Gerar vídeo com Runway ML
            if runway_service.is_configured() and runway_service.is_enabled():
                result = runway_service.generate_video(
                    prompt=scene.ai_prompt or scene.script,
                    duration=int(scene.duration),
                    resolution=scene.project.resolution
                )
                
                if result['success']:
                    # Salvar ID da geração
                    scene.file_path = result['generation_id']  # Temporário
                    db.session.commit()
                    
                    return {
                        'success': True,
                        'generation_id': result['generation_id'],
                        'estimated_time': result['estimated_time']
                    }
                else:
                    scene.status = 'failed'
                    db.session.commit()
                    return result
            
            # Fallback: simular geração
            import time
            time.sleep(2)  # Simular processamento
            
            # Gerar arquivo simulado
            output_path = f"{self.output_dir}/scene_{scene_id}_{uuid.uuid4()}.mp4"
            with open(output_path, 'w') as f:
                f.write(f"Scene {scene_id} - {scene.title}")
            
            scene.file_path = output_path
            scene.status = 'completed'
            db.session.commit()
            
            return {
                'success': True,
                'file_path': output_path
            }
            
        except Exception as e:
            scene.status = 'failed'
            db.session.commit()
            return {
                'success': False,
                'error': str(e)
            }
    
    def get_scene_status(self, scene_id: int) -> Dict[str, Any]:
        """Obter status da geração da cena"""
        try:
            scene = Scene.query.get(scene_id)
            if not scene:
                return {
                    'success': False,
                    'error': 'Cena não encontrada'
                }
            
            # Se tem generation_id, verificar com Runway
            if scene.file_path and scene.file_path.startswith('gen_'):
                if runway_service.is_configured():
                    result = runway_service.get_generation_status(scene.file_path)
                    if result['success']:
                        if result['status'] == 'completed':
                            # Download do vídeo
                            download_result = runway_service.download_video(
                                result['video_url'],
                                f"{self.output_dir}/scene_{scene_id}.mp4"
                            )
                            if download_result['success']:
                                scene.file_path = download_result['local_path']
                                scene.status = 'completed'
                                db.session.commit()
                        
                        return {
                            'success': True,
                            'status': result['status'],
                            'progress': result.get('progress', 0),
                            'video_url': result.get('video_url')
                        }
            
            return {
                'success': True,
                'status': scene.status,
                'file_path': scene.file_path
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def generate_project_video(self, project_id: int) -> Dict[str, Any]:
        """Gerar vídeo final do projeto"""
        try:
            project = Project.query.get(project_id)
            if not project:
                return {
                    'success': False,
                    'error': 'Projeto não encontrado'
                }
            
            # Verificar se todas as cenas estão prontas
            pending_scenes = [s for s in project.scenes if s.status != 'completed']
            if pending_scenes:
                return {
                    'success': False,
                    'error': f'{len(pending_scenes)} cenas ainda não foram geradas'
                }
            
            # Atualizar status
            project.status = 'processing'
            db.session.commit()
            
            # Combinar vídeos das cenas
            output_path = f"{self.output_dir}/project_{project_id}_{uuid.uuid4()}.mp4"
            
            # Simular combinação de vídeos
            import time
            time.sleep(3)
            
            with open(output_path, 'w') as f:
                f.write(f"Project {project_id} - {project.title}")
            
            project.final_video_path = output_path
            project.status = 'completed'
            db.session.commit()
            
            return {
                'success': True,
                'file_path': output_path
            }
            
        except Exception as e:
            project.status = 'failed'
            db.session.commit()
            return {
                'success': False,
                'error': str(e)
            }

# Instância global
project_manager = ProjectManager()