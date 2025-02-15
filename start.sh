#!/bin/bash

set -a
source .env
set +a

if [ "$LLM_PROVIDER" = "local" ]; then
    export BACKEND_SERVICE=backend-gpu
    echo "Starting services with GPU-enabled backend..."
    docker-compose --profile local up -d
else
    export BACKEND_SERVICE=backend
    echo "Starting services with OpenAI backend..."
    docker-compose --profile openai up -d
fi 