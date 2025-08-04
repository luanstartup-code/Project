import os
import time
from src.database.config import db
from src.models.video import Video

class VideoService:
    def __init__(self):
        self.output_dir = 'src/static/assets/videos'
        self.ensure_output_dir()
    
    def ensure_output_dir(self):
        """Garantir que o diretório de saída existe"""
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir, exist_ok=True)
    
    def generate_simple_video(self, video_id, text="Hello World", duration=5):
        """Gerar vídeo simples com texto (simulado)"""
        try:
            # Simular geração de vídeo criando um arquivo de texto
            output_path = os.path.join(self.output_dir, f'video_{video_id}.txt')
            
            # Criar arquivo de simulação
            with open(output_path, 'w') as f:
                f.write(f"Video ID: {video_id}\n")
                f.write(f"Text: {text}\n")
                f.write(f"Duration: {duration} seconds\n")
                f.write(f"Generated at: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write("Status: Generated successfully\n")
            
            # Simular tempo de processamento
            time.sleep(2)
            
            return output_path
            
        except Exception as e:
            print(f"Erro na geração do vídeo: {e}")
            raise e
    
    def get_video_info(self, video_path):
        """Obter informações do vídeo"""
        try:
            if os.path.exists(video_path):
                file_size = os.path.getsize(video_path)
                modified_time = os.path.getmtime(video_path)
                
                return {
                    'path': video_path,
                    'size': file_size,
                    'modified': modified_time,
                    'exists': True
                }
            else:
                return {
                    'path': video_path,
                    'exists': False
                }
        except Exception as e:
            print(f"Erro ao obter informações do vídeo: {e}")
            return {
                'path': video_path,
                'error': str(e)
            }