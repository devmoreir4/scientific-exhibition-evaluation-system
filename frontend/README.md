# Frontend - Sistema de Avaliação para Mostra Científica

Interface moderna e responsiva para gerenciamento e avaliação de trabalhos científicos.

## Tecnologias

### Core
- **Framework**: Vue 3.4.0
- **Build Tool**: Vite 5.0.0
- **Roteamento**: Vue Router 4.2.0
- **Estado Global**: Pinia 2.1.0

### HTTP e Comunicação
- **HTTP Client**: Axios 1.6.0
- **API**: Comunicação com backend Flask
- **Autenticação**: JWT Tokens

## Páginas e Funcionalidades

### Páginas Públicas
- **LoginView**: Autenticação de usuários

### Páginas Administrativas
- **AdminDashboardView**: Dashboard principal
- **AdminUsersView**: Gestão de usuários
- **AdminWorksView**: Gestão de trabalhos
- **AdminDistributionsView**: Distribuição de trabalhos
- **AdminMonitoringView**: Monitoramento
- **AdminPodiumView**: Geração de pódio
- **AdminSheetsView**: Processamento de fichas

### Páginas do Avaliador
- **EvaluatorDashboardView**: Dashboard do avaliador
- **EvaluationFormView**: Formulário de avaliação
- **ChangePasswordView**: Alteração de senha

## Instalação e Execução

### Com Docker

1. **Execute com Docker Compose**
```bash
docker-compose up frontend
```

2. **Acesse a aplicação**
- **Frontend**: http://localhost:4173

## Build e Deploy

### Build de Produção
```bash
npm run build
```

### Preview do Build
```bash
npm run preview
```

### Deploy
```bash
npm run build
```

## Funcionalidades por Tipo de Usuário

### Administrador
- **Dashboard**: Visão geral do sistema
- **Gestão de Usuários**: CRUD completo de avaliadores
- **Gestão de Trabalhos**: Importação CSV, edição, remoção
- **Distribuição**: Algoritmo automático de distribuição
- **Monitoramento**: Acompanhamento em tempo real
- **Pódio**: Geração de rankings
- **Processamento de Fichas**: IA para extrair notas

### Avaliador
- **Dashboard**: Trabalhos atribuídos
- **Avaliação**: Formulário com 5 critérios
- **Histórico**: Avaliações realizadas
- **Perfil**: Alteração de senha
