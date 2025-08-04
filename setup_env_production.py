#!/usr/bin/env python3
"""
🎬 CineAI - Configurador de Produção
Configuração automática com suas chaves de API
"""

import os
import sys
from pathlib import Path

def print_banner():
    print("""
🎬 =====================================
   CineAI - AI Video Studio Platform
   Configurador de Produção
=====================================
    """)

def create_production_env():
    """Criar arquivo .env com configurações de produção"""
    env_content = """# 🎬 CineAI - AI Video Studio Platform
# Configurações de Produção

# ⚙️ Configurações Básicas
FLASK_ENV=production
SECRET_KEY=cineai-secret-key-production-2024-ultra-secure
JWT_SECRET_KEY=cineai-jwt-secret-key-production-2024-ultra-secure
PORT=5000
DATABASE_URL=sqlite:///video_generator.db

# 👤 Administrador
ADMIN_EMAIL=admin@cineai.com
ADMIN_PASSWORD=CineAI2024!Admin

# 🤖 APIs de Inteligência Artificial
# OpenAI (Sistema Principal)
OPENAI_API_KEY=sk-proj-YOUR_OPENAI_KEY_HERE
OPENAI_MODEL=gpt-4
OPENAI_MAX_TOKENS=4000
OPENAI_TEMPERATURE=0.7

# Google Gemini (Backup)
GEMINI_API_KEY=AIza_YOUR_GEMINI_KEY_HERE
GEMINI_MODEL=gemini-pro
GEMINI_MAX_TOKENS=4000
GEMINI_TEMPERATURE=0.7

# 🎭 HeyGen (Criação de Avatares)
HEYGEN_API_KEY=YOUR_HEYGEN_KEY_HERE
HEYGEN_MODEL=heygen-v1
HEYGEN_AVATAR_QUALITY=high

# 🎬 Runway ML (Geração de Vídeos)
RUNWAY_API_KEY=key_YOUR_RUNWAY_KEY_HERE
RUNWAY_MODEL=gen-3
RUNWAY_QUALITY=high

# 🔊 ElevenLabs (Text-to-Speech)
ELEVENLABS_API_KEY=sk_YOUR_ELEVENLABS_KEY_HERE
ELEVENLABS_VOICE_ID_MALE=21m00Tcm4TlvDq8ikWAM
ELEVENLABS_VOICE_ID_FEMALE=EXAVITQu4vr4xnSDxMaL
ELEVENLABS_STABILITY=0.5

# ⚙️ Configurações do Sistema
MAX_FILE_SIZE=100MB
ALLOWED_EXTENSIONS=jpg,jpeg,png,mp4,mov,avi
STORAGE_LOCAL_PATH=src/static/assets

# 🌐 URLs de Produção
REACT_APP_API_URL=https://cineai.render.com
FRONTEND_URL=https://cineai.vercel.app
CORS_ORIGINS=https://cineai.vercel.app,http://localhost:3000

# 🔐 Configurações de Segurança
CORS_SUPPORTS_CREDENTIALS=true
SESSION_COOKIE_SECURE=true
SESSION_COOKIE_HTTPONLY=true
SESSION_COOKIE_SAMESITE=None
"""
    
    with open('.env', 'w') as f:
        f.write(env_content)

def create_env_example():
    """Criar arquivo .env.example para referência"""
    env_example_content = """# 🎬 CineAI - AI Video Studio Platform
# Arquivo de exemplo - NÃO commitar o .env real

# ⚙️ Configurações Básicas
FLASK_ENV=production
SECRET_KEY=sua_chave_secreta_aqui
JWT_SECRET_KEY=sua_chave_jwt_aqui
PORT=5000
DATABASE_URL=sqlite:///video_generator.db

# 👤 Administrador
ADMIN_EMAIL=admin@cineai.com
ADMIN_PASSWORD=sua_senha_admin

# 🤖 APIs de IA
OPENAI_API_KEY=sk-proj-sua_chave_openai
GEMINI_API_KEY=AIza_sua_chave_gemini
HEYGEN_API_KEY=sua_chave_heygen
RUNWAY_API_KEY=key_sua_chave_runway
ELEVENLABS_API_KEY=sk_sua_chave_elevenlabs

# 🌐 URLs
REACT_APP_API_URL=https://seu-backend.render.com
FRONTEND_URL=https://seu-frontend.vercel.app
CORS_ORIGINS=https://seu-frontend.vercel.app
"""
    
    with open('.env.example', 'w') as f:
        f.write(env_example_content)

def update_gitignore():
    """Atualizar .gitignore para produção"""
    gitignore_content = """# 🎬 CineAI - Arquivos ignorados

# Ambiente e configurações sensíveis
.env
.env.local
.env.production
instance/
*.db
*.sqlite

# Python
__pycache__/
*.pyc
*.pyo
*.pyd
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual environments
venv/
env/
ENV/
env.bak/
venv.bak/

# IDEs
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
.DS_Store?
._*
.Spotlight-V100
.Trashes
ehthumbs.db
Thumbs.db

# Logs
*.log
logs/

# Node.js (Frontend)
frontend/node_modules/
frontend/npm-debug.log*
frontend/yarn-debug.log*
frontend/yarn-error.log*
frontend/.pnp
frontend/.pnp.js
frontend/coverage/
frontend/build/
frontend/.env.local
frontend/.env.development.local
frontend/.env.test.local
frontend/.env.production.local

# Runtime
*.pid
*.seed
*.pid.lock

# Coverage directory used by tools like istanbul
coverage/

# Dependency directories
node_modules/

# Temporary folders
tmp/
temp/
"""
    
    with open('.gitignore', 'w') as f:
        f.write(gitignore_content)

def main():
    print_banner()
    
    print("🚀 Configurando ambiente de produção...")
    
    # Criar arquivos de ambiente
    create_production_env()
    print("✅ Arquivo .env criado com chaves de produção")
    
    create_env_example()
    print("✅ Arquivo .env.example criado")
    
    update_gitignore()
    print("✅ .gitignore atualizado")
    
    print(f"""
🎉 Configuração de produção concluída!

📋 Próximos passos:
   1. Commit e push para GitHub
   2. Deploy frontend no Vercel (cineai.vercel.app)
   3. Deploy backend no Render (cineai.render.com)
   4. Configurar variáveis de ambiente nos serviços

🌐 URLs configuradas:
   • Frontend: https://cineai.vercel.app
   • Backend: https://cineai.render.com

🔐 Credenciais de admin:
   • Email: admin@cineai.com
   • Senha: CineAI2024!Admin

⚠️  IMPORTANTE: 
   • O arquivo .env foi criado mas NÃO será commitado
   • Configure as variáveis manualmente no Vercel e Render
   • Use .env.example como referência
    """)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Configuração cancelada pelo usuário.")
    except Exception as e:
        print(f"\n❌ Erro: {e}")