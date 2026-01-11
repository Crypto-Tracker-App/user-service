# User Service

User authentication and management microservice for the Azure Crypto Tracker Application.

## Overview

The User Service is a Flask-based microservice responsible for handling user authentication, JWT token management, and user-related operations within the Crypto Tracker platform. It provides REST API endpoints for user registration, login, and authentication verification.

## Features

- User authentication with JWT (JSON Web Tokens)
- Session-based security
- Health check endpoint
- Swagger/OpenAPI documentation
- Containerized deployment with Docker
- Automated CI/CD with GitHub Actions

## Prerequisites

- Python 3.12 or higher
- pip (Python package manager)
- Docker (for containerized deployment)
- Virtual environment (recommended)

## Installation

### Local Development Setup

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd user-service
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables:**
   Create a `.env` file in the root directory with necessary configuration:
   ```bash
   FLASK_ENV=development
   FLASK_APP=wsgi.py
   ```

## Running the Application

### Development Server

```bash
python wsgi.py
```

The application will be available at `http://localhost:5000`

### Using Docker

1. **Build the Docker image:**
   ```bash
   docker build -t user-service:latest .
   ```

2. **Run the container:**
   ```bash
   docker run -p 5000:5000 user-service:latest
   ```

## Testing

Run the test suite using pytest:

```bash
pytest
```

For coverage report:

```bash
pytest --cov=app --cov-report=html
```

## API Documentation

The API is fully documented with Swagger/OpenAPI. Once the application is running, access the interactive API documentation at:

- **Swagger UI:** `http://localhost:5000/apidocs/`
- **OpenAPI JSON:** `http://localhost:5000/apispec.json`

## Endpoints

### Authentication
- `POST /api/auth/login` - User login
- `POST /api/auth/register` - User registration
- `GET /api/auth/verify` - Verify JWT token

### Health
- `GET /health` - Health check endpoint

## Project Structure

```
user-service/
├── app/
│   ├── __init__.py           # Flask application factory
│   ├── config.py             # Configuration management
│   ├── extensions.py         # Flask extensions
│   ├── models.py             # Database models
│   ├── api/                  # API routes
│   │   ├── auth.py          # Authentication endpoints
│   │   └── health.py        # Health check endpoint
│   ├── middleware/           # Custom middleware
│   │   └── auth_middleware.py
│   ├── services/             # Business logic
│   │   ├── auth_service.py
│   │   ├── auth_utils.py
│   │   └── jwt_service.py
│   └── utils/                # Utility functions
│       └── resilience.py
├── tests/                    # Unit and integration tests
├── Dockerfile                # Docker configuration
├── requirements.txt          # Python dependencies
├── wsgi.py                   # WSGI entry point
└── pytest.ini                # Pytest configuration
```

## Deployment

### Azure Kubernetes Service (AKS)

This service is deployed on AKS using Kubernetes manifests. The CI/CD pipeline automatically:

1. Runs tests on code push
2. Builds and pushes Docker images to Azure Container Registry (cryptotracker.azurecr.io)
3. Updates the AKS deployment with the new image

### Manual Deployment

Deploy using kubectl:

```bash
kubectl apply -f k8s/
kubectl rollout restart deployment/user-service -n default
```

## Configuration

Configuration is managed through the `app/config.py` file. Key settings include:

- Flask environment (development/production)
- Database connection details
- JWT secret key and expiration
- Logging configuration

## Contributing

1. Ensure all tests pass: `pytest`
2. Follow PEP 8 style guidelines
3. Add tests for new features
4. Update documentation as needed

## Troubleshooting

### Common Issues

**Port already in use:**
```bash
# Change the port in wsgi.py or use environment variable
python wsgi.py --port 5001
```

**Database connection errors:**
- Verify database credentials in configuration
- Check database connectivity and availability

**JWT token issues:**
- Ensure JWT secret key is configured correctly
- Verify token expiration settings

## License

This project is part of the Azure Crypto Tracker Application.

## Support

For issues or questions, please contact the development team or create an issue in the repository.
