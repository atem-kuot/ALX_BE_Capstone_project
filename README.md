<div align="center">
  <h1>🏥 Pharmacy Inventory Management API</h1>
  <p>A comprehensive Django REST API for modern pharmacy operations</p>
  
  [![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
  [![Django](https://img.shields.io/badge/Django-4.2-brightgreen.svg)](https://www.djangoproject.com/)
  [![DRF](https://img.shields.io/badge/DRF-3.14.0-red.svg)](https://www.django-rest-framework.org/)
  [![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
</div>

## ✨ Features

### 📦 Inventory Management
- Real-time stock monitoring & alerts
- Batch and expiry tracking
- Supplier management
- Automated reordering

### 📝 Prescription Workflow
- Digital prescriptions
- Stock validation
- Fulfillment tracking
- Patient history

### 🔔 Smart Alerts
- Low stock warnings
- Expiry notifications
- Prescription status updates
- Customizable thresholds

### 🔒 Security
- JWT Authentication
- Role-based access
- Activity logging
- Secure endpoints

## 📋 Table of Contents

- [Quick Start](#-quick-start)
- [Project Structure](#-project-structure)
- [API Documentation](#-api-documentation)
- [Authentication](#-authentication)
- [Deployment](#-deployment)
- [Testing](#-testing)
- [Contributing](#-contributing)
- [License](#-license)

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- PostgreSQL/SQLite
- pip

### Installation

```bash
# Clone repository
git clone https://github.com/yourusername/Pharmacy_Inventory_API.git
cd Pharmacy_Inventory_API

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment
cp .env.example .env
# Edit .env with your settings

# Run migrations
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
sqlmigrate
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

### Creating a Medicine
```python
POST /api/medicines/
{
    "name": "Paracetamol",
    "category": "ANALGESIC",
    "quantity": 100,
    "dosage": "500mg/tablet",
    "expiry_date": "2025-12-31",
    "threshold_alert": 20,
    "supplier": 1
}
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
