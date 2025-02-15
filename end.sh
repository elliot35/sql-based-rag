#!/bin/bash

# Source the .env file to get LLM_PROVIDER
set -a
source .env
set +a

# Determine which profile to use
if [ "$LLM_PROVIDER" = "local" ]; then
    PROFILE="--profile local"
    BACKEND_SERVICE="backend-gpu"
else
    PROFILE="--profile openai"
    BACKEND_SERVICE="backend"
fi

echo "🛑 Stopping all containers..."
docker-compose $PROFILE down

echo "🗑️ Removing all volumes..."
docker-compose $PROFILE down -v

echo "🧹 Removing all related images..."
# Remove backend images (both GPU and non-GPU versions)
docker rmi $(docker images | grep "${BACKEND_SERVICE}" | awk '{print $3}') 2>/dev/null || true
# Remove frontend image
docker rmi $(docker images | grep 'smart-battery-storage-knowledge-rag_frontend' | awk '{print $3}') 2>/dev/null || true

echo "🧼 Cleaning up unused volumes..."
docker volume prune -f

echo "🧼 Cleaning up unused networks..."
docker network prune -f

echo "✨ Cleanup complete! The environment has been completely reset."
echo "To restart the services, run: ./start.sh" 