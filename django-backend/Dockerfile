FROM python:3.12

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && \
    apt-get install -y postgresql-client netcat-traditional && \
    pip install --upgrade pip && \
    pip install pipenv && \
    pip install websockets uvicorn[standard]

COPY Pipfile ./

# Generate fresh Pipfile.lock and install dependencies
RUN pipenv lock && \
    pipenv install --system --deploy

# Create necessary directories
RUN mkdir -p /app/api/documents

# Copy project
COPY . .

COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

# Ensure documents directory exists and has correct permissions
RUN chmod -R 755 /app/api/documents

# Set the entrypoint
ENTRYPOINT ["/app/entrypoint.sh"]
