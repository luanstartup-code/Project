FROM node:18-alpine

# Definir diretório de trabalho
WORKDIR /app

# Copiar package.json e package-lock.json
COPY package*.json ./

# Instalar dependências
RUN npm ci --only=production

# Copiar código da aplicação
COPY . .

# Build da aplicação
RUN npm run build

# Instalar serve para servir a aplicação
RUN npm install -g serve

# Expor porta
EXPOSE 3000

# Comando para executar a aplicação
CMD ["serve", "-s", "build", "-l", "3000"]