# Sistema de Avaliação para Mostra Científica

Sistema para gerenciamento, distribuição e avaliação de trabalhos científicos em mostras e feiras de ciência.

## Visão Geral

Este sistema oferece uma solução completa para organizadores de mostras científicas, permitindo:

- **Cadastro e gerenciamento** de avaliadores e trabalhos
- **Distribuição automática** de trabalhos entre avaliadores
- **Avaliação online** com critérios padronizados
- **Monitoramento em tempo real** do progresso das avaliações
- **Geração de pódio** automático
- **Processamento de fichas** com IA

## Stack Tecnológica

### Backend
- **Framework**: Flask
- **ORM**: SQLAlchemy
- **Autenticação**: Flask-JWT-Extended
- **Banco de Dados**: PostgreSQL
- **IA**: Google Gemini API
- **Documentação**: Swagger

### Frontend
- **Framework**: Vue 3.4.0
- **Build Tool**: Vite 5.0.0
- **Gerenciamento de Estado**: Pinia 2.1.0
- **Roteamento**: Vue Router 4.2.0
- **HTTP Client**: Axios 1.6.0

### Infraestrutura
- **Containerização**: Docker & Docker Compose
- **Banco de Dados**: PostgreSQL 15-alpine
- **Interface DB**: Adminer

## Instalação e Execução

### Pré-requisitos
- Docker e Docker Compose
- Node.js 20+ (desenvolvimento local)
- Python 3.11+ (desenvolvimento local)

### Execução com Docker

1. **Clone o repositório**
```bash
git clone https://github.com/devmoreir4/scientific-exhibition-evaluation-system.git
cd scientific-exhibition-evaluation-system
```

2. **Configure as variáveis de ambiente**
    - Renomeie o arquivo `.env.example` para `.env` e adicione suas informações

3. **Execute os serviços**
```bash
docker-compose up --build
```

4. **Cadastrar avaliadores de exemplo (opcional)**
Se quiser cadastrar avaliadores de exemplo no banco, execute o comando abaixo após o backend estar rodando:
```bash
docker exec -it evaluation_backend python init_evaluators.py
```

5. **Acesse a aplicação**
- **Frontend**: http://localhost:4173
- **API**: http://localhost:5000/api/v1
- **Adminer (DB)**: http://localhost:8080
- **Documentação API**: http://localhost:5000/api/v1/docs

### Desenvolvimento Local

#### Backend (SQLite)
```bash
cd backend
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate

pip install -r requirements.txt
python init_db_local.py
set FLASK_ENV=local  # Windows
export FLASK_ENV=local  # Linux/Mac
python run.py
```

#### Frontend
```bash
cd frontend
npm install
npm run dev
```

## Funcionalidades Principais

### Para Administradores
- **Gestão de Usuários**: Cadastro, edição e remoção de avaliadores
- **Gestão de Trabalhos**: Importação CSV, edição e remoção
- **Distribuição**: Algoritmo automático de distribuição de trabalhos
- **Monitoramento**: Acompanhamento do progresso das avaliações
- **Pódio**: Geração automática de rankings
- **Processamento de Fichas**: IA para extrair notas de imagens

### Para Avaliadores
- **Dashboard**: Visão geral dos trabalhos atribuídos
- **Avaliação**: Formulário com 5 critérios (1-5 pontos)
- **Histórico**: Visualização de avaliações realizadas
- **Alteração de Senha**: Gerenciamento de credenciais

## Monitoramento

O sistema oferece dashboards em tempo real para:
- Progresso das avaliações
- Distribuição de trabalhos
- Performance dos avaliadores
- Rankings e pódios

## Integração com IA

Opcionalmente, o sistema pode processar fichas de avaliação:
- Upload de imagem da ficha
- Extração automática das notas
- Confirmação manual pelo admin
