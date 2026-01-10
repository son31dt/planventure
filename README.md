# Planventure API 🚁

[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/github-samples/planventure)

A Flask-based REST API backend for the Planventure application - a comprehensive trip planning platform that helps users organize, manage, and track their travel adventures.

## 📋 Overview

PlanVenture API is a production-ready RESTful web service built with Flask and SQLAlchemy that provides:

- **User Authentication**: Secure JWT-based authentication with bcrypt password hashing
- **Trip Management**: Complete CRUD operations for managing travel plans
- **Itinerary Planning**: Auto-generated day-by-day itinerary templates
- **Trip Organization**: Filter trips by status, pagination support, and upcoming trip tracking
- **Data Validation**: Comprehensive input validation and error handling
- **CORS Support**: Configured for seamless integration with React/Vue frontends
- **Logging**: Built-in logging for debugging and monitoring
- **Database Flexibility**: Support for SQLite, PostgreSQL, and MySQL

## 🏗️ Architecture

The API follows a modular, layered architecture:

```
planventure-api/
├── app.py                 # Flask application entry point
├── models/                # SQLAlchemy database models
│   ├── __init__.py       # Database initialization
│   ├── user.py           # User model with authentication
│   └── trip.py           # Trip model with relationships
├── routes/                # API endpoint blueprints
│   ├── __init__.py       # Blueprint registration
│   ├── auth.py           # Authentication routes
│   └── trips.py          # Trip management routes
├── middleware.py          # Authentication decorators
├── utils.py              # Utility functions (hashing, JWT, validation)
├── exceptions.py         # Custom exception classes
├── error_handler.py      # Error response formatting
├── cors_config.py        # CORS configuration management
└── requirements.txt      # Python dependencies
```

## 🔑 Key Features

### Authentication System
- User registration with email validation and password strength requirements
- Secure login with JWT token generation
- Access tokens (24-hour expiration) and refresh tokens (30-day expiration)
- Password hashing with bcrypt and automatic salt generation

### Trip Management
- Create, read, update, and delete trips
- Automatic itinerary template generation based on trip dates
- Trip status tracking (planning, confirmed, completed, cancelled)
- Geolocation support (latitude/longitude storage)
- Custom notes and trip details

### Data Models

**User Model:**
- Unique username and email
- Hashed password storage
- Profile information (full name)
- Active status tracking
- Timestamps (created_at, updated_at)

**Trip Model:**
- User relationship (one-to-many)
- Destination and date range
- Geolocation coordinates
- JSON-based itinerary storage
- Status and notes
- Duplicate prevention (unique constraint)

### API Endpoints

#### Authentication (`/api/auth`)
- `POST /api/auth/register` - Create new user account
- `POST /api/auth/login` - Authenticate user and get tokens
- `POST /api/auth/validate-email` - Check email availability

#### Trips (`/api/trips`)
- `GET /api/trips` - List user's trips (with pagination)
- `POST /api/trips` - Create new trip
- `GET /api/trips/<id>` - Get trip details
- `PUT /api/trips/<id>` - Update trip
- `DELETE /api/trips/<id>` - Delete trip
- `GET /api/trips/upcoming` - Get upcoming trips

### Middleware & Security
- `@token_required` - Validates JWT for protected routes
- `@user_required` - Fetches user object from database
- `@optional_auth` - Allows both authenticated and unauthenticated access
- `@admin_required` - Admin-only route protection

## Prerequisites
Before you begin, ensure you have the following:

