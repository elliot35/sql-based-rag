#!/bin/bash

if [ "$1" = "setup-tables" ]; then
    python -m backend.database.db_mock.setup_tables
elif [ "$1" = "generate-mock-data" ]; then
    python -m backend.database.db_mock.generate_mock_data
elif [ "$1" = "cleanup-db" ]; then
    python -m backend.database.db_mock.cleanup_db
else
    exec "$@"
fi 