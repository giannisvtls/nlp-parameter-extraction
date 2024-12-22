# AI-Powered Real-Time Chat Analytics

A full-stack application that provides real-time chat analysis using OpenAI's API to extract meaningful parameters from messages and perform dynamic SQL queries. The system utilizes WebSocket connections for instant communication between the frontend and backend.

## 🏗️ Architecture

- **Frontend**: React application with real-time WebSocket communication
- **Backend**: Django with Channels for WebSocket support
- **Database**: PostgreSQL for data storage
- **Cache**: Redis for WebSocket channel layers and caching
- **AI Integration**: OpenAI API for message parameter extraction

## 🚀 Features

- Real-time chat interface
- Automatic parameter extraction from messages using OpenAI
- Dynamic SQL query generation based on extracted parameters
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

2. Create a `.env` file in the root directory with your OpenAI API key:
```bash
OPENAI_API_KEY=your_api_key_here
```

3. Start the application:
```bash
docker-compose up --build
```

4. Access the application:
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
├── django-backend/         # Django backend application
├── react-frontend/        # React frontend application
├── docker-compose.yml     # Docker composition configuration
└── README.md             # This file
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
