#!/bin/bash

set -a
source .env
set +a

BACKEND_SERVICE=backend
PROFILE="--profile openai"
if [ "$LLM_PROVIDER" = "local" ]; then
    BACKEND_SERVICE=backend-gpu
    PROFILE="--profile local"
fi

echo "Cleaning up database..."
docker-compose $PROFILE run --rm $BACKEND_SERVICE cleanup-db

echo "Database cleanup complete!" 