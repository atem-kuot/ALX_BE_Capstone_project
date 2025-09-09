<div align="center">
  <h1>🏥 Pharmacy Inventory Management System</h1>
  <p>Modern, scalable, and secure RESTful API for managing pharmacy inventory, prescriptions, and healthcare operations</p>
  
  [![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
  [![Django](https://img.shields.io/badge/Django-4.2-brightgreen.svg)](https://www.djangoproject.com/)
  [![DRF](https://img.shields.io/badge/DRF-3.14.0-red.svg)](https://www.django-rest-framework.org/)
  [![SQLite](https://img.shields.io/badge/SQLite-3.36+-blue.svg)](https://www.sqlite.org/)
  [![Docker](https://img.shields.io/badge/Docker-20.10+-blue.svg)](https://www.docker.com/)
  [![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
  [![Code Style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
  
</div>

## ✨ Key Features

### 📦 Advanced Inventory Management
- Real-time stock monitoring with automated alerts
- Batch and expiry tracking with proactive notifications
- Supplier management with performance metrics
- Intelligent automated reordering system
- Barcode/QR code integration for quick scanning
- Multi-location inventory synchronization

### 💊 Comprehensive Prescription System
- Digital prescription processing with e-signature support
- Real-time medication availability validation
- Automated prescription status tracking
- Complete patient medication history
- Advanced analytics and reporting tools
- Prescription-to-inventory integration

### 📊 Business Intelligence
- Real-time sales analytics dashboard
- Inventory turnover and performance metrics
- Custom report generation
- Revenue and profit analysis
- Patient adherence tracking
- Expiry and waste management reports

### 🔒 Enterprise-Grade Security
- JWT Authentication with refresh tokens
- Granular role-based access control (RBAC)
- Comprehensive audit logging
- HIPAA/GDPR compliant data protection
- API rate limiting and DDoS protection
- Regular security audits and updates

## 📋 Table of Contents

- [🚀 Quick Start](#-quick-start)
- [🏗️ Project Structure](#%EF%B8%8F-project-structure)
- [🔌 Requirements](#-requirements)
- [⚙️ Configuration](#%EF%B8%8F-configuration)
- [📚 API Documentation](#-api-documentation)
- [🔐 Authentication](#-authentication)
- [🐳 Docker Deployment](#-docker-deployment)
- [☁️ Production Deployment](#%EF%B8%8F-production-deployment)
- [🧪 Testing](#-testing)
- [🤝 Contributing](#-contributing)
- [📄 License](#-license)
- [License](#-license)

## 🚀 Quick Start

Get started with the Pharmacy Inventory API in minutes.

### Prerequisites
- Python 3.8 or higher
- PostgreSQL 13+ (recommended) or SQLite
- pip 20.0.0+
- Git
- Virtualenv (recommended)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/atem-kuot/ALX_BE_Capstone_project.git
   cd Pharmacy_Inventory_API
   ```

2. **Set up a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: .\venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   Create a `.env` file in the project root:
   ```env
   DEBUG=True
   SECRET_KEY=your-secret-key-here
   DATABASE_URL=postgres://user:password@localhost:5432/pharmacy_db
   ALLOWED_HOSTS=localhost,127.0.0.1
   ```

5. **Run migrations**
   ```bash
   python manage.py makemigrations
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

   The API will be available at `http://127.0.0.1:8000/`
   
   Access the admin panel at `http://127.0.0.1:8000/admin/`

## 🏗️ Project Structure

```
pharmacy-inventory/
├── Pharmacy_Inventory_API/     # Main project directory
│   ├── __init__.py
│   ├── settings.py            # Project settings
│   ├── urls.py                # Main URL configuration
│   └── wsgi.py                # WSGI config
├── alerts/                    # Alerts app
├── core/                      # Core functionality
├── medicines/                 # Medicines app
│   ├── migrations/
│   ├── __init__.py
│   ├── admin.py
│   ├── models.py
│   ├── serializers.py
│   ├── urls.py
│   └── views.py
├── manage.py
├── requirements.txt           # Project dependencies
└── .env.example              # Example environment variables
```

## 🔌 Requirements

The project requires the following dependencies:

### Core Dependencies
- Python 3.8+
- Django 4.2
- Django REST Framework 3.14.0
- SQLite 3.36+ (built into Python)
- Python Decouple 3.8
- dj-database-url 1.3.0

### Development Dependencies
- black 23.7.0 (code formatting)
- flake8 6.1.0 (linting)
- pytest 7.4.0 (testing)
- pytest-django 4.5.2 (Django test integration)
- coverage 7.2.7 (test coverage)
- factory-boy 3.3.0 (test fixtures)

### Production Dependencies
- gunicorn 21.2.0 (WSGI server)
- whitenoise 6.5.0 (static files)
- django-cors-headers 4.3.0 (CORS support)
- django-environ 0.11.2 (environment management)

### Security Dependencies
- djangorestframework-simplejwt 5.3.0 (JWT authentication)
- django-axes 6.0.2 (security monitoring)
- django-ratelimit 4.0.0 (API rate limiting)

## ⚙️ Configuration

### Environment Variables

Create a `.env` file in the project root with the following variables:

```env
# Django Settings
DEBUG=True
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=localhost,127.0.0.1

# Database
DATABASE_URL=sqlite:///db.sqlite3

# JWT Authentication
JWT_SECRET_KEY=your-jwt-secret-key
JWT_ALGORITHM=HS256
JWT_EXPIRATION_DELTA_DAYS=7

# Email Configuration (for notifications)
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
DEFAULT_FROM_EMAIL=noreply@pharmacy.com

# CORS Settings
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
```

### Running with Docker (Alternative)

1. Ensure Docker and Docker Compose are installed
2. Copy the example environment file:
   ```bash
   cp .env.example .env
   ```
3. Update the `.env` file with your configuration
4. Build and start the containers:
   ```bash
   docker-compose up --build
   ```
5. Run migrations:
   ```bash
   docker-compose exec web python manage.py migrate
   ```
6. Create a superuser:
   ```bash
   docker-compose exec web python manage.py createsuperuser
   ```

## 📚 API Documentation

Once the development server is running, you can access the following endpoints:

### Base URL
```
http://localhost:8000/api/
```

### Authentication
All API endpoints require authentication using JWT tokens.

#### Obtain Token
```http
POST /api/token/
Content-Type: application/json

{
    "username": "your_username",
    "password": "your_password"
}
```

Response:
```json
{
    "refresh": "your_refresh_token",
    "access": "your_access_token"
}
```

#### Refresh Token
```http
POST /api/token/refresh/
Content-Type: application/json

{
    "refresh": "your_refresh_token"
}
```

### Core Endpoints

#### Medicines
- `GET /api/medicines/` - List all medicines
- `POST /api/medicines/` - Create a new medicine
- `GET /api/medicines/{id}/` - Retrieve a specific medicine
- `PUT /api/medicines/{id}/` - Update a medicine
- `DELETE /api/medicines/{id}/` - Delete a medicine
- `GET /api/medicines/low-stock/` - List low stock medicines
- `GET /api/medicines/expiring-soon/` - List medicines expiring soon

#### Prescriptions
- `GET /api/prescriptions/` - List all prescriptions
- `POST /api/prescriptions/` - Create a new prescription
- `GET /api/prescriptions/{id}/` - Retrieve a specific prescription
- `PUT /api/prescriptions/{id}/` - Update a prescription
- `DELETE /api/prescriptions/{id}/` - Delete a prescription
- `GET /api/prescriptions/patient/{patient_id}/` - Get patient's prescriptions

#### Alerts
- `GET /api/alerts/` - List all alerts
- `GET /api/alerts/unread/` - List unread alerts
- `PATCH /api/alerts/{id}/mark-read/` - Mark alert as read

## 🔐 Authentication

The API uses JWT (JSON Web Tokens) for authentication. To authenticate your requests, include the JWT token in the Authorization header:

```http
Authorization: Bearer your_access_token_here
```

### User Roles

1. **Admin**
   - Full access to all endpoints
   - Can manage users and system settings
   - Can view all data across the system

2. **Pharmacist**
   - Can manage medicines and prescriptions
   - Can view and update patient information
   - Cannot modify system settings

3. **Staff**
   - Can view medicines and prescriptions
   - Limited write access
   - Cannot access sensitive operations

## 🐳 Docker Deployment

### Prerequisites
- Docker 20.10.0+
- Docker Compose 1.29.0+

### Steps

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/pharmacy-inventory.git
   cd pharmacy-inventory
   ```

2. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

3. **Build and start the containers**
   ```bash
   docker-compose up --build -d
   ```

4. **Run migrations**
   ```bash
   docker-compose exec web python manage.py migrate
   ```

5. **Create superuser**
   ```bash
   docker-compose exec web python manage.py createsuperuser
   ```

6. **Access the application**
   - API: http://localhost:8000/
   - Admin: http://localhost:8000/admin/

## ☁️ Production Deployment

### Prerequisites
- Linux server (Ubuntu 20.04+ recommended)
- Nginx
- PostgreSQL
- Python 3.8+
- Redis (for caching and Celery)

### Deployment Steps

1. **Server Setup**
   ```bash
   # Update system packages
   sudo apt update && sudo apt upgrade -y
   
   # Install required packages
   sudo apt install -y python3-pip python3-venv nginx redis-server
   ```

2. **Database Setup**
   SQLite is used by default with Django. The database file (`db.sqlite3`) will be created automatically when you run migrations.

3. **Deploy Application**
   ```bash
   # Clone repository
   git clone https://github.com/atem-kuot/ALX_BE_Capstone_project.git/opt/pharmacy-inventory
   cd /opt/Pharmacy_Inventory_API
   
   # Create virtual environment
   python3 -m venv venv
   source venv/bin/activate
   
   # Install dependencies
   pip install -r requirements/production.txt
   
   # Configure environment variables
   cp .env.example .env
   nano .env  # Update with production settings
   
   # Run migrations
   python manage.py migrate
   python manage.py collectstatic --noinput
   
   # Create superuser
   python manage.py createsuperuser
   ```

4. **Configure Gunicorn**
   Create `/etc/systemd/system/pharmacy.service`:
   ```ini
   [Unit]
   Description=Pharmacy Inventory Gunicorn Service
   After=network.target

   [Service]
   User=www-data
   Group=www-data
   WorkingDirectory=/opt/pharmacy-inventory
   Environment="PATH=/opt/pharmacy-inventory/venv/bin"
   ExecStart=/opt/pharmacy-inventory/venv/bin/gunicorn \
       --workers 3 \
       --bind unix:/run/pharmacy.sock \
       --timeout 120 \
       Pharmacy_Inventory_API.wsgi:application
   
   [Install]
   WantedBy=multi-user.target
   ```

5. **Configure Nginx**
   Create `/etc/nginx/sites-available/pharmacy`:
   ```nginx
   server {
       listen 80;
       server_name yourdomain.com;

       location = /favicon.ico { access_log off; log_not_found off; }
       
       location /static/ {
           root /opt/pharmacy-inventory;
       }

       location / {
           include proxy_params;
           proxy_pass http://unix:/run/pharmacy.sock;
       }
   }
   ```

6. **Enable the site and start services**
   ```bash
   sudo systemctl daemon-reload
   sudo systemctl start pharmacy
   sudo systemctl enable pharmacy
   sudo systemctl restart nginx
   ```

7. **Set up SSL (recommended)**
   ```bash
   sudo apt install certbot python3-certbot-nginx
   sudo certbot --nginx -d yourdomain.com
   ```

## 🧪 Testing

Run the test suite with:

```bash
# Run all tests
pytest

# Run tests with coverage report
pytest --cov=.

# Run specific test file
pytest path/to/test_file.py
```

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📞 Contact

For any questions or support, please contact Atem Kuot - atemliaikuot@gmail.com

Project Link: [https://github.com/atem-kuot/ALX_BE_Capstone_project.git](https://github.com/atem-kuot/ALX_BE_Capstone_project.git)
pip install -r requirements.txt

# Set up environment
cp .env.example .env
# Edit .env with your settings

# Run migrations
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser

# Start development server
python manage.py runserver
```

## 🏗 Project Structure

```
Pharmacy_Inventory_API/
├── core/            # Authentication & user management
├── medicines/       # Inventory management
├── prescriptions/   # Prescription handling
├── alerts/          # Notification system
└── config/          # Project configuration
```

## 📚 API Documentation

### Authentication
- `POST /api/auth/login/` - User login
- `POST /api/auth/refresh/` - Refresh token
- `POST /api/auth/register/` - Register new user (Admin only)

### Medicines
- `GET /api/medicines/` - List all medicines
- `POST /api/medicines/` - Add new medicine
- `GET /api/medicines/{id}/` - Get medicine details
- `PUT /api/medicines/{id}/` - Update medicine
- `DELETE /api/medicines/{id}/` - Delete medicine

### Prescriptions
- `GET /api/prescriptions/` - List prescriptions
- `POST /api/prescriptions/` - Create prescription
- `GET /api/prescriptions/{id}/` - Get details
- `PUT /api/prescriptions/{id}/fulfill/` - Fulfill prescription

## 🔐 Authentication

Uses JWT with role-based access control:

```python
# Example login request
POST /api/auth/login/
{
    "username": "pharmacist1",
    "password": "securepassword123"
}
```

## 🚀 Deployment

### Production
```bash
# Install Gunicorn
pip install gunicorn

# Run with Gunicorn
gunicorn --workers 3 --bind 0.0.0.0:8000 config.wsgi:application
```

### Docker
```bash
docker-compose up -d --build
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
```

## 🧪 Testing

```bash
# Run tests
python manage.py test

# With coverage
coverage run manage.py test
coverage report
```

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.



### 🔍 API Reference

### Authentication
- `POST /api/core/auth/login/` - User login
- `POST /api/core/auth/refresh/` - Refresh JWT token
- `POST /api/core/auth/register/` - Register new user (Admin only)
- `GET /api/core/auth/me/` - Get current user info

### Medicine Management
- `GET /api/medicines/` - List medicines
- `POST /api/medicines/` - Add medicine
- `GET /api/medicines/{id}/` - Get medicine details
- `PUT /api/medicines/{id}/` - Update medicine
- `DELETE /api/medicines/{id}/` - Delete medicine
- `GET /api/medicines/low-stock/` - List low stock items

### Prescription Management
- `GET /api/prescriptions/` - List prescriptions
- `POST /api/prescriptions/` - Create prescription
- `GET /api/prescriptions/{id}/` - Get details
- `PUT /api/prescriptions/{id}/fulfill/` - Fulfill prescription

### Alert System
- `GET /api/alerts/` - List alerts
- `POST /api/alerts/{id}/resolve/` - Resolve alert
- `GET /api/alerts/preferences/` - Get alert settings

## 📊 Models Overview

### Core Models

#### [User Model](core/models.py)
- **Roles**: Doctor, Pharmacist, Admin
- **Fields**: username, email, role, phone
- **Constraints**: Unique email, required phone for doctors

### Medicine Models

#### [Medicine Model](medicines/models.py)
- **Categories**: 70+ medical categories (Antibiotic, Analgesic, etc.)
- **Key Fields**: name, category, quantity, dosage, expiry_date, threshold_alert
- **Relations**: Links to Supplier
- **Methods**: `update_quantity()` for safe stock updates

#### [Supplier Model](medicines/models.py)
- **Fields**: name, contact_person, email, phone, address
- **Relations**: One-to-many with Medicine

#### [Patient Model](medicines/models.py)
- **Fields**: personal info, medical history, allergies
- **Relations**: Links to prescriptions

#### [InventoryLog Model](medicines/models.py)
- **Purpose**: Audit trail for all inventory changes
- **Actions**: Stock add/remove, prescription fulfillment, discarding
- **Relations**: Links to Medicine, User, and Prescription

### Alert Models

#### [AlertLog Model](alerts/models.py)
- **Types**: Low stock, expiry warnings, prescription alerts
- **Severity Levels**: Low, Medium, High, Critical
- **Features**: Auto-resolution, Telegram notifications
- **Relations**: Links to Medicine, Prescription, User

#### [AlertPreference Model](alerts/models.py)
- **Notification Methods**: Email, push, SMS, Telegram
- **Customization**: Alert type filters, severity thresholds
- **Features**: Daily digest, immediate alerts

## 🚨 Alert System

The alert system provides comprehensive monitoring with multiple notification channels:

### Alert Types
- **Low Stock**: When medicine quantity falls below threshold
- **Expiry Warning**: Medicines approaching expiration
- **Expired**: Medicines past expiration date
- **Prescription Alerts**: Urgent or pending prescriptions
- **System Alerts**: General system notifications

### Notification Channels
- **Telegram Bot**: Real-time notifications via [`telegram_service.py`](core/telegram_service.py)
- **Email**: Standard email notifications
- **Push Notifications**: In-app notifications
- **Daily Digest**: Summary of unresolved alerts

### Alert Configuration
Users can customize their alert preferences through the [`AlertPreference`](alerts/models.py) model:
- Choose notification methods
- Set minimum severity levels
- Filter by alert types
- Configure frequency settings

## 🔧 Management Commands

### Daily Digest Command
[`send_daily_digest.py`](alerts/management/commands/send_daily_digest.py)

Sends a daily summary of unresolved alerts via Telegram:

```bash
python manage.py send_daily_digest
```

**Features**:
- Filters alerts from last 24 hours
- Groups by severity level
- Includes medicine and prescription details
- Automatic scheduling support

## 🔐 Authentication

The API uses JWT (JSON Web Tokens) for authentication with role-based access control:

### User Roles
- **Doctor**: Can create prescriptions, view patient records
- **Pharmacist**: Can manage inventory, fulfill prescriptions
- **Admin**: Full system access, user management

### Permission Classes
Custom permission classes in [`permissions.py`](core/permissions.py) control access based on user roles and object ownership.

## 💡 Usage Examples

### Creating a Supplier
```python
# Example: Create a new supplier
import requests

url = "http://localhost:8000/api/medicines/suppliers/"
headers = {
    "Authorization": "Bearer your_access_token_here",
    "Content-Type": "application/json"
}

supplier_data = {
    "name": "Global Pharma Supplies",
    "contact_person": "John Doe",
    "email": "contact@globalpharma.com",
    "phone": "+1234567890",
    "address": "123 Medical Supply Ave, Pharma City, PC 12345"
}

response = requests.post(url, json=supplier_data, headers=headers)
print(response.status_code)
print(response.json())
```

### Retrieving Suppliers
```python
# Get all suppliers
response = requests.get("http://localhost:8000/api/medicines/suppliers/", headers=headers)
suppliers = response.json()
print(suppliers)

# Get a specific supplier
supplier_id = 1
response = requests.get(f"http://localhost:8000/api/medicines/suppliers/{supplier_id}/", headers=headers)
supplier = response.json()
print(supplier)
```

### Fulfilling a Prescription
```python
PUT /api/prescriptions/1/fulfill/
{
    "notes": "Prescription fulfilled successfully"
}
```

### Setting Alert Preferences
```python
PUT /api/alerts/preferences/
{
    "telegram_notifications": true,
    "min_severity_level": "MEDIUM",
    "daily_digest": true,
    "immediate_alerts": true
}
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Guidelines
- Follow Django best practices
- Write comprehensive tests
- Update documentation for new features
- Ensure proper error handling
- Maintain API versioning

## 📝 License

This project is part of the ALX Backend Engineering Capstone Project.

## 🆘 Support

For support and questions:
- Create an issue in the repository
- Check the [Django documentation](https://docs.djangoproject.com/)
- Review the [Django REST Framework documentation](https://www.django-rest-framework.org/)

---
