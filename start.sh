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
sleep 15

echo "📊 Status dos containers:"
docker-compose ps

echo ""
echo "🎉 Sistema iniciado com sucesso!"
echo ""
echo "📱 Serviços:"
echo "   Frontend: http://localhost:4173"
echo "   Backend API: http://localhost:5000"
echo "   Adminer: http://localhost:8080"
echo ""
echo "📝 Logs: docker-compose logs -f"
echo "🛑 Parar: docker-compose down"
