# Development Guide

This guide provides information for developers working on the Pharmacy Inventory API project.

## Table of Contents
1. [Development Setup](#development-setup)
2. [Project Structure](#project-structure)
3. [Coding Standards](#coding-standards)
4. [Testing](#testing)
5. [API Versioning](#api-versioning)
6. [Database Migrations](#database-migrations)
7. [Environment Configuration](#environment-configuration)
8. [Deployment](#deployment)
9. [Troubleshooting](#troubleshooting)

## Development Setup

### Prerequisites
- Python 3.8+
- pip (Python package manager)
- Git
- SQLite (for development)
- PostgreSQL (for production)

### Setup Instructions

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd Pharmacy_Inventory_API
   ```

2. **Create and activate a virtual environment**
   ```bash
   # Windows
   python -m venv venv
   .\venv\Scripts\activate
   
   # macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

5. **Run migrations**
   ```bash
   python manage.py migrate
   ```

6. **Create a superuser**
   ```bash
   python manage.py createsuperuser
   ```

7. **Run the development server**
   ```bash
   python manage.py runserver
   ```

## Project Structure

```
Pharmacy_Inventory_API/
├── core/                  # Core functionality
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings/          # Split settings for different environments
│   │   ├── __init__.py
│   │   ├── base.py       # Base settings
│   │   ├── dev.py        # Development settings
│   │   └── prod.py       # Production settings
│   ├── urls.py
│   └── wsgi.py
├── medicines/            # Medicines app
│   ├── migrations/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── serializers.py
│   ├── tests/
│   │   ├── __init__.py
│   │   ├── test_models.py
│   │   ├── test_views.py
│   │   └── factories.py
│   └── views.py
├── .env.example
├── .gitignore
├── manage.py
├── requirements/
│   ├── base.txt         # Core requirements
│   ├── dev.txt          # Development requirements
│   └── prod.txt         # Production requirements
└── requirements.txt     # Pinned dependencies
```

## Coding Standards

### Python
- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) style guide
- Use docstrings for all public modules, functions, classes, and methods
- Keep lines under 88 characters (PEP 8)
- Use type hints for better code documentation

### Django
- Follow [Django's coding style](https://docs.djangoproject.com/en/dev/internals/contributing/writing-code/coding-style/)
- Use class-based views where appropriate
- Keep views thin, move business logic to models or services
- Use Django's built-in decorators for common functionality

### Git
- Write clear, concise commit messages
- Use feature branches for new features (`feature/feature-name`)
- Create pull requests for code review
- Keep commits atomic and focused

## Testing

### Running Tests
```bash
# Run all tests
pytest

# Run tests with coverage
pytest --cov=.

# Run a specific test file
pytest medicines/tests/test_views.py

# Run a specific test
pytest medicines/tests/test_views.py::TestMedicineViewSet::test_list_medicines
```

### Writing Tests
- Write unit tests for models and utility functions
- Write integration tests for API endpoints
- Use factories for test data (e.g., `factory_boy`)
- Aim for good test coverage (>80%)

## API Versioning

The API uses URL-based versioning. Example:
```
/api/v1/medicines/
```

To create a new API version:
1. Create a new version directory in the app
2. Copy and update the necessary files
3. Update the URL routing

## Database Migrations

### Creating Migrations
```bash
# Create a new migration
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Check migration status
python manage.py showmigrations
```

### Migration Best Practices
- Always test migrations on a copy of production data
- Keep migrations small and focused
- Never edit migrations after they've been committed
- Use `RunPython` for complex data migrations

## Environment Configuration

### Required Environment Variables
```
# Django
SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database
DATABASE_URL=sqlite:///db.sqlite3

# Email
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
DEFAULT_FROM_EMAIL=noreply@example.com

# JWT
JWT_SECRET_KEY=your-jwt-secret
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_LIFETIME=3600  # 1 hour
JWT_REFRESH_TOKEN_LIFETIME=2592000  # 30 days
```

## Deployment

### Production Checklist
- [ ] Set `DEBUG=False`
- [ ] Configure a production database (PostgreSQL)
- [ ] Set up proper logging
- [ ] Configure static files
- [ ] Set up HTTPS
- [ ] Configure CORS
- [ ] Set up monitoring
- [ ] Configure backups

### Deployment Steps
1. Set up a production server (e.g., Ubuntu, Nginx, Gunicorn)
2. Clone the repository
3. Install dependencies
4. Configure environment variables
5. Run migrations
6. Collect static files
7. Set up a process manager (e.g., systemd, Supervisor)
8. Configure the web server (Nginx/Apache)

## Troubleshooting

### Common Issues

#### Database Connection Issues
- Verify database credentials in `.env`
- Ensure the database server is running
- Check database user permissions

#### Migration Problems
- Check for unapplied migrations
- Look for migration conflicts
- Try resetting the database (development only)

#### API Authentication Issues
- Verify JWT token is valid and not expired
- Check token in the Authorization header
- Ensure the user has the required permissions

### Getting Help
- Check the logs in `logs/`
- Search the issue tracker
- Ask for help in the project's communication channel
