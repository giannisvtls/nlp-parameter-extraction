#!/bin/bash
# Wait for postgres
echo "Waiting for PostgreSQL..."
while ! nc -z db 5432; do
  sleep 0.1
done
echo "PostgreSQL started"

# Wait for Redis
echo "Waiting for Redis..."
while ! nc -z redis 6379; do
  sleep 0.1
done
echo "Redis started"

# Create database if it doesn't exist
echo "Creating database if it doesn't exist..."
PGPASSWORD=$POSTGRES_PASSWORD psql -h db -U $POSTGRES_USER -tc "SELECT 1 FROM pg_database WHERE datname = '$POSTGRES_DB'" | grep -q 1 || PGPASSWORD=$POSTGRES_PASSWORD psql -h db -U $POSTGRES_USER -c "CREATE DATABASE $POSTGRES_DB"

# Wait a bit for database to be created
sleep 2

# Apply database migrations
echo "Applying database migrations..."
python manage.py migrate

# Start server using Daphne
echo "Starting server with Daphne..."
daphne -b 0.0.0.0 -p 8000 app.asgi:application