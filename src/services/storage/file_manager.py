import os
import uuid
import shutil
from typing import List, Dict, Any, Optional
from werkzeug.utils import secure_filename
from PIL import Image
import cv2
from src.utils.config_manager import config_manager
import math

class FileManager:
    """Gerenciador de arquivos e uploads"""
    
    def __init__(self):
        self.base_path = config_manager.get('storage.local_path', 'src/static/assets')
        self.max_file_size = config_manager.get('storage.max_file_size', 100 * 1024 * 1024)
        self.allowed_extensions = config_manager.get('storage.allowed_extensions', ['jpg', 'jpeg', 'png', 'mp4', 'mov', 'avi'])
        
        # Criar diretórios necessários
        self.ensure_directories()
    
    def ensure_directories(self):
        """Garantir que os diretórios existem"""
        directories = [
            self.base_path,
            f"{self.base_path}/avatars",
            f"{self.base_path}/videos",
            f"{self.base_path}/scenes",
            f"{self.base_path}/uploads",
            f"{self.base_path}/temp"
        ]
        
        for directory in directories:
            os.makedirs(directory, exist_ok=True)
    
    def validate_file(self, file) -> Dict[str, Any]:
        """Validar arquivo"""
        errors = []
        warnings = []
        
        # Verificar tamanho
        if file.content_length and file.content_length > self.max_file_size:
            errors.append(f"Arquivo muito grande: {self.format_size(file.content_length)} (máximo: {self.format_size(self.max_file_size)})")
        
        # Verificar extensão
        filename = secure_filename(file.filename)
        extension = filename.rsplit('.', 1)[1].lower() if '.' in filename else ''
        
        if extension not in self.allowed_extensions:
            errors.append(f"Tipo de arquivo não suportado: {extension}")
        
        # Verificar se é imagem
        if extension in ['jpg', 'jpeg', 'png']:
            try:
                with Image.open(file) as img:
                    # Verificar dimensões mínimas
                    if img.width < 100 or img.height < 100:
                        warnings.append("Imagem muito pequena (mínimo 100x100px)")
                    
                    # Verificar dimensões máximas
                    if img.width > 4096 or img.height > 4096:
                        warnings.append("Imagem muito grande (máximo 4096x4096px)")
                    
                    # Verificar formato
                    if img.format not in ['JPEG', 'PNG']:
                        warnings.append(f"Formato de imagem não otimizado: {img.format}")
            except Exception as e:
                errors.append(f"Erro ao processar imagem: {str(e)}")
        
        return {
            'valid': len(errors) == 0,
            'errors': errors,
            'warnings': warnings,
            'extension': extension,
            'filename': filename
        }
    
    def save_file(self, file, category: str = 'uploads', custom_name: str = None) -> Dict[str, Any]:
        """Salvar arquivo"""
        try:
            # Validar arquivo
            validation = self.validate_file(file)
            if not validation['valid']:
                return {
                    'success': False,
                    'errors': validation['errors']
                }
            
            # Gerar nome único
            if custom_name:
                filename = secure_filename(custom_name)
            else:
                unique_id = str(uuid.uuid4())
                filename = f"{unique_id}.{validation['extension']}"
            
            # Criar diretório da categoria
            category_path = f"{self.base_path}/{category}"
            os.makedirs(category_path, exist_ok=True)
            
            # Caminho completo do arquivo
            file_path = f"{category_path}/{filename}"
            
            # Salvar arquivo
            file.save(file_path)
            
            # Obter informações do arquivo
            file_info = self.get_file_info(file_path)
            
            return {
                'success': True,
                'file_path': file_path,
                'filename': filename,
                'url': f"/static/assets/{category}/{filename}",
                'size': file_info['size'],
                'mime_type': file_info['mime_type'],
                'warnings': validation['warnings']
            }
            
        except Exception as e:
            return {
                'success': False,
                'errors': [str(e)]
            }
    
    def save_avatar_photos(self, files: List, avatar_id: str) -> Dict[str, Any]:
        """Salvar fotos para avatar"""
        try:
            saved_files = []
            errors = []
            
            for file in files:
                # Validar arquivo
                validation = self.validate_file(file)
                if not validation['valid']:
                    errors.extend(validation['errors'])
                    continue
                
                # Verificar se é imagem
                if validation['extension'] not in ['jpg', 'jpeg', 'png']:
                    errors.append(f"Arquivo deve ser uma imagem: {file.filename}")
                    continue
                
                # Salvar arquivo
                result = self.save_file(file, 'avatars', f"avatar_{avatar_id}_{len(saved_files)}")
                
                if result['success']:
                    saved_files.append(result)
                else:
                    errors.extend(result['errors'])
            
            return {
                'success': len(errors) == 0,
                'files': saved_files,
                'errors': errors
            }
            
        except Exception as e:
            return {
                'success': False,
                'errors': [str(e)]
            }
    
    def process_image(self, file_path: str, operations: Dict[str, Any] = None) -> Dict[str, Any]:
        """Processar imagem (redimensionar, comprimir, etc.)"""
        try:
            if not operations:
                operations = {
                    'resize': {'width': 1024, 'height': 1024},
                    'quality': 85,
                    'format': 'JPEG'
                }
            
            with Image.open(file_path) as img:
                # Converter para RGB se necessário
                if img.mode in ('RGBA', 'LA', 'P'):
                    img = img.convert('RGB')
                
                # Redimensionar se especificado
                if 'resize' in operations:
                    resize_op = operations['resize']
                    if 'width' in resize_op and 'height' in resize_op:
                        img = img.resize((resize_op['width'], resize_op['height']), Image.Resampling.LANCZOS)
                    elif 'width' in resize_op:
                        ratio = resize_op['width'] / img.width
                        img = img.resize((resize_op['width'], int(img.height * ratio)), Image.Resampling.LANCZOS)
                    elif 'height' in resize_op:
                        ratio = resize_op['height'] / img.height
                        img = img.resize((int(img.width * ratio), resize_op['height']), Image.Resampling.LANCZOS)
                
                # Salvar com qualidade otimizada
                quality = operations.get('quality', 85)
                format = operations.get('format', 'JPEG')
                
                # Gerar novo nome
                base_name = os.path.splitext(file_path)[0]
                new_path = f"{base_name}_processed.{format.lower()}"
                
                img.save(new_path, format=format, quality=quality, optimize=True)
                
                return {
                    'success': True,
                    'original_path': file_path,
                    'processed_path': new_path,
                    'size_reduction': self.get_size_reduction(file_path, new_path)
                }
                
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def get_file_info(self, file_path: str) -> Dict[str, Any]:
        """Obter informações do arquivo"""
        try:
            if not os.path.exists(file_path):
                return {'exists': False}
            
            stat = os.stat(file_path)
            
            info = {
                'exists': True,
                'size': stat.st_size,
                'modified': stat.st_mtime,
                'created': stat.st_ctime
            }
            
            # Detectar tipo MIME
            import mimetypes
            mime_type, _ = mimetypes.guess_type(file_path)
            info['mime_type'] = mime_type or 'application/octet-stream'
            
            # Informações específicas para imagens
            if mime_type and mime_type.startswith('image/'):
                try:
                    with Image.open(file_path) as img:
                        info['dimensions'] = {
                            'width': img.width,
                            'height': img.height
                        }
                        info['format'] = img.format
                        info['mode'] = img.mode
                except Exception:
                    pass
            
            return info
            
        except Exception as e:
            return {
                'exists': False,
                'error': str(e)
            }
    
    def delete_file(self, file_path: str) -> bool:
        """Deletar arquivo"""
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
                return True
            return False
        except Exception:
            return False
    
    def cleanup_temp_files(self, max_age_hours: int = 24) -> int:
        """Limpar arquivos temporários antigos"""
        try:
            import time
            temp_dir = f"{self.base_path}/temp"
            current_time = time.time()
            max_age = max_age_hours * 3600
            deleted_count = 0
            
            for filename in os.listdir(temp_dir):
                file_path = os.path.join(temp_dir, filename)
                if os.path.isfile(file_path):
                    file_age = current_time - os.path.getmtime(file_path)
                    if file_age > max_age:
                        os.remove(file_path)
                        deleted_count += 1
            
            return deleted_count
            
        except Exception:
            return 0
    
    def format_size(self, bytes: int) -> str:
        """Formatar tamanho de arquivo"""
        if bytes == 0:
            return "0 Bytes"
        
        k = 1024
        sizes = ['Bytes', 'KB', 'MB', 'GB']
        i = int(math.floor(math.log(bytes) / math.log(k)))
        
        return f"{bytes / math.pow(k, i):.1f} {sizes[i]}"
    
    def get_size_reduction(self, original_path: str, processed_path: str) -> Dict[str, Any]:
        """Calcular redução de tamanho"""
        try:
            original_size = os.path.getsize(original_path)
            processed_size = os.path.getsize(processed_path)
            
            reduction = original_size - processed_size
            reduction_percent = (reduction / original_size) * 100
            
            return {
                'original_size': original_size,
                'processed_size': processed_size,
                'reduction_bytes': reduction,
                'reduction_percent': reduction_percent
            }
        except Exception:
            return {}

# Instância global
file_manager = FileManager()