#!/bin/bash

echo "Setting up database tables..."
docker-compose run --rm backend setup-tables

echo "Generating mock data..."
docker-compose run --rm backend generate-mock-data

echo "Database setup complete!" 