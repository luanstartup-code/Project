#!/usr/bin/env python3
"""
🎬 CineAI - Configurador de Variáveis de Ambiente
Configuração fácil e interativa das chaves de API
"""

import os
import sys
import getpass
from pathlib import Path

def print_banner():
    print("""
🎬 =====================================
   CineAI - AI Video Studio Platform
   Configurador de Variáveis de Ambiente
=====================================
    """)

def print_step(step, title):
    print(f"\n📋 Passo {step}: {title}")
    print("=" * 50)

def get_secure_input(prompt, required=True, current_value=None):
    """Obter input do usuário com opção de valor atual"""
    if current_value:
        prompt += f" (atual: {current_value[:10]}...)"
    
    while True:
        value = input(f"   {prompt}: ").strip()
        
        if value:
            return value
        elif not required:
            return current_value or ""
        else:
            print("   ❌ Este campo é obrigatório!")

def load_current_env():
    """Carregar variáveis atuais do .env se existir"""
    env_vars = {}
    env_file = Path('.env')
    
    if env_file.exists():
        with open(env_file, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    env_vars[key] = value
    
    return env_vars

def create_env_file(config):
    """Criar arquivo .env com as configurações"""
    env_content = f"""# 🎬 CineAI - AI Video Studio Platform
# Configurações de Produção
FLASK_ENV=production
SECRET_KEY={config['SECRET_KEY']}
JWT_SECRET_KEY={config['JWT_SECRET_KEY']}
PORT=5000
DATABASE_URL=sqlite:///video_generator.db

# 👤 Administrador
ADMIN_EMAIL={config['ADMIN_EMAIL']}
ADMIN_PASSWORD={config['ADMIN_PASSWORD']}

# 🤖 APIs de Inteligência Artificial
# OpenAI (Sistema Principal)
OPENAI_API_KEY={config['OPENAI_API_KEY']}
OPENAI_MODEL=gpt-4
OPENAI_MAX_TOKENS=4000
OPENAI_TEMPERATURE=0.7

# Google Gemini (Backup)
GEMINI_API_KEY={config['GEMINI_API_KEY']}
GEMINI_MODEL=gemini-pro
GEMINI_MAX_TOKENS=4000
GEMINI_TEMPERATURE=0.7

# 🎭 HeyGen (Criação de Avatares)
HEYGEN_API_KEY={config['HEYGEN_API_KEY']}
HEYGEN_MODEL=heygen-v1
HEYGEN_AVATAR_QUALITY=high

# 🎬 Runway ML (Geração de Vídeos)
RUNWAY_API_KEY={config['RUNWAY_API_KEY']}
RUNWAY_MODEL=gen-3
RUNWAY_QUALITY=high

# 🔊 ElevenLabs (Text-to-Speech)
ELEVENLABS_API_KEY={config['ELEVENLABS_API_KEY']}
ELEVENLABS_VOICE_ID_MALE=7u8qsX4HQsSHJ0f8xsQZ
ELEVENLABS_VOICE_ID_FEMALE=MZxV5lN3cv7hi1376O0m
ELEVENLABS_STABILITY=0.5

# ⚙️ Configurações do Sistema
MAX_FILE_SIZE=100MB
ALLOWED_EXTENSIONS=jpg,jpeg,png,mp4,mov,avi
STORAGE_LOCAL_PATH=src/static/assets
REACT_APP_API_URL=http://localhost:5000
"""
    
    with open('.env', 'w') as f:
        f.write(env_content)

def validate_api_key(key, service):
    """Validar formato básico das chaves de API"""
    if not key:
        return False
    
    validations = {
        'OPENAI_API_KEY': lambda k: k.startswith('sk-') and len(k) > 20,
        'GEMINI_API_KEY': lambda k: k.startswith('AIza') and len(k) == 39,
        'HEYGEN_API_KEY': lambda k: len(k) > 10,
        'RUNWAY_API_KEY': lambda k: k.startswith('key_') and len(k) > 20,
        'ELEVENLABS_API_KEY': lambda k: k.startswith('sk_') and len(k) > 20
    }
    
    if service in validations:
        return validations[service](key)
    return len(key) > 5

def main():
    print_banner()
    
    # Carregar configurações atuais
    current_env = load_current_env()
    is_update = bool(current_env)
    
    if is_update:
        print("✅ Arquivo .env existente encontrado!")
        choice = input("   Deseja atualizar as configurações? (s/n): ").lower()
        if choice != 's':
            print("   Configuração cancelada.")
            return
    
    config = {}
    
    # Passo 1: Configurações Básicas
    print_step(1, "Configurações Básicas do Sistema")
    
    config['SECRET_KEY'] = get_secure_input(
        "Chave secreta do Flask (gerada automaticamente se vazia)", 
        False, 
        current_env.get('SECRET_KEY', 'cineai-secret-key-production-2024')
    ) or 'cineai-secret-key-production-2024'
    
    config['JWT_SECRET_KEY'] = get_secure_input(
        "Chave JWT (gerada automaticamente se vazia)", 
        False,
        current_env.get('JWT_SECRET_KEY', 'cineai-jwt-secret-key-production-2024')
    ) or 'cineai-jwt-secret-key-production-2024'
    
    # Passo 2: Administrador
    print_step(2, "Conta de Administrador")
    
    config['ADMIN_EMAIL'] = get_secure_input(
        "Email do administrador",
        True,
        current_env.get('ADMIN_EMAIL')
    )
    
    config['ADMIN_PASSWORD'] = get_secure_input(
        "Senha do administrador",
        True,
        current_env.get('ADMIN_PASSWORD')
    )
    
    # Passo 3: APIs de IA
    print_step(3, "Chaves de API dos Serviços de IA")
    
    print("   💡 Dica: Pressione ENTER para pular APIs que você não tem")
    
    # OpenAI
    config['OPENAI_API_KEY'] = get_secure_input(
        "🤖 OpenAI API Key (sk-proj-...)",
        False,
        current_env.get('OPENAI_API_KEY')
    )
    
    if config['OPENAI_API_KEY'] and not validate_api_key(config['OPENAI_API_KEY'], 'OPENAI_API_KEY'):
        print("   ⚠️  Formato da chave OpenAI pode estar incorreto")
    
    # Gemini
    config['GEMINI_API_KEY'] = get_secure_input(
        "🧠 Google Gemini API Key (AIza...)",
        False,
        current_env.get('GEMINI_API_KEY')
    )
    
    if config['GEMINI_API_KEY'] and not validate_api_key(config['GEMINI_API_KEY'], 'GEMINI_API_KEY'):
        print("   ⚠️  Formato da chave Gemini pode estar incorreto")
    
    # HeyGen
    config['HEYGEN_API_KEY'] = get_secure_input(
        "🎭 HeyGen API Key",
        False,
        current_env.get('HEYGEN_API_KEY')
    )
    
    # Runway ML
    config['RUNWAY_API_KEY'] = get_secure_input(
        "🎬 Runway ML API Key (key_...)",
        False,
        current_env.get('RUNWAY_API_KEY')
    )
    
    if config['RUNWAY_API_KEY'] and not validate_api_key(config['RUNWAY_API_KEY'], 'RUNWAY_API_KEY'):
        print("   ⚠️  Formato da chave Runway pode estar incorreto")
    
    # ElevenLabs
    config['ELEVENLABS_API_KEY'] = get_secure_input(
        "🔊 ElevenLabs API Key (sk_...)",
        False,
        current_env.get('ELEVENLABS_API_KEY')
    )
    
    if config['ELEVENLABS_API_KEY'] and not validate_api_key(config['ELEVENLABS_API_KEY'], 'ELEVENLABS_API_KEY'):
        print("   ⚠️  Formato da chave ElevenLabs pode estar incorreto")
    
    # Passo 4: Confirmação
    print_step(4, "Confirmação")
    
    print("   📋 Resumo das configurações:")
    print(f"   • Admin Email: {config['ADMIN_EMAIL']}")
    print(f"   • OpenAI: {'✅ Configurada' if config['OPENAI_API_KEY'] else '❌ Não configurada'}")
    print(f"   • Gemini: {'✅ Configurada' if config['GEMINI_API_KEY'] else '❌ Não configurada'}")
    print(f"   • HeyGen: {'✅ Configurada' if config['HEYGEN_API_KEY'] else '❌ Não configurada'}")
    print(f"   • Runway: {'✅ Configurada' if config['RUNWAY_API_KEY'] else '❌ Não configurada'}")
    print(f"   • ElevenLabs: {'✅ Configurada' if config['ELEVENLABS_API_KEY'] else '❌ Não configurada'}")
    
    if not any([config['OPENAI_API_KEY'], config['GEMINI_API_KEY']]):
        print("\n   ⚠️  AVISO: Nenhuma API de IA principal foi configurada!")
        print("   O sistema funcionará com limitações.")
    
    confirm = input("\n   Salvar configurações? (s/n): ").lower()
    
    if confirm == 's':
        # Passo 5: Salvar
        print_step(5, "Salvando Configurações")
        
        try:
            create_env_file(config)
            print("   ✅ Arquivo .env criado com sucesso!")
            print("   🎬 CineAI está pronto para usar!")
            
            print(f"\n🚀 Próximos passos:")
            print(f"   1. python app.py")
            print(f"   2. cd frontend && npm install && npm start")
            print(f"   3. Acesse http://localhost:5000")
            
        except Exception as e:
            print(f"   ❌ Erro ao criar arquivo: {e}")
            
    else:
        print("   Configuração cancelada.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n   ⚠️  Configuração interrompida pelo usuário.")
    except Exception as e:
        print(f"\n   ❌ Erro inesperado: {e}")