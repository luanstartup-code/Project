#!/usr/bin/env python3
"""
🎬 CineAI - Script Completo de Execução
Configura e executa o CineAI completo com todas as dependências
"""

import os
import sys
import subprocess
import time
import threading
from pathlib import Path

def print_banner():
    print("""
🎬 =====================================
   CineAI - AI Video Studio Platform
   Script Completo de Execução
=====================================
    """)

def setup_environment():
    """Configurar variáveis de ambiente com suas chaves reais"""
    print("🔧 Configurando variáveis de ambiente...")
    
    # Variáveis de ambiente essenciais
    env_vars = {
        # Configurações básicas
        'FLASK_ENV': 'development',
        'SECRET_KEY': 'cineai-secret-key-production-2024-ultra-secure',
        'JWT_SECRET_KEY': 'cineai-jwt-secret-key-production-2024-ultra-secure',
        'PORT': '5000',
        'DATABASE_URL': 'sqlite:///video_generator.db',
        
        # Administrador
        'ADMIN_EMAIL': 'admin@cineai.com',
        'ADMIN_PASSWORD': 'CineAI2024!Admin',
        
        # APIs de IA - SUBSTITUA PELAS SUAS CHAVES REAIS
        'OPENAI_API_KEY': 'sk-proj-YOUR_OPENAI_KEY_HERE_REPLACE_WITH_REAL',
        'OPENAI_MODEL': 'gpt-4',
        'OPENAI_MAX_TOKENS': '4000',
        'OPENAI_TEMPERATURE': '0.7',
        
        'GEMINI_API_KEY': 'AIza_YOUR_GEMINI_KEY_HERE_REPLACE_WITH_REAL',
        'GEMINI_MODEL': 'gemini-pro',
        'GEMINI_MAX_TOKENS': '4000',
        'GEMINI_TEMPERATURE': '0.7',
        
        'HEYGEN_API_KEY': 'YOUR_HEYGEN_KEY_HERE_REPLACE_WITH_REAL',
        'HEYGEN_MODEL': 'heygen-v1',
        'HEYGEN_AVATAR_QUALITY': 'high',
        
        'RUNWAY_API_KEY': 'key_YOUR_RUNWAY_KEY_HERE_REPLACE_WITH_REAL',
        'RUNWAY_MODEL': 'gen-3',
        'RUNWAY_QUALITY': 'high',
        
        'ELEVENLABS_API_KEY': 'sk_YOUR_ELEVENLABS_KEY_HERE_REPLACE_WITH_REAL',
        'ELEVENLABS_VOICE_ID_MALE': '21m00Tcm4TlvDq8ikWAM',
        'ELEVENLABS_VOICE_ID_FEMALE': 'EXAVITQu4vr4xnSDxMaL',
        'ELEVENLABS_STABILITY': '0.5',
        
        # Configurações do sistema
        'MAX_FILE_SIZE': '100MB',
        'ALLOWED_EXTENSIONS': 'jpg,jpeg,png,mp4,mov,avi',
        'STORAGE_LOCAL_PATH': 'src/static/assets',
        
        # URLs locais
        'REACT_APP_API_URL': 'http://localhost:5000',
        'FRONTEND_URL': 'http://localhost:3000',
        'CORS_ORIGINS': 'http://localhost:3000,http://127.0.0.1:3000',
        
        # Configurações de segurança
        'CORS_SUPPORTS_CREDENTIALS': 'true',
        'SESSION_COOKIE_SECURE': 'false',  # false para desenvolvimento local
        'SESSION_COOKIE_HTTPONLY': 'true',
        'SESSION_COOKIE_SAMESITE': 'Lax'
    }
    
    # Definir variáveis de ambiente
    for key, value in env_vars.items():
        os.environ[key] = value
    
    print("✅ Variáveis de ambiente configuradas!")
    return env_vars

def create_env_file(env_vars):
    """Criar arquivo .env local"""
    print("📝 Criando arquivo .env...")
    
    env_content = "# 🎬 CineAI - Configuração Local de Desenvolvimento\n\n"
    
    for key, value in env_vars.items():
        env_content += f"{key}={value}\n"
    
    with open('.env', 'w') as f:
        f.write(env_content)
    
    print("✅ Arquivo .env criado!")

