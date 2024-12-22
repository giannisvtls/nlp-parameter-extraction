FROM python:3.12

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && \
    apt-get install -y postgresql-client netcat-traditional && \
    pip install --upgrade pip && \
    pip install pipenv

# Copy dependency files
COPY Pipfile Pipfile.lock ./

# Install dependencies
RUN pipenv install --system --deploy

# Copy project
COPY . .

# Make the entrypoint script executable
COPY entrypoint.sh .
RUN chmod +x entrypoint.sh

# Set the entrypoint
ENTRYPOINT ["./entrypoint.sh"]