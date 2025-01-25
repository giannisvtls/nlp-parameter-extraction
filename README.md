# Description

A full-stack application that provides real-time chat analysis using OpenAI's API with Retrieval Augmented Generation (RAG) capabilities. The system utilizes WebSocket connections for instant communication between the frontend and backend, and includes intelligent document-based responses for banking-related queries.

## 🏗️ Architecture

- **Frontend**: React application with real-time WebSocket communication
- **Backend**: Django with Channels for WebSocket support
- **Database**: PostgreSQL for data storage
- **Cache**: Redis for WebSocket channel layers and caching
- **AI Integration**: OpenAI API for message parameter extraction

## 🚀 Features

- Real-time chat interface with WebSocket communication
- Intelligent responses using RAG with banking domain knowledge
- Document-based context retrieval for accurate responses
- Instant results display through WebSocket connection
- Scalable architecture with Docker containerization

## 🛠️ Tech Stack

- **Frontend**:
  - React
  - Vite
  - WebSocket client
  
- **Backend**:
  - Django
  - Django Channels
  - OpenAI API
  - PostgreSQL
  - Redis
  
- **DevOps**:
  - Docker
  - Docker Compose

## 📋 Prerequisites

- Docker and Docker Compose
- OpenAI API key

## 🚦 Getting Started

1. Clone the repository:
```bash
git clone [repository-url]
cd [repository-name]
```

2. In docker-compose.yml add your OpenAI API-KEY:
```bash
OPENAI_API_KEY=your_api_key_here
```

3. Start the application:
```bash
docker-compose up --build
```

4. Add documents to the RAG system:
```bash
# Add a document to the system (supports multiple categories: guide, faq, troubleshooting)
curl -X POST http://localhost:8000/api/documents/add_with_embedding/ \
  -H "Content-Type: application/json" \
  -d '{
    "content": "Your document content here",
  }'

# You can add multiple documents for comprehensive coverage:
# - Banking FAQs (category: faq)
# - Troubleshooting guides (category: troubleshooting)
# - General guides (category: guide)
```

5. Access the application:
- Frontend: http://localhost:5173
- Backend API: http://localhost:8000/api
- API Documentation: http://localhost:8000/docs (when DEV_DOCS=true)

## 🔧 Configuration

### Environment Variables

#### Backend
- `SECRET_KEY`: Django secret key
- `DB_NAME`: PostgreSQL database name
- `DB_USER`: Database user
- `DB_PASS`: Database password
- `DB_HOST`: Database host
- `DB_PORT`: Database port
- `REDIS_HOST`: Redis host
- `REDIS_PORT`: Redis port
- `DJANGO_LOG_LEVEL`: Logging level
- `DEV_DOCS`: Enable/disable API documentation

#### Frontend
- `VITE_API_URL`: Backend API URL
- `VITE_WS_URL`: WebSocket URL

## 🔍 Project Structure

```
.
├── django-backend/           # Django backend application
│   ├── api/                 # API implementation
│   │   ├── documents/       # Banking domain documents
│   │   ├── services/        # Business logic services
│   │   ├── tests/          # Test suites
│   │   └── ...
│   └── ...
├── react-frontend/          # React frontend application
│   ├── src/
│   │   ├── components/     # React components
│   │   ├── screens/        # Application screens
│   │   ├── store/          # Redux store and API
│   │   └── ...
│   └── ...
├── docker-compose.yml       # Docker composition configuration
├── railway.toml            # Railway deployment configuration
├── render.yaml             # Render deployment configuration
└── README.md               # This file
```

## 📝 Development

### Code Style
The project follows standard code style guidelines:
- Backend: PEP 8
- Frontend: ESLint with Airbnb configuration

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👥 Authors

- [GEORGE PARNALIS-PALANTZIDHS] - *TBD*
- [ELENH TRAXANIDOY] - *TBD*
- [IOANNIS VITALIS] - *Frontend/Backend bootstrapping and websocket connection*