- A GitHub account - [sign up for FREE](https://github.com)
- Access to GitHub Copilot - [sign up for FREE](https://gh.io/gfb-copilot)!
- A Code Editor - [VS Code](https://code.visualstudio.com/download) is recommended
- API Client (like [Bruno](https://github.com/usebruno/bruno))
- Git - [Download & Install Git](https://git-scm.com/downloads)
- Python 3.8 or higher

## 🚀 Getting Started

### Build along in a Codespace

1. Click the "Open in GitHub Codespaces" button above to start developing in a GitHub Codespace.

### Local Development Setup

If you prefer to develop locally, follow the steps below:

1. Fork and clone the repository and navigate to the [planventure-api](/planventure-api/) directory:
```sh
cd planventure-api
```

2. Create a virtual environment and activate it:
```sh
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install the required dependencies:
```sh
pip install -r requirements.txt
```

4. Create an `.env` file based on [.env.example](/planventure-api/.env.example):
```sh
cp .env.example .env
```

Edit the `.env` file and add your configuration:
```env
SECRET_KEY=your-secret-key-here-change-in-production
FLASK_ENV=development
FLASK_DEBUG=True
DATABASE_URL=sqlite:///planventure.db
CORS_ORIGINS=http://localhost:3000,http://localhost:5173
```

5. Initialize the database:
```sh
python create_db.py
```

6. Start the Flask development server:
```sh
flask run
```

The API will be available at `http://localhost:5000`

## 📚 API Endpoints

### Core Endpoints
- `GET /` - Welcome message
- `GET /health` - Health check endpoint

### Example Requests

**Register a new user:**
```json
POST /api/auth/register
Content-Type: application/json

{
  "username": "john_doe",
  "email": "john@example.com",
  "password": "SecurePass123",
  "full_name": "John Doe"
}
```

**Login:**
```json
POST /api/auth/login
Content-Type: application/json

{
  "email": "john@example.com",
  "password": "SecurePass123"
}
```

**Create a trip:**
```json
POST /api/trips
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "destination": "Paris, France",
  "start_date": "2026-06-01",
  "end_date": "2026-06-15",
  "latitude": 48.8566,
  "longitude": 2.3522,
  "notes": "Summer vacation",
  "status": "planning"
}
```

## 🛠️ Technology Stack

- **Framework**: Flask 3.0.0
- **Database ORM**: SQLAlchemy 2.0.23
- **Authentication**: PyJWT 2.8.0
- **Password Hashing**: bcrypt 4.1.2
- **CORS**: flask-cors 4.0.0
- **Validation**: marshmallow 3.20.1
- **Database Support**: SQLite, PostgreSQL, MySQL

## 📊 Database Schema

The database includes:
- `users` table - User accounts and authentication
- `trips` table - Trip information with user relationship
- Proper indexing on frequently queried columns
- Unique constraints to prevent duplicate data
- Foreign key relationships for data integrity

## 🔒 Security Features

- JWT token-based authentication
- Bcrypt password hashing with automatic salt
- Email validation on registration
- Password strength requirements
- CORS configuration for production domains
- Error handling without exposing sensitive information
- SQL injection prevention through SQLAlchemy ORM
- Request validation and sanitization

## 🧪 Testing

Use [Bruno](https://github.com/usebruno/bruno) or similar API clients to test endpoints:

1. Test health check: `GET http://localhost:5000/health`
2. Register user: Use the auth register endpoint
3. Login: Get JWT tokens
4. Create trip: Use token in Authorization header
5. Manage trips: Use CRUD operations

## 📝 Environment Variables

Configure these variables in your `.env` file:

```env
# Flask Configuration
SECRET_KEY=your-secret-key-here-change-in-production
FLASK_ENV=development
FLASK_DEBUG=True

# Database Configuration
DATABASE_URL=sqlite:///planventure.db
# For PostgreSQL: postgresql://user:password@localhost:5432/planventure
# For MySQL: mysql+pymysql://user:password@localhost:3306/planventure

# CORS Configuration
CORS_ORIGINS=http://localhost:3000,http://localhost:5173,http://127.0.0.1:3000,http://127.0.0.1:5173

# API Configuration
API_HOST=0.0.0.0
API_PORT=5000
```

## 🚀 Deployment

To deploy to production:

1. Set `FLASK_ENV=production`
2. Generate a strong `SECRET_KEY`
3. Use a production database (PostgreSQL recommended)
4. Configure `CORS_ORIGINS` with your frontend domain
5. Use a production WSGI server (Gunicorn, uWSGI)
6. Set up SSL/TLS certificates
7. Enable logging and monitoring

## 📖 Documentation

- See [PROMPTS.md](/planventure-api/PROMPTS.md) for step-by-step development guide
- API documentation available via endpoints
- Comprehensive docstrings in all functions

## 🤝 Contributing

See [CODE_OF_CONDUCT.md](/CODE_OF_CONDUCT.md) for community guidelines.

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

For issues and questions, see [SUPPORT.md](/SUPPORT.md) for resources and community guidelines.