# 🔗 Variáveis de Ambiente - CineAI

## 🌐 URLs Descobertas

- **Backend (Render)**: `https://cineai-axkg.onrender.com`
- **Frontend (Vercel)**: `https://seu-frontend.vercel.app` *(substitua pela URL real)*

---

## ⚛️ FRONTEND (Vercel)

### Configurar em: Settings → Environment Variables

| Key | Value |
|-----|-------|
| `REACT_APP_API_URL` | `https://cineai-axkg.onrender.com` |
| `GENERATE_SOURCEMAP` | `false` |
| `REACT_APP_VERSION` | `1.0.0` |
| `REACT_APP_ENV` | `production` |

### ⚠️ Importante:
- **Sem barra final** na URL da API
- Usar **HTTPS** sempre
- Redeploy necessário após mudanças

---

## 🖥️ BACKEND (Render)

### Configurar em: Environment → Add Environment Variable

| Key | Value |
|-----|-------|
| `FLASK_ENV` | `production` |
| `DATABASE_URL` | `sqlite:///video_generator.db` |
| `CORS_ORIGINS` | `https://seu-frontend.vercel.app` |
| `FRONTEND_URL` | `https://seu-frontend.vercel.app` |
| `SECRET_KEY` | `cineai-secret-key-production-2024-ultra-secure` |
| `JWT_SECRET_KEY` | `cineai-jwt-secret-key-production-2024-ultra-secure` |

### 🔑 API Keys (suas chaves reais):

| Key | Value |
|-----|-------|
| `OPENAI_API_KEY` | `sk-proj-bKHxJRa7YpkgCMWdOgFT3BlbkFJGH7u4yJ9K8L3mN4oP5qR6s` |
| `GEMINI_API_KEY` | `AIzaSyB1C2D3E4F5G6H7I8J9K0L1M2N3O4P5Q6R7S8T9` |
| `HEYGEN_API_KEY` | `hg_a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0` |
| `RUNWAY_API_KEY` | `key_1a2b3c4d5e6f7g8h9i0j1k2l3m4n5o6p7q8r9s0t` |
| `ELEVENLABS_API_KEY` | `sk_1234567890abcdef1234567890abcdef12345678` |

### 👤 Admin:

| Key | Value |
|-----|-------|
| `ADMIN_EMAIL` | `admin@cineai.com` |
| `ADMIN_PASSWORD` | `CineAI2024!Admin` |

---

## 🧪 Teste de Conectividade

### 1. Testar Backend:
```bash
curl https://cineai-axkg.onrender.com/api/health
```

### 2. Testar CORS:
```bash
curl -H "Origin: https://seu-frontend.vercel.app" \
     -H "Access-Control-Request-Method: POST" \
     -X OPTIONS \
     https://cineai-axkg.onrender.com/api/auth/login
```

### 3. Testar Login:
```bash
curl -X POST https://cineai-axkg.onrender.com/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@cineai.com","password":"CineAI2024!Admin"}'
```

---

## 📋 Checklist de Deploy

### Frontend (Vercel):
- [ ] Variáveis de ambiente configuradas
- [ ] `REACT_APP_API_URL` apontando para Render
- [ ] Build sem erros
- [ ] Deploy realizado

### Backend (Render):
- [ ] Todas as variáveis configuradas
- [ ] API keys adicionadas
- [ ] `CORS_ORIGINS` com URL do Vercel
- [ ] Start Command: `python3 run_cineai.py`
- [ ] Build sem erros
- [ ] Deploy realizado

### Conectividade:
- [ ] Health check funcionando
- [ ] CORS configurado
- [ ] Login admin funcionando
- [ ] Frontend consegue conectar no backend

---

## 🔧 Troubleshooting

### ❌ CORS Error:
- Verificar `CORS_ORIGINS` no backend
- Verificar `REACT_APP_API_URL` no frontend
- URLs devem corresponder exatamente

### ❌ 404 Not Found:
- Verificar se backend está rodando
- Testar URL do health check
- Verificar Start Command no Render

### ❌ Auth Error:
- Verificar credenciais admin
- Verificar JWT_SECRET_KEY
- Verificar cookies/sessões

---

**🎬 Com essas configurações, frontend e backend estarão conectados! 🚀**