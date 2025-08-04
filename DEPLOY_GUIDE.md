# 🚀 Guia de Deploy - CineAI

Deploy do **Frontend no Vercel** e **Backend no Render** com domínios personalizados.

## 🎯 URLs de Produção

- **Frontend**: https://cineai.vercel.app
- **Backend**: https://cineai.render.com
- **Admin**: admin@cineai.com / CineAI2024!Admin

## 📋 Pré-requisitos

1. ✅ Conta no [Vercel](https://vercel.com)
2. ✅ Conta no [Render](https://render.com)
3. ✅ Repositório GitHub limpo
4. ✅ API Keys das integrações

## 🏗️ 1. Preparação do Ambiente

### Execute o configurador de produção:
```bash
python3 setup_env_production.py
```

Isso irá:
- ✅ Criar arquivo .env com suas API keys
- ✅ Gerar .env.example
- ✅ Atualizar .gitignore
- ✅ Configurar URLs de produção

## 🌐 2. Deploy do Frontend (Vercel)

### 2.1 Via Dashboard Vercel
1. Acesse [vercel.com](https://vercel.com)
2. Clique em **"New Project"**
3. Conecte seu repositório GitHub
4. Configure:
   - **Framework**: Create React App
   - **Root Directory**: `frontend`
   - **Build Command**: `npm run build`
   - **Output Directory**: `build`

### 2.2 Configurar Variáveis de Ambiente
No painel do Vercel, vá para **Settings** → **Environment Variables**:

```
REACT_APP_API_URL=https://cineai.render.com
GENERATE_SOURCEMAP=false
REACT_APP_VERSION=1.0.0
```

### 2.3 Configurar Domínio
1. Vá para **Settings** → **Domains**
2. Adicione: `cineai.vercel.app`
3. Configure DNS se necessário

### 2.4 Via CLI (Alternativo)
```bash
# Instalar Vercel CLI
npm i -g vercel

# Deploy
cd frontend
vercel --prod

# Configurar domínio
vercel domains add cineai.vercel.app
```

## 🖥️ 3. Deploy do Backend (Render)

### 3.1 Via Dashboard Render
1. Acesse [render.com](https://render.com)
2. Clique em **"New"** → **"Web Service"**
3. Conecte seu repositório GitHub
4. Configure:
   - **Name**: `cineai-backend`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`

### 3.2 Configurar Variáveis de Ambiente
No painel do Render, vá para **Environment**:

```bash
# Básico
FLASK_ENV=production
SECRET_KEY=cineai-secret-key-production-2024-ultra-secure
JWT_SECRET_KEY=cineai-jwt-secret-key-production-2024-ultra-secure
DATABASE_URL=sqlite:///video_generator.db

# Admin
ADMIN_EMAIL=admin@cineai.com
ADMIN_PASSWORD=CineAI2024!Admin

# APIs (Substitua com suas chaves reais)
OPENAI_API_KEY=sk-proj-YOUR_OPENAI_KEY_HERE
GEMINI_API_KEY=AIza_YOUR_GEMINI_KEY_HERE
HEYGEN_API_KEY=YOUR_HEYGEN_KEY_HERE
RUNWAY_API_KEY=key_YOUR_RUNWAY_KEY_HERE
ELEVENLABS_API_KEY=sk_YOUR_ELEVENLABS_KEY_HERE

# CORS
CORS_ORIGINS=https://cineai.vercel.app
FRONTEND_URL=https://cineai.vercel.app
```

### 3.3 Configurar Domínio Personalizado
1. Vá para **Settings** → **Custom Domain**
2. Adicione: `cineai.render.com`
3. Configure CNAME no seu provedor DNS

## 🔗 4. Conectar Frontend e Backend

### 4.1 Verificar URLs
- Frontend deve usar `REACT_APP_API_URL=https://cineai.render.com`
- Backend deve permitir `CORS_ORIGINS=https://cineai.vercel.app`

### 4.2 Testar Conectividade
```bash
# Testar backend
curl https://cineai.render.com/api/health

# Testar CORS
curl -H "Origin: https://cineai.vercel.app" \
     -H "Access-Control-Request-Method: POST" \
     -H "Access-Control-Request-Headers: X-Requested-With" \
     -X OPTIONS \
     https://cineai.render.com/api/auth/login
```

## 🔄 5. Deploy Automático

### 5.1 GitHub Actions (Opcional)
Crie `.github/workflows/deploy.yml`:

```yaml
name: Deploy
on:
  push:
    branches: [main]

jobs:
  deploy-frontend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: amondnet/vercel-action@v20
        with:
          vercel-token: ${{ secrets.VERCEL_TOKEN }}
          vercel-org-id: ${{ secrets.ORG_ID }}
          vercel-project-id: ${{ secrets.PROJECT_ID }}
          working-directory: ./frontend
```

### 5.2 Auto-Deploy Render
Render faz deploy automático a cada push para a branch main.

## 🧪 6. Teste de Produção

### 6.1 Funcionalidades Críticas
- [ ] Login/Register funcionando
- [ ] Chat IA respondendo
- [ ] API Keys configuradas
- [ ] CORS funcionando
- [ ] Dashboard carregando
- [ ] Autenticação entre serviços

### 6.2 URLs de Teste
```bash
# Frontend
open https://cineai.vercel.app

# Backend Health
curl https://cineai.render.com/api/health

# Login teste
curl -X POST https://cineai.render.com/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@cineai.com","password":"CineAI2024!Admin"}'
```

## 🔧 7. Troubleshooting

### 7.1 Problemas Comuns

**CORS Error:**
- Verificar CORS_ORIGINS no backend
- Verificar REACT_APP_API_URL no frontend

**Build Error (Vercel):**
- Verificar Node.js version em .nvmrc
- Verificar dependências no package.json

**Start Error (Render):**
- Verificar requirements.txt
- Verificar comando start: `gunicorn app:app`

**Auth Error:**
- Verificar SECRET_KEY e JWT_SECRET_KEY
- Verificar cookies e session config

### 7.2 Logs
```bash
# Vercel
vercel logs https://cineai.vercel.app

# Render - ver no dashboard
```

## 📊 8. Monitoramento

### 8.1 Uptime
- Render: Built-in monitoring
- Vercel: Built-in analytics

### 8.2 Performance
- [GTmetrix](https://gtmetrix.com) para frontend
- [Pingdom](https://pingdom.com) para uptime

## 🚀 9. Comandos Rápidos

```bash
# Setup completo
python3 setup_env_production.py

# Commit e push
git add .
git commit -m "🚀 Production ready - Deploy to Vercel & Render"
git push origin main

# URLs finais
echo "Frontend: https://cineai.vercel.app"
echo "Backend:  https://cineai.render.com"
echo "Admin:    admin@cineai.com / CineAI2024!Admin"
```

---

## ✅ Checklist Final

- [ ] `setup_env_production.py` executado
- [ ] Frontend deployado no Vercel
- [ ] Backend deployado no Render  
- [ ] Domínios configurados
- [ ] Variáveis de ambiente definidas
- [ ] CORS configurado
- [ ] Autenticação testada
- [ ] URLs conectadas

**🎬 Seu CineAI está pronto para produção! 🚀**