#!/bin/bash
# Wait for the database to be ready
sleep 5

# Run migrations
alembic upgrade head

# Start the application
uvicorn app.main:app --host 0.0.0.0 --port 8000 