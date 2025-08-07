# Sistema de Avaliação para Mostra Científica

Sistema completo para gerenciamento e avaliação de trabalhos científicos, desenvolvido com **Flask** (backend) e **Vue.js** (frontend).

## 🚀 Funcionalidades

### **Administração**
- ✅ Gestão completa de avaliadores (CRUD)
- ✅ Importação de trabalhos via CSV
- ✅ Distribuição automática inteligente de trabalhos
- ✅ Processamento de fichas com OCR e IA
- ✅ Monitoramento de progresso das avaliações
- ✅ Dashboard com estatísticas e relatórios

### **Avaliação**
- ✅ Sistema de login seguro com JWT
- ✅ Interface intuitiva para avaliação online
- ✅ Critérios múltiplos (1-5 pontos)
- ✅ Validação de distribuição de trabalhos
- ✅ Histórico de avaliações realizadas

### **Tecnologias Avançadas**
- ✅ **OCR Tradicional**: Extração de dados de fichas físicas
- ✅ **IA Generativa**: Processamento inteligente com Google AI
- ✅ **Distribuição Inteligente**: Algoritmo que considera expertise e conflitos
- ✅ **Validação Robusta**: Múltiplas camadas de verificação

## 🏗️ Arquitetura

```
scientific-exhibition-evaluation-system/
├── backend/                 # API Flask
│   ├── app/
│   │   ├── blueprints/     # Rotas da API
│   │   ├── services/       # Lógica de negócio
│   │   └── models.py       # Modelos do banco
│   └── requirements.txt
├── frontend/               # SPA Vue.js
│   ├── src/
│   │   ├── views/         # Páginas da aplicação
│   │   ├── stores/        # Gerenciamento de estado
│   │   └── routes.js      # Configuração de rotas
│   └── package.json
└── docker-compose.yml     # Orquestração dos containers
```

## 🐳 Executando com Docker

### **Pré-requisitos**
- Docker
- Docker Compose

### **1. Clone o repositório**
```bash
git clone <url-do-repositorio>
cd scientific-exhibition-evaluation-system
```

### **2. Configure as variáveis de ambiente**
Crie um arquivo `.env` na raiz do projeto:
```bash
# Configurações do Banco
DB_NAME=scientific_exhibition
DB_USER=postgres
DB_PASSWORD=sua_senha_segura

# Chaves de Segurança
SECRET_KEY=sua_chave_secreta_aqui
JWT_SECRET_KEY=sua_jwt_secret_aqui

# API do Google (opcional, para IA)
GOOGLE_API_KEY=sua_chave_google_aqui

# Ambiente
FLASK_ENV=development
```

### **3. Execute os containers**
```bash
# Executar todos os serviços
docker-compose up -d

# Ou para ver os logs em tempo real
docker-compose up
```

### **4. Acesse a aplicação**
- **Frontend**: http://localhost:4173
- **Backend API**: http://localhost:5000
- **Documentação API**: http://localhost:5000/apidocs/
- **Adminer (DB)**: http://localhost:8080

### **5. Comandos úteis**
```bash
# Parar todos os serviços
docker-compose down

# Reconstruir containers
docker-compose up --build

# Ver logs de um serviço específico
docker-compose logs backend
docker-compose logs frontend
```

## 🔧 Desenvolvimento Local

### **Backend (Flask)**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate     # Windows

pip install -r requirements.txt
python run.py
```

### **Frontend (Vue.js)**
```bash
cd frontend
npm install
npm run dev
```

## 📊 Estrutura de Dados

### **Formatos de Separação**
- **Autores**: Separados por ponto e vírgula (;)
- **Subáreas**: Separadas por ponto e vírgula (;)

> **Nota**: O uso de ponto e vírgula (;) como separador evita conflitos com vírgulas que podem aparecer nos nomes das subáreas.

### **Tipos de Avaliador**
- **Pedagógico**: Avaliadores com área contendo "pedag"
- **Técnico**: Demais avaliadores

### **Critérios de Avaliação**
1. Critério 1 (1-5 pontos)
2. Critério 2 (1-5 pontos)
3. Critério 3 (1-5 pontos)
4. Critério 4 (1-5 pontos)
5. Critério 5 (1-5 pontos)

## 🔐 Segurança

- **Autenticação JWT**: Tokens seguros para todas as operações
- **Validação de Distribuição**: Apenas avaliadores distribuídos podem avaliar
- **Prevenção de Duplicatas**: Sistema impede avaliações duplicadas
- **Validação de Scores**: Critérios devem estar entre 1-5

## 📚 Documentação

- **[API Documentation](backend/API_DOCUMENTATION.md)**: Documentação completa da API
- **[Frontend README](frontend/README.md)**: Guia do frontend Vue.js

## 🚀 Deploy

### **Produção**
```bash
# Configurar variáveis de produção
export FLASK_ENV=production
```

### **Variáveis de Ambiente de Produção**
```bash
FLASK_ENV=production
SECRET_KEY=<chave_secreta_forte>
JWT_SECRET_KEY=<jwt_secret_forte>
DB_NAME=scientific_exhibition_prod
DB_USER=postgres
DB_PASSWORD=<senha_forte>
```

## 🤝 Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

---

**Desenvolvido com ❤️ para Mostras Científicas**
