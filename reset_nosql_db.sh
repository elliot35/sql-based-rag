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

# Wait for MongoDB to be ready
# echo "Waiting for MongoDB to be ready..."
# until docker-compose $PROFILE run --rm mongodb mongosh --eval "db.adminCommand('ping')" > /dev/null 2>&1; do
#     echo "Still waiting for MongoDB..."
#     sleep 2
# done

echo "Resetting MongoDB database..."

# Step 1: Clean up existing data
echo "Step 1: Cleaning up existing data..."
docker-compose $PROFILE run --rm $BACKEND_SERVICE python -m backend.database.nosql.mock.cleanup_mongodb

# Step 2: Set up indexes
echo "Step 2: Setting up indexes..."
docker-compose $PROFILE run --rm $BACKEND_SERVICE python -m backend.database.nosql.mock.setup_mongodb

# Step 3: Populate knowledge base
echo "Step 3: Populating knowledge base..."
docker-compose $PROFILE run --rm $BACKEND_SERVICE python -m backend.database.nosql.mock.battery_knowledge

echo "MongoDB database reset completed successfully!" 