#!/bin/bash

# Amazon ETL Docker Runner Script

set -e

echo "🐳 Amazon ETL Docker Setup"
echo "=========================="

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker Desktop first."
    echo "   Run: open -a Docker"
    exit 1
fi

echo "✅ Docker is running"

# Function to show usage
show_usage() {
    echo "Usage: $0 [COMMAND]"
    echo ""
    echo "Commands:"
    echo "  build     Build the Docker images"
    echo "  up        Start all services"
    echo "  down      Stop all services"
    echo "  logs      Show logs from all services"
    echo "  etl       Run only the Amazon ETL process"
    echo "  nyc       Run only the NYC Taxi ETL process (Docker)"
    echo "  nyc-local Run NYC Taxi ETL directly on host"
    echo "  finnhub   Run Finnhub stock ETL to Elasticsearch"
    echo "  clean     Remove all containers and volumes"
    echo "  status    Show status of all services"
    echo ""
}

# Parse command line arguments
case "${1:-up}" in
    "build")
        echo "🔨 Building Docker images..."
        docker-compose build
        ;;
    "up")
        echo "🚀 Starting all services..."
        docker-compose up --build -d
        echo ""
        echo "✅ Services started!"
        echo "📊 Grafana: http://localhost:3001 (Swami123/Swami@123)"
        echo "🗄️  PostgreSQL: localhost:5433 (sravya/Swami@123)"
        echo ""
        echo "📋 To view logs: ./run.sh logs"
        echo "🛑 To stop: ./run.sh down"
        ;;
    "down")
        echo "🛑 Stopping all services..."
        docker-compose down
        ;;
    "logs")
        echo "📋 Showing logs..."
        docker-compose logs -f
        ;;
    "etl")
        echo "⚙️  Running Amazon ETL process only..."
        docker-compose up --build etl
        ;;
    "nyc")
        echo "🚕 Running NYC Taxi ETL process only (Docker)..."
        docker-compose up --build nyc_taxi_etl
        ;;
    "nyc-local")
        echo "🚕 Running NYC Taxi ETL directly on host..."
        python etl/nyc_taxi_etl.py
        ;;
    "finnhub")
        echo "📈 Running Finnhub Stock ETL to Elasticsearch..."
        python etl/finnhub_etl_elasticsearch.py
        ;;
    "clean")
        echo "🧹 Cleaning up containers and volumes..."
        docker-compose down -v
        docker system prune -f
        ;;
    "status")
        echo "📊 Service status:"
        docker-compose ps
        ;;
    "help"|"-h"|"--help")
        show_usage
        ;;
    *)
        echo "❌ Unknown command: $1"
        show_usage
        exit 1
        ;;
esac
