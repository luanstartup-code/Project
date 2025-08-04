import os
import requests
import json
from typing import Dict, Any, List, Optional
from src.utils.config_manager import config_manager
from src.services.storage.file_manager import file_manager
from src.models.avatar import Avatar, AvatarPhoto
from src.database.config import db

class AvatarProcessor:
    """Processador de avatares com integração HeyGen"""
    
    def __init__(self):
        self.heygen_api_key = config_manager.get_api_key('video', 'heygen')
        self.heygen_base_url = "https://api.heygen.com/v1"
        self.quality = config_manager.get('video.heygen.avatar_quality', 'high')
    
    def is_configured(self) -> bool:
        """Verificar se HeyGen está configurado"""
        return bool(self.heygen_api_key)
    
    def is_enabled(self) -> bool:
        """Verificar se HeyGen está habilitado"""
        return config_manager.is_service_enabled('video', 'heygen')
    
    def create_avatar_from_photos(self, photos: List, name: str, description: str = "") -> Dict[str, Any]:
        """Criar avatar a partir de fotos"""
        try:
            if not self.is_configured() or not self.is_enabled():
                return {
                    'success': False,
                    'error': 'HeyGen não está configurado ou habilitado'
                }
            
            # Criar avatar no banco
            avatar = Avatar(
                name=name,
                description=description,
                quality=self.quality,
                status='processing'
            )
            db.session.add(avatar)
            db.session.commit()
            
            # Salvar fotos
            photo_results = file_manager.save_avatar_photos(photos, str(avatar.id))
            
            if not photo_results['success']:
                avatar.status = 'failed'
                db.session.commit()
                return {
                    'success': False,
                    'error': 'Erro ao salvar fotos',
                    'details': photo_results['errors']
                }
            
            # Salvar referências das fotos no banco
            for photo_result in photo_results['files']:
                avatar_photo = AvatarPhoto(
                    avatar_id=avatar.id,
                    filename=photo_result['filename'],
                    file_path=photo_result['file_path'],
                    file_size=photo_result['size'],
                    mime_type=photo_result['mime_type'],
                    is_valid=True
                )
                db.session.add(avatar_photo)
            
            db.session.commit()
            
            # Processar com HeyGen em background
            self._process_with_heygen(avatar.id, photo_results['files'])
            
            return {
                'success': True,
                'avatar_id': avatar.id,
                'message': 'Avatar criado com sucesso. Processamento em andamento.'
            }
            
        except Exception as e:
            db.session.rollback()
            return {
                'success': False,
                'error': str(e)
            }
    
    def _process_with_heygen(self, avatar_id: int, photo_files: List[Dict[str, Any]]):
        """Processar avatar com HeyGen"""
        try:
            avatar = Avatar.query.get(avatar_id)
            if not avatar:
                return
            
            # Preparar dados para HeyGen
            photo_urls = []
            for photo_file in photo_files:
                # Em produção, você faria upload para um CDN
                # Por enquanto, usamos caminhos locais
                photo_urls.append(photo_file['file_path'])
            
            # Chamada para API HeyGen
            headers = {
                'X-Api-Key': self.heygen_api_key,
                'Content-Type': 'application/json'
            }
            
            payload = {
                'name': avatar.name,
                'description': avatar.description or '',
                'photo_urls': photo_urls,
                'quality': self.quality
            }
            
            response = requests.post(
                f"{self.heygen_base_url}/avatar/create",
                headers=headers,
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                avatar.heygen_id = data.get('avatar_id')
                avatar.status = 'completed'
            else:
                avatar.status = 'failed'
                print(f"Erro HeyGen: {response.text}")
            
            db.session.commit()
            
        except Exception as e:
            print(f"Erro ao processar avatar com HeyGen: {e}")
            avatar = Avatar.query.get(avatar_id)
            if avatar:
                avatar.status = 'failed'
                db.session.commit()
    
    def get_avatar_status(self, avatar_id: int) -> Dict[str, Any]:
        """Obter status do avatar"""
        try:
            avatar = Avatar.query.get(avatar_id)
            if not avatar:
                return {
                    'success': False,
                    'error': 'Avatar não encontrado'
                }
            
            return {
                'success': True,
                'avatar': avatar.to_dict(),
                'photos': [photo.to_dict() for photo in avatar.photos]
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def list_avatars(self) -> Dict[str, Any]:
        """Listar todos os avatares"""
        try:
            avatars = Avatar.query.order_by(Avatar.created_at.desc()).all()
            
            return {
                'success': True,
                'avatars': [avatar.to_dict() for avatar in avatars]
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def delete_avatar(self, avatar_id: int) -> Dict[str, Any]:
        """Deletar avatar"""
        try:
            avatar = Avatar.query.get(avatar_id)
            if not avatar:
                return {
                    'success': False,
                    'error': 'Avatar não encontrado'
                }
            
            # Deletar arquivos
            for photo in avatar.photos:
                file_manager.delete_file(photo.file_path)
            
            # Deletar do HeyGen se existir
            if avatar.heygen_id and self.is_configured():
                self._delete_from_heygen(avatar.heygen_id)
            
            # Deletar do banco
            db.session.delete(avatar)
            db.session.commit()
            
            return {
                'success': True,
                'message': 'Avatar deletado com sucesso'
            }
            
        except Exception as e:
            db.session.rollback()
            return {
                'success': False,
                'error': str(e)
            }
    
    def _delete_from_heygen(self, heygen_id: str):
        """Deletar avatar do HeyGen"""
        try:
            headers = {
                'X-Api-Key': self.heygen_api_key,
                'Content-Type': 'application/json'
            }
            
            response = requests.delete(
                f"{self.heygen_base_url}/avatar/{heygen_id}",
                headers=headers,
                timeout=10
            )
            
            if response.status_code != 200:
                print(f"Erro ao deletar avatar do HeyGen: {response.text}")
                
        except Exception as e:
            print(f"Erro ao deletar avatar do HeyGen: {e}")
    
    def update_avatar(self, avatar_id: int, updates: Dict[str, Any]) -> Dict[str, Any]:
        """Atualizar avatar"""
        try:
            avatar = Avatar.query.get(avatar_id)
            if not avatar:
                return {
                    'success': False,
                    'error': 'Avatar não encontrado'
                }
            
            # Atualizar campos permitidos
            if 'name' in updates:
                avatar.name = updates['name']
            if 'description' in updates:
                avatar.description = updates['description']
            if 'quality' in updates:
                avatar.quality = updates['quality']
            
            db.session.commit()
            
            return {
                'success': True,
                'avatar': avatar.to_dict()
            }
            
        except Exception as e:
            db.session.rollback()
            return {
                'success': False,
                'error': str(e)
            }
    
    def test_connection(self) -> Dict[str, Any]:
        """Testar conexão com HeyGen"""
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
            
            headers = {
                'X-Api-Key': self.heygen_api_key,
                'Content-Type': 'application/json'
            }
            
            response = requests.get(
                f"{self.heygen_base_url}/avatar/list",
                headers=headers,
                timeout=10
            )
            
            response_time = time.time() - start_time
            
            if response.status_code == 200:
                return {
                    'connected': True,
                    'message': 'Conexão com HeyGen estabelecida com sucesso',
                    'response_time': round(response_time, 2)
                }
            else:
                return {
                    'connected': False,
                    'message': f'Erro da API: {response.status_code}',
                    'response_time': round(response_time, 2)
                }
                
        except Exception as e:
            return {
                'connected': False,
                'message': str(e),
                'response_time': 0
            }

# Instância global
avatar_processor = AvatarProcessor()