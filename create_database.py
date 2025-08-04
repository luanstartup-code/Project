#!/usr/bin/env python3
"""
CineAI - Script de Criação de Banco de Dados
Cria o banco SQLite com dados iniciais para deploy
"""

import sqlite3
import os
import hashlib
from datetime import datetime

def hash_password(password):
    """Hash simples para senha (em produção usar bcrypt)"""
    return hashlib.sha256(password.encode()).hexdigest()

def create_database():
    """Criar banco de dados SQLite com estrutura completa"""
    
    # Criar diretório instance se não existir
    os.makedirs('instance', exist_ok=True)
    
    # Conectar ao banco
    db_path = 'instance/video_generator.db'
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    print("🗄️ Criando tabelas do banco de dados...")
    
    # Tabela users
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email VARCHAR(255) UNIQUE NOT NULL,
            password_hash VARCHAR(255) NOT NULL,
            name VARCHAR(255) NOT NULL,
            is_active BOOLEAN DEFAULT 1,
            is_admin BOOLEAN DEFAULT 0,
            is_verified BOOLEAN DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            last_login TIMESTAMP,
            login_count INTEGER DEFAULT 0,
            failed_login_attempts INTEGER DEFAULT 0,
            locked_until TIMESTAMP
        )
    ''')
    
    # Tabela avatars
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS avatars (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name VARCHAR(255) NOT NULL,
            description TEXT,
            image_url VARCHAR(500),
            status VARCHAR(50) DEFAULT 'pending',
            user_id INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
        )
    ''')
    
    # Tabela projects
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS projects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title VARCHAR(255) NOT NULL,
            description TEXT,
            status VARCHAR(50) DEFAULT 'draft',
            user_id INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
        )
    ''')
    
    # Tabela scenes
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS scenes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title VARCHAR(255) NOT NULL,
            script TEXT,
            duration INTEGER DEFAULT 30,
            order_index INTEGER DEFAULT 0,
            project_id INTEGER,
            avatar_id INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (project_id) REFERENCES projects (id) ON DELETE CASCADE,
            FOREIGN KEY (avatar_id) REFERENCES avatars (id)
        )
    ''')
    
    # Tabela sessions (chat)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title VARCHAR(255) DEFAULT 'Nova conversa',
            user_id INTEGER,
            message_count INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
        )
    ''')
    
    # Tabela messages
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            content TEXT NOT NULL,
            role VARCHAR(50) NOT NULL,
            session_id INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (session_id) REFERENCES sessions (id) ON DELETE CASCADE
        )
    ''')
    
    # Tabela videos
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS videos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title VARCHAR(255) NOT NULL,
            description TEXT,
            file_path VARCHAR(500),
            thumbnail_path VARCHAR(500),
            duration INTEGER,
            status VARCHAR(50) DEFAULT 'processing',
            project_id INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (project_id) REFERENCES projects (id) ON DELETE CASCADE
        )
    ''')
    
    print("✅ Tabelas criadas com sucesso!")
    
    # Inserir dados iniciais
    print("📊 Inserindo dados iniciais...")
    
    # Usuário admin
    admin_password = hash_password('admin123')
    cursor.execute('''
        INSERT OR IGNORE INTO users 
        (email, password_hash, name, is_active, is_admin, is_verified)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', ('admin@cineai.com', admin_password, 'Administrator', 1, 1, 1))
    
    # Usuário demo
    demo_password = hash_password('demo123')
    cursor.execute('''
        INSERT OR IGNORE INTO users 
        (email, password_hash, name, is_active, is_admin, is_verified)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', ('demo@cineai.com', demo_password, 'Usuário Demo', 1, 0, 1))
    
    # Projeto demo
    cursor.execute('''
        INSERT OR IGNORE INTO projects 
        (title, description, status, user_id)
        VALUES (?, ?, ?, ?)
    ''', ('Projeto Demo CineAI', 'Projeto demonstrativo da plataforma CineAI', 'completed', 2))
    
    # Avatar demo
    cursor.execute('''
        INSERT OR IGNORE INTO avatars 
        (name, description, status, user_id)
        VALUES (?, ?, ?, ?)
    ''', ('Avatar Demo', 'Avatar demonstrativo para testes', 'completed', 2))
    
    # Sessão de chat demo
    cursor.execute('''
        INSERT OR IGNORE INTO sessions 
        (title, user_id, message_count)
        VALUES (?, ?, ?)
    ''', ('Chat Demo CineAI', 2, 2))
    
    # Mensagens demo
    cursor.execute('''
        INSERT OR IGNORE INTO messages 
        (content, role, session_id)
        VALUES (?, ?, ?)
    ''', ('Olá! Como posso criar um vídeo com avatar?', 'user', 1))
    
    cursor.execute('''
        INSERT OR IGNORE INTO messages 
        (content, role, session_id)
        VALUES (?, ?, ?)
    ''', ('Olá! Para criar um vídeo com avatar no CineAI, siga estes passos: 1) Acesse o Avatar Studio, 2) Crie ou selecione um avatar, 3) Vá ao Video Studio, 4) Configure seu roteiro, 5) Gere o vídeo! É muito simples!', 'assistant', 1))
    
    # Commit das mudanças
    conn.commit()
    
    print("✅ Dados iniciais inseridos!")
    
    # Verificar dados
    cursor.execute('SELECT COUNT(*) FROM users')
    user_count = cursor.fetchone()[0]
    
    cursor.execute('SELECT COUNT(*) FROM projects')
    project_count = cursor.fetchone()[0]
    
    cursor.execute('SELECT COUNT(*) FROM avatars')
    avatar_count = cursor.fetchone()[0]
    
    cursor.execute('SELECT COUNT(*) FROM sessions')
    session_count = cursor.fetchone()[0]
    
    cursor.execute('SELECT COUNT(*) FROM messages')
    message_count = cursor.fetchone()[0]
    
    print(f"📊 Estatísticas do banco:")
    print(f"  👥 Usuários: {user_count}")
    print(f"  📁 Projetos: {project_count}")
    print(f"  🎭 Avatares: {avatar_count}")
    print(f"  💬 Sessões de chat: {session_count}")
    print(f"  📝 Mensagens: {message_count}")
    
    # Fechar conexão
    conn.close()
    
    # Verificar tamanho do arquivo
    db_size = os.path.getsize(db_path)
    print(f"  💾 Tamanho do banco: {db_size} bytes ({db_size/1024:.1f} KB)")
    
    print(f"\n🎉 Banco de dados criado: {db_path}")
    return db_path

if __name__ == "__main__":
    print("🎬 CineAI - Criação de Banco de Dados")
    print("=====================================")
    
    try:
        db_path = create_database()
        print(f"\n✅ Banco criado com sucesso em: {db_path}")
        print("🚀 Pronto para deploy!")
        
    except Exception as e:
        print(f"\n❌ Erro ao criar banco: {e}")
        exit(1)