#!/bin/bash

# Source the .env file to get LLM_PROVIDER
set -a
source .env
set +a

BACKEND_SERVICE=backend
PROFILE="--profile openai"
if [ "$LLM_PROVIDER" = "local" ]; then
    BACKEND_SERVICE=backend-gpu
    PROFILE="--profile local"
fi

echo "Resetting database..."

echo "Step 1: Cleaning up existing tables..."
docker-compose $PROFILE run --rm $BACKEND_SERVICE cleanup-db

echo "Step 2: Creating new tables..."
docker-compose $PROFILE run --rm $BACKEND_SERVICE setup-tables

echo "Step 3: Generating mock data..."
docker-compose $PROFILE run --rm $BACKEND_SERVICE generate-mock-data

echo "Database reset completed successfully!" 