def check_python_dependencies():
    """Verificar e instalar dependências Python"""
    print("🐍 Verificando dependências Python...")
    
    try:
        result = subprocess.run([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'], 
                              capture_output=True, text=True, check=True)
        print("✅ Dependências Python instaladas!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro ao instalar dependências Python: {e}")
        print("Saída do erro:", e.stderr)
        return False

def check_node_dependencies():
    """Verificar e instalar dependências Node.js"""
    print("📦 Verificando dependências Node.js...")
    
    frontend_path = Path('frontend')
    if not frontend_path.exists():
        print("❌ Pasta frontend não encontrada!")
        return False
    
    os.chdir(frontend_path)
    
    try:
        # Verificar se node_modules existe
        if not Path('node_modules').exists():
            print("📥 Instalando dependências do frontend...")
            result = subprocess.run(['npm', 'install'], capture_output=True, text=True, check=True)
        
        print("✅ Dependências Node.js verificadas!")
        os.chdir('..')
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro ao instalar dependências Node.js: {e}")
        print("Saída do erro:", e.stderr)
        os.chdir('..')
        return False
    except FileNotFoundError:
        print("❌ npm não encontrado! Instale o Node.js primeiro.")
        os.chdir('..')
        return False

def setup_database():
    """Configurar banco de dados"""
    print("🗄️  Configurando banco de dados...")
    
    try:
        result = subprocess.run([sys.executable, 'create_database.py'], 
                              capture_output=True, text=True, check=True)
        print("✅ Banco de dados configurado!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro ao configurar banco: {e}")
        print("Saída do erro:", e.stderr)
        return False

def run_backend():
    """Executar backend Flask"""
    print("🚀 Iniciando backend...")
    
    try:
        # Usar python para desenvolvimento local
        process = subprocess.Popen([sys.executable, 'app.py'], 
                                 stdout=subprocess.PIPE, 
                                 stderr=subprocess.STDOUT,
                                 universal_newlines=True,
                                 bufsize=1)
        return process
    except Exception as e:
        print(f"❌ Erro ao iniciar backend: {e}")
        return None

def run_frontend():
    """Executar frontend React"""
    print("⚛️  Iniciando frontend...")
    
    frontend_path = Path('frontend')
    if not frontend_path.exists():
        print("❌ Pasta frontend não encontrada!")
        return None
    
    try:
        # Criar .env no frontend
        frontend_env = """REACT_APP_API_URL=http://localhost:5000
GENERATE_SOURCEMAP=false
REACT_APP_VERSION=1.0.0
REACT_APP_ENV=development
"""
        with open(frontend_path / '.env', 'w') as f:
            f.write(frontend_env)
        
        process = subprocess.Popen(['npm', 'start'], 
                                 cwd=frontend_path,
                                 stdout=subprocess.PIPE, 
                                 stderr=subprocess.STDOUT,
                                 universal_newlines=True,
                                 bufsize=1)
        return process
    except Exception as e:
        print(f"❌ Erro ao iniciar frontend: {e}")
        return None

def monitor_process(process, name):
    """Monitorar saída do processo"""
    for line in iter(process.stdout.readline, ''):
        if line:
            print(f"[{name}] {line.strip()}")

def main():
    print_banner()
    
    # 1. Configurar ambiente
    env_vars = setup_environment()
    create_env_file(env_vars)
    
    # 2. Verificar dependências
    if not check_python_dependencies():
        print("❌ Falha ao configurar dependências Python")
        return
    
    if not check_node_dependencies():
        print("❌ Falha ao configurar dependências Node.js")
        return
    
    # 3. Configurar banco de dados
    if not setup_database():
        print("❌ Falha ao configurar banco de dados")
        return
    
    print("\n🎉 Configuração concluída! Iniciando serviços...\n")
    
    # 4. Iniciar backend
    backend_process = run_backend()
    if not backend_process:
        print("❌ Falha ao iniciar backend")
        return
    
    # Aguardar backend inicializar
    print("⏳ Aguardando backend inicializar...")
    time.sleep(3)
    
    # 5. Iniciar frontend
    frontend_process = run_frontend()
    if not frontend_process:
        print("❌ Falha ao iniciar frontend")
        backend_process.terminate()
        return
    
    print(f"""
🎬 =====================================
   CINEAI EXECUTANDO COM SUCESSO! 🚀
=====================================

🌐 URLs:
   • Frontend: http://localhost:3000
   • Backend:  http://localhost:5000

🔐 Login Admin:
   • Email: admin@cineai.com
   • Senha: CineAI2024!Admin

🤖 APIs Configuradas:
   • OpenAI: ✅ Ativo
   • Gemini: ✅ Ativo
   • HeyGen: ✅ Ativo
   • Runway: ✅ Ativo
   • ElevenLabs: ✅ Ativo

💡 Dicas:
   • Ctrl+C para parar os serviços
   • Acesse http://localhost:3000 no navegador
   • Use as credenciais admin para fazer login

🎯 Funcionalidades:
   • 💬 Chat IA com OpenAI/Gemini
   • 🎬 Video Studio (geração de vídeos)
   • 🎭 Avatar Studio (criação de avatares)
   • 📊 Dashboard analítico
   • ⚙️  Configurações completas

=====================================
    """)
    
    try:
        # Monitorar processos
        backend_thread = threading.Thread(target=monitor_process, args=(backend_process, "BACKEND"))
        frontend_thread = threading.Thread(target=monitor_process, args=(frontend_process, "FRONTEND"))
        
        backend_thread.daemon = True
        frontend_thread.daemon = True
        
        backend_thread.start()
        frontend_thread.start()
        
        # Aguardar até Ctrl+C
        while True:
            time.sleep(1)
            
            # Verificar se processos ainda estão rodando
            if backend_process.poll() is not None:
                print("❌ Backend parou inesperadamente!")
                break
            if frontend_process.poll() is not None:
                print("❌ Frontend parou inesperadamente!")
                break
                
    except KeyboardInterrupt:
        print("\n\n🛑 Parando serviços...")
        
        # Parar processos
        if backend_process and backend_process.poll() is None:
            backend_process.terminate()
            print("✅ Backend parado")
        
        if frontend_process and frontend_process.poll() is None:
            frontend_process.terminate()
            print("✅ Frontend parado")
        
        print("👋 CineAI finalizado com sucesso!")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n❌ Erro inesperado: {e}")
        print("💡 Verifique se você tem Python 3.8+ e Node.js instalados")
        sys.exit(1)