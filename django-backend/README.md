# AI-Enhanced Django Backend

A Django backend service that provides WebSocket communication for real-time chat analysis using OpenAI's API, with PostgreSQL for data storage and Redis for WebSocket channel layers.

## 🔑 Key Features

- WebSocket integration using Django Channels
- Real-time message processing with OpenAI API
- Dynamic SQL query generation
- RESTful API endpoints
- PostgreSQL database integration
- Redis for WebSocket channel layers
- OpenAPI documentation

## 🛠️ Tech Stack

- Django
- Django Channels
- OpenAI API
- PostgreSQL
- Redis
- Swagger/OpenAPI

## 📋 Requirements

- Python >=3.12
- PostgreSQL
- Redis
- OpenAI API Key

## 🚀 Running the Project

### Local Development Setup

1. Create a virtual environment:
```bash
pipenv shell
```

2. Install dependencies:
```bash
pipenv install
```

3. Create PostgreSQL database:
```sql
CREATE DATABASE efo_db;
```

4. Configure environment variables:
   - Copy `.env.sample` to `.env`
   - Fill in required variables:
     ```
     SECRET_KEY=your_secret_key
     DB_NAME=efo_db
     DB_USER=postgres
     DB_PASS=postgres
     DB_HOST=localhost
     DB_PORT=5432
     REDIS_HOST=localhost
     REDIS_PORT=6379
     OPENAI_API_KEY=your_api_key
     ```

5. Apply migrations:
```bash
python manage.py migrate
```

6. Start the development server:
```bash
python manage.py runserver
```

### Docker Setup

The backend can also be run using Docker:

```bash
docker-compose up backend
```

## 🔌 WebSocket Endpoints

- Chat Connection: `ws://localhost:8000/ws/chat/`

### Message Format
```json
{
    "type": "message",
    "content": "your message here"
}
```

## 🌐 API Documentation

Access the OpenAPI documentation at:
- Local: http://localhost:8000/api/docs
- Docker: http://localhost:8000/api/docs

## 📝 Development Guidelines

### Code Style
- Follow PEP 8 guidelines
- Use Django's coding style
- Type hints for Python functions

## 🔧 Project Structure

```
django-backend/
├── api/                  # API application
│   ├── migrations/      # Database migrations
│   ├── serializers/     # API serializers
│   │   ├── api.py
│   │   └── metadata.py
│   ├── templates/       # API templates
│   │   └── swagger-ui.html
│   ├── admin.py        # Admin interface configuration
│   ├── apps.py         # App configuration
│   ├── consumers.py    # WebSocket consumers
│   ├── models.py       # Database models
│   ├── routing.py      # WebSocket routing
│   ├── test.py         # Test files
│   ├── urls.py         # URL configurations
│   └── views.py        # API views
├── app/                 # Core application
├── .dockerignore       # Docker ignore file
├── .env.docker         # Docker environment variables
├── .env.sample         # Sample environment file
├── .gitignore         # Git ignore file
├── Dockerfile         # Docker configuration
├── entrypoint.sh      # Docker entrypoint script
├── manage.py          # Django management script
├── Pipfile           # Pipenv dependencies
├── Pipfile.lock      # Pipenv lock file
└── README.md         # Project documentation
```

## 📄 License

This project is licensed under the MIT License.
