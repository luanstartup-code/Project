# 🎬 CineAI - AI Video Studio Platform

> **Plataforma completa para criação de vídeos com Inteligência Artificial**

![CineAI](https://img.shields.io/badge/CineAI-v1.0-blue?style=for-the-badge&logo=video&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.8+-green?style=for-the-badge&logo=python&logoColor=white)
![React](https://img.shields.io/badge/React-18+-blue?style=for-the-badge&logo=react&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-purple?style=for-the-badge)

## 🌟 Características Principais

### 🤖 **IA Integrada**
- **OpenAI GPT-4** + **Google Gemini** com fallback automático
- **HeyGen** para criação de avatares realistas
- **Runway ML** para geração de vídeos
- **ElevenLabs** para síntese de voz premium

### 🎨 **Interface Moderna**
- Dashboard analítico completo
- Editor de vídeos com IA
- Studio de avatares interativo
- Chat inteligente para assistência

### 🔐 **Sistema Robusto**
- Autenticação JWT segura
- Banco de dados SQLite/PostgreSQL
- API RESTful documentada
- Deploy em containers Docker

---

## 🚀 Início Rápido

### **Configuração em 3 passos:**

```bash
# 1. Clone e entre no diretório
git clone https://github.com/luanstartup-code/Project.git
cd Project

# 2. Configure as variáveis de ambiente (interativo)
python3 setup_env.py

# 3. Execute o projeto
pip install -r requirements.txt
python create_database.py
python app.py
```

### **Frontend (terminal separado):**
```bash
cd frontend
npm install && npm start
```

### **Acesse em:**
- 🌐 **Frontend**: http://localhost:3000
- 🔧 **API**: http://localhost:5000

📖 **[Guia Completo →](QUICKSTART.md)**

---

## 🏗️ Arquitetura

```
CineAI/
├── 🐍 Backend (Flask + SQLAlchemy)
│   ├── src/models/          # Modelos de dados
│   ├── src/routes/          # Endpoints da API
│   ├── src/services/        # Serviços de IA
│   └── src/utils/           # Utilitários e auth
├── ⚛️ Frontend (React + Tailwind)
│   ├── src/components/      # Componentes UI
│   ├── src/pages/           # Páginas da aplicação
│   ├── src/contexts/        # Estado global
│   └── public/              # Assets estáticos
├── 🗄️ Database (SQLite)
│   └── instance/            # Banco de dados local
└── 🐳 Deploy (Docker + Config)
    ├── Dockerfile           # Container backend
    ├── docker-compose.yml   # Orquestração
    └── render.yaml          # Deploy Render.com
```

---

## 🔑 APIs Suportadas

| Serviço | Função | Status | Obrigatório |
|---------|--------|--------|-------------|
| **OpenAI** | Chat IA, Enhancement | ✅ Ativo | 🟡 Recomendado |
| **Google Gemini** | Backup IA, Fallback | ✅ Ativo | 🟡 Recomendado |
| **HeyGen** | Avatares Realistas | ✅ Ativo | ❌ Opcional |
| **Runway ML** | Geração de Vídeos | ✅ Ativo | ❌ Opcional |
| **ElevenLabs** | Text-to-Speech | ✅ Ativo | ❌ Opcional |

> **💡 Dica**: Configure pelo menos OpenAI OU Gemini para funcionalidade completa

---

## 📱 Funcionalidades

### 🎬 **Video Studio**
- ✅ Geração de vídeos com prompts de IA
- ✅ Editor visual avançado
- ✅ Biblioteca de templates
- ✅ Exportação em múltiplos formatos

### 🎭 **Avatar Studio**
- ✅ Criação de avatares personalizados
- ✅ Animação facial realística
- ✅ Sincronização labial
- ✅ Galeria de avatares

### 💬 **Chat IA**
- ✅ Assistente criativo inteligente
- ✅ Histórico de conversas
- ✅ Enhancement de prompts
- ✅ Sugestões contextuais

### 📊 **Analytics**
- ✅ Dashboard de performance
- ✅ Métricas de uso
- ✅ Relatórios detalhados
- ✅ Insights de IA

---

## 🛠️ Stack Tecnológica

### **Backend**
- **Flask** - Framework web Python
- **SQLAlchemy** - ORM para banco de dados
- **JWT** - Autenticação segura
- **bcrypt** - Hash de senhas
- **python-dotenv** - Gerenciamento de variáveis

### **Frontend**
- **React 18** - Biblioteca UI moderna
- **Tailwind CSS** - Framework CSS utilitário
- **Axios** - Cliente HTTP
- **React Router** - Roteamento SPA

### **IA & APIs**
- **OpenAI API** - GPT-4 para chat e enhancement
- **Google Gemini** - Backup de IA
- **HeyGen API** - Geração de avatares
- **Runway ML** - Criação de vídeos
- **ElevenLabs** - Síntese de voz

### **Deploy**
- **Docker** - Containerização
- **Render.com** - Deploy backend
- **Vercel** - Deploy frontend
- **SQLite/PostgreSQL** - Bancos de dados

---

## 🚀 Deploy

### **Desenvolvimento Local**
```bash
python3 setup_env.py    # Configurar
python app.py           # Backend
npm start              # Frontend
```

### **Produção com Docker**
```bash
docker-compose up -d
```

### **Deploy em Render.com**
1. Fork este repositório
2. Configure as variáveis de ambiente no Render
3. Deploy automático via Git

### **Deploy no Vercel (Frontend)**
```bash
cd frontend
vercel --prod
```

---

## 📋 Requisitos

### **Sistema**
- Python 3.8+
- Node.js 16+
- Git

### **APIs (pelo menos uma de IA)**
- OpenAI API Key
- Google Gemini API Key
- HeyGen API Key (opcional)
- Runway ML API Key (opcional)
- ElevenLabs API Key (opcional)

---

## 🤝 Contribuição

1. **Fork** o projeto
2. **Clone** sua fork
3. **Branch** para feature (`git checkout -b feature/nova-feature`)
4. **Commit** suas mudanças (`git commit -m 'Add nova feature'`)
5. **Push** para branch (`git push origin feature/nova-feature`)
6. **Pull Request**

---

## 📄 Licença

Este projeto está sob a licença **MIT**. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

---

## 📞 Suporte

- 📖 **[Guia Rápido](QUICKSTART.md)** - Setup em 5 minutos
- 🏗️ **[Estrutura](STRUCTURE.md)** - Arquitetura detalhada
- 🔧 **Configuração**: `python3 setup_env.py`

---

<div align="center">

**🎬 Criado com ❤️ para revolucionar a criação de vídeos com IA**

[![GitHub](https://img.shields.io/badge/GitHub-CineAI-black?style=for-the-badge&logo=github)](https://github.com/luanstartup-code/Project)

</div>