# 🎬 CineAI - Guia Rápido

> Configuração e execução em menos de 5 minutos!

## 🚀 Início Rápido

### 1️⃣ Clone o Repositório
```bash
git clone https://github.com/luanstartup-code/Project.git
cd Project
```

### 2️⃣ Configure as Variáveis de Ambiente
```bash
python3 setup_env.py
```

**O script irá guiá-lo através de:**
- 📧 Configuração do administrador
- 🤖 Chaves de API (OpenAI, Gemini, HeyGen, Runway, ElevenLabs)
- ⚙️ Configurações do sistema

### 3️⃣ Execute o Backend
```bash
# Instalar dependências
pip install -r requirements.txt

# Criar banco de dados
python create_database.py

# Executar servidor
python app.py
```

### 4️⃣ Execute o Frontend
```bash
# Em outro terminal
cd frontend
npm install
npm start
```

### 5️⃣ Acesse a Aplicação
```
🌐 Frontend: http://localhost:3000
🔧 Backend API: http://localhost:5000
```

---

## 🔑 APIs Necessárias

### **Obrigatórias (pelo menos uma):**
- 🤖 **OpenAI**: https://platform.openai.com/api-keys
- 🧠 **Google Gemini**: https://aistudio.google.com/app/apikey

### **Opcionais:**
- 🎭 **HeyGen**: https://heygen.com
- 🎬 **Runway ML**: https://runwayml.com
- 🔊 **ElevenLabs**: https://elevenlabs.io

---

## 📋 Configuração Manual (Alternativa)

Se preferir configurar manualmente, edite o arquivo `.env`:

```env
# Básico
ADMIN_EMAIL=seu@email.com
ADMIN_PASSWORD=suasenha123

# IA (pelo menos uma)
OPENAI_API_KEY=sk-proj-sua_chave_aqui
GEMINI_API_KEY=AIza_sua_chave_aqui

# Opcionais
HEYGEN_API_KEY=sua_chave_heygen
RUNWAY_API_KEY=key_sua_chave_runway
ELEVENLABS_API_KEY=sk_sua_chave_elevenlabs
```

---

## 🎯 Funcionalidades Principais

### ✅ **Chat IA**
- Conversas inteligentes com OpenAI/Gemini
- Histórico de conversas
- Fallback automático entre APIs

### ✅ **Video Studio**
- Geração de vídeos com IA
- Integração com Runway ML
- Editor de prompts inteligente

### ✅ **Avatar Studio**
- Criação de avatares com HeyGen
- Personalização completa
- Galeria de avatares

### ✅ **Sistema Completo**
- Autenticação JWT
- Dashboard analítico
- Gerenciamento de projetos
- Upload de arquivos

---

## 🔧 Comandos Úteis

```bash
# Reconfigurar variáveis
python3 setup_env.py

# Resetar banco de dados
python create_database.py

# Verificar logs
tail -f logs/app.log

# Build para produção
docker-compose up -d
```

---

## 🆘 Troubleshooting

### **Erro de módulo não encontrado:**
```bash
pip install -r requirements.txt
```

### **Erro de banco de dados:**
```bash
python create_database.py
```

### **Erro de API:**
- Verifique se as chaves estão corretas no `.env`
- Execute `python3 setup_env.py` para reconfigurar

### **Frontend não carrega:**
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
npm start
```

---

## 📞 Suporte

- 📚 **Documentação completa**: `README.md`
- 🏗️ **Estrutura do projeto**: `STRUCTURE.md`
- 🤖 **Configuração**: Execute `python3 setup_env.py`

---

**🎬 Pronto! Seu CineAI está funcionando! 🚀**