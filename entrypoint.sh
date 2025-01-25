#!/bin/bash

if [ "$DEBUG" = "True" ]; then
    echo "checking the environment variables..."
    printenv
fi

echo "Running Alembic migrations..."
poetry run alembic upgrade head

echo "Starting the application..."
poetry run uvicorn main:app --host 0.0.0.0 --port 8000
