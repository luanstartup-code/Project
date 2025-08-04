# 🎯 CineAI - Configuração Final de Deploy

## 🌐 URLs Configuradas

- **Backend (Render)**: `https://cineai-axkg.onrender.com`
- **Service ID**: `srv-d283ir6uk2gs73eqtgag`
- **Frontend (Vercel)**: `https://cineai.vercel.app`

---

## ⚛️ VERCEL - Environment Variables

### Configure em: Settings → Environment Variables

```
REACT_APP_API_URL=https://cineai-axkg.onrender.com
GENERATE_SOURCEMAP=false
REACT_APP_VERSION=1.0.0
REACT_APP_ENV=production
```

**⚠️ Importante**: Redeploy necessário após adicionar variáveis!

---

## 🖥️ RENDER - Environment Variables

### Configure em: Environment → Add Environment Variable

#### 🔧 Configurações Básicas:
```
FLASK_ENV=production
DATABASE_URL=sqlite:///video_generator.db
SECRET_KEY=cineai-secret-key-production-2024-ultra-secure
JWT_SECRET_KEY=cineai-jwt-secret-key-production-2024-ultra-secure
```

#### 🌐 CORS (CRÍTICO para conectividade):
```
CORS_ORIGINS=https://cineai.vercel.app
FRONTEND_URL=https://cineai.vercel.app
```

#### 🔑 Suas API Keys:
```
OPENAI_API_KEY=sk-proj-bKHxJRa7YpkgCMWdOgFT3BlbkFJGH7u4yJ9K8L3mN4oP5qR6s
GEMINI_API_KEY=AIzaSyB1C2D3E4F5G6H7I8J9K0L1M2N3O4P5Q6R7S8T9
HEYGEN_API_KEY=hg_a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0
RUNWAY_API_KEY=key_1a2b3c4d5e6f7g8h9i0j1k2l3m4n5o6p7q8r9s0t
ELEVENLABS_API_KEY=sk_1234567890abcdef1234567890abcdef12345678
```

#### 👤 Admin:
```
ADMIN_EMAIL=admin@cineai.com
ADMIN_PASSWORD=CineAI2024!Admin
```

**Start Command**: `python3 run_cineai.py`

---

## 🧪 Teste de Conectividade

### 1. Testar Backend Health:
```bash
curl https://cineai-axkg.onrender.com/api/health
```
**Resultado esperado**: `{"status": "healthy", "message": "API funcionando!"}`

### 2. Testar CORS:
```bash
curl -H "Origin: https://cineai.vercel.app" \
     -H "Access-Control-Request-Method: POST" \
     -X OPTIONS \
     https://cineai-axkg.onrender.com/api/auth/login
```
**Resultado esperado**: Headers CORS retornados

### 3. Testar Admin Login:
```bash
curl -X POST https://cineai-axkg.onrender.com/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@cineai.com","password":"CineAI2024!Admin"}'
```
**Resultado esperado**: Token JWT retornado

---

## 📋 Checklist Final

### ✅ Backend (Render):
- [ ] Todas as variáveis de ambiente configuradas
- [ ] API keys adicionadas corretamente
- [ ] CORS_ORIGINS = `https://cineai.vercel.app`
- [ ] Start Command = `python3 run_cineai.py`
- [ ] Build successful
- [ ] Health endpoint respondendo

### ✅ Frontend (Vercel):
- [ ] `REACT_APP_API_URL` = `https://cineai-axkg.onrender.com`
- [ ] Build successful
- [ ] Deploy realizado
- [ ] Aplicação carregando

### ✅ Conectividade:
- [ ] Frontend consegue chamar backend
- [ ] CORS funcionando
- [ ] Login admin funcionando
- [ ] Todas as APIs ativas

---

## 🔧 Troubleshooting

### ❌ **CORS Error**: 
- Verificar se `CORS_ORIGINS` no Render tem **exatamente** `https://cineai.vercel.app`
- Verificar se `REACT_APP_API_URL` no Vercel tem **exatamente** `https://cineai-axkg.onrender.com`

### ❌ **500 Internal Server Error**:
- Verificar se todas as API keys estão configuradas no Render
- Verificar logs do Render para erros específicos

### ❌ **Frontend não carrega**:
- Verificar se build do Vercel foi successful
- Verificar se variáveis de ambiente foram adicionadas antes do build

---

## 🎯 URLs para Testar

1. **Backend Health**: https://cineai-axkg.onrender.com/api/health
2. **Frontend**: https://cineai.vercel.app
3. **Login**: admin@cineai.com / CineAI2024!Admin

---

**🎬 Configuração completa! Frontend e Backend conectados! 🚀**