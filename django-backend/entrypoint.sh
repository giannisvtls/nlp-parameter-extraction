#!/bin/bash

# Function to wait for a service
wait_for_service() {
    local host=$1
    local port=$2
    local service=$3
   
    echo "Waiting for $service..."
    if [ "$service" = "PostgreSQL" ]; then
        until pg_isready -h $host -p $port -U postgres >/dev/null 2>&1; do
            sleep 1
        done
    elif [ "$service" = "Redis" ]; then
        until echo "PING" | nc -w 1 $host $port | grep -q "PONG"; do
            sleep 1
        done
    fi
    echo "$service started"
}

# Wait for required services
wait_for_service db 5432 "PostgreSQL"
wait_for_service redis 6379 "Redis"

# Create database if it doesn't exist
echo "Creating database if it doesn't exist..."
PGPASSWORD=$DB_PASS psql -h db -U $DB_USER -tc "SELECT 1 FROM pg_database WHERE datname = '$DB_NAME'" | grep -q 1 || \
    PGPASSWORD=$DB_PASS psql -h db -U $DB_USER -c "CREATE DATABASE $DB_NAME"

# Wait a bit for database to be created
sleep 5

# Apply database migrations
echo "Applying database migrations..."
python manage.py migrate

# Start uvicorn with hot reload
echo "Starting uvicorn server..."
uvicorn app.asgi:application \
    --host 0.0.0.0 \
    --port 8000 \
    --reload \
    --reload-dir . \
    --ws websockets