#!/bin/bash

echo "Iniciando Sistema de Avaliação com Docker..."

if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker não está rodando."
    exit 1
fi

if [ ! -f .env ]; then
    echo "❌ Arquivo .env não encontrado!"
    exit 1
fi

echo "🛑 Parando containers existentes..."
docker-compose down

echo "🔨 Construindo e iniciando containers..."
docker-compose up --build -d

echo "⏳ Aguardando serviços inicializarem..."
sleep 20

echo "📊 Status dos containers:"
docker-compose ps

echo ""
echo "🎉 Sistema iniciado com sucesso!"
echo ""
echo "📱 Serviços:"
echo "   Frontend: http://localhost"
echo "   Backend API: http://localhost/api/v1"
echo "   Documentação Swagger: http://localhost/api/v1/docs"
echo "   Adminer (DB): http://localhost:8080"
echo ""
echo "🔍 Verificar logs:"
echo "   Todos: docker-compose logs -f"
echo "   Nginx: docker-compose logs -f nginx"
echo "   Backend: docker-compose logs -f backend"
echo "   Frontend: docker-compose logs -f frontend"
echo ""
echo "🛑 Parar sistema: docker-compose down"
echo "🔄 Reiniciar Nginx: docker-compose restart nginx"
