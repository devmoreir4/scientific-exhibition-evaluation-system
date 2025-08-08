# Backend - Sistema de Avaliação para Mostra Científica

API REST completa para gerenciamento, distribuição e avaliação de trabalhos científicos.

## 🛠️ Stack Tecnológica

- **Framework**: Flask 3.1.1
- **ORM**: SQLAlchemy 2.0.41
- **Autenticação**: Flask-JWT-Extended 4.7.1
- **CORS**: Flask-CORS 6.0.1
- **Banco de Dados**: PostgreSQL 15-alpine
- **Interface**: Adminer
- **Processamento de Imagens**: Google Gemini API
- **Documentação**: Swagger

## 🔌 Endpoints da API

### Autenticação (`/api/v1/auth`)
| Método | Endpoint | Descrição |
|--------|----------|-----------|
| `POST` | `/auth/token` | Login de avaliador |
| `POST` | `/auth/admin/token` | Login de administrador |
| `POST` | `/auth/register` | Registro de avaliador |

### Administração (`/api/v1/admin`)
| Método | Endpoint | Descrição |
|--------|----------|-----------|
| `GET` | `/admin/users` | Listar usuários |
| `POST` | `/admin/users` | Criar usuário |
| `PUT` | `/admin/users/{id}` | Atualizar usuário |
| `DELETE` | `/admin/users/{id}` | Remover usuário |
| `GET` | `/admin/users/simple` | Lista simplificada de usuários |

### Trabalhos (`/api/v1/admin/works`)
| Método | Endpoint | Descrição |
|--------|----------|-----------|
| `GET` | `/admin/works` | Listar trabalhos |
| `POST` | `/admin/works` | Criar trabalho |
| `PUT` | `/admin/works/{id}` | Atualizar trabalho |
| `DELETE` | `/admin/works/{id}` | Remover trabalho |
| `POST` | `/admin/works/import-csv` | Importar trabalhos via CSV |
| `GET` | `/admin/works/distributions` | Ver distribuições |
| `GET` | `/admin/works/evaluator/{id}` | Trabalhos de um avaliador |

### Distribuição (`/api/v1/admin/works`)
| Método | Endpoint | Descrição |
|--------|----------|-----------|
| `POST` | `/admin/works/distribute` | Distribuir trabalhos automaticamente |
| `GET` | `/admin/works/distribution-status` | Status da distribuição |
| `POST` | `/admin/works/reset-distribution` | Reset da distribuição (emergência) |

### Áreas (`/api/v1/admin`)
| Método | Endpoint | Descrição |
|--------|----------|-----------|
| `GET` | `/admin/areas` | Listar todas as áreas |
| `GET` | `/admin/areas/{area}/subareas` | Listar subáreas de uma área |

### Monitoramento (`/api/v1/admin`)
| Método | Endpoint | Descrição |
|--------|----------|-----------|
| `GET` | `/admin/works/evaluation-progress` | Progresso das avaliações |
| `GET` | `/admin/works/podium` | Gerar pódio |

### Fichas com IA (`/api/v1/admin/sheets`)
| Método | Endpoint | Descrição |
|--------|----------|-----------|
| `POST` | `/admin/sheets/process-ai` | Processar ficha com IA |
| `POST` | `/admin/sheets/confirm` | Confirmar dados extraídos |

### Avaliador (`/api/v1/evaluator`)
| Método | Endpoint | Descrição |
|--------|----------|-----------|
| `GET` | `/evaluator/works/assigned` | Trabalhos atribuídos |
| `GET` | `/evaluator/works/{id}` | Detalhes do trabalho |
| `POST` | `/evaluator/evaluations` | Criar avaliação |
| `GET` | `/evaluator/evaluations/mine` | Minhas avaliações |
| `GET` | `/evaluator/evaluations/work/{id}` | Avaliações de um trabalho específico |
| `PUT` | `/evaluator/change-password` | Alterar senha |

## 🚀 Instalação e Execução

### Com Docker

1. **Configure as variáveis de ambiente**
    - Renomeie o arquivo `.env.example` para `.env` e adicione suas informações

2. **Execute com Docker Compose**
```bash
docker-compose up -d backend
```

3. **Acesse a API**
- **API**: http://localhost:5000/api/v1
- **Documentação**: http://localhost:5000/api/v1/docs
- **Adminer**: http://localhost:8080

### Desenvolvimento Local

1. **Configure o ambiente**
```bash
cd backend
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

2. **Instale as dependências**
```bash
pip install -r requirements.txt
```

3. **Configure as variáveis de ambiente**
```bash
# Windows
set FLASK_ENV=local
# Linux/Mac
export FLASK_ENV=local
```

4. **Inicialize o banco**
```bash
python init_db_local.py
```

5. **Execute a aplicação**
```bash
python run.py
```

## 📚 Documentação da API

### Swagger
A documentação automática está disponível em: http://localhost:5000/api/v1/docs

### Coleção Postman
Uma coleção completa do Postman está disponível em:
`postman_collection/evaluation_system.postman_collection.json`
