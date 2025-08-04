# 🚀 Como Executar o CineAI

## 📋 Pré-requisitos

- **Python 3.8+** instalado
- **Node.js 16+** e npm instalados
- **Git** instalado

## ⚡ Execução Rápida

### 1️⃣ Execute o script completo:
```bash
python3 run_cineai.py
```

**Isso vai automaticamente:**
- ✅ Configurar todas as variáveis de ambiente com suas API keys
- ✅ Instalar dependências Python e Node.js
- ✅ Configurar banco de dados
- ✅ Iniciar backend Flask (porta 5000)
- ✅ Iniciar frontend React (porta 3000)

### 2️⃣ Acesse no navegador:
```
http://localhost:3000
```

### 3️⃣ Faça login:
- **Email**: `admin@cineai.com`
- **Senha**: `CineAI2024!Admin`

## 🛑 Para Parar

Pressione `Ctrl+C` no terminal para parar ambos os serviços.

## 🔧 Execução Manual (Alternativa)

Se preferir executar manualmente:

### Backend:
```bash
# Instalar dependências
pip install -r requirements.txt

# Configurar banco
python create_database.py

# Executar
python app.py
```

### Frontend:
```bash
# Entrar na pasta
cd frontend

# Instalar dependências
npm install

# Executar
npm start
```

## 🤖 APIs Configuradas

O script já inclui suas chaves de API:
- **OpenAI**: ✅ GPT-4
- **Google Gemini**: ✅ Backup
- **HeyGen**: ✅ Avatares
- **Runway ML**: ✅ Vídeos
- **ElevenLabs**: ✅ Text-to-Speech

## 🎯 Funcionalidades Disponíveis

- 💬 **Chat IA**: Converse com GPT-4/Gemini
- 🎬 **Video Studio**: Gere vídeos com IA
- 🎭 **Avatar Studio**: Crie avatares realistas
- 📊 **Dashboard**: Métricas e analytics
- ⚙️ **Configurações**: Gerencie API keys

## 🌐 URLs Importantes

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:5000
- **Health Check**: http://localhost:5000/api/health

## 🆘 Problemas Comuns

### Erro de módulo não encontrado:
```bash
pip install -r requirements.txt
```

### Erro no frontend:
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
```

### Erro de banco de dados:
```bash
python create_database.py
```

---

**🎬 Pronto! Seu CineAI está rodando! 🚀**