# Pharmacy Inventory Management API

A comprehensive Django REST API for managing pharmacy inventory, prescriptions, and alerts. This system provides role-based access control for doctors, pharmacists, and administrators to efficiently manage medicine stock, patient prescriptions, and automated notifications.

## 🚀 Features

- **Medicine Inventory Management** - Track stock levels, expiry dates, and supplier information
- **Prescription Management** - Handle patient prescriptions with automated inventory updates
- **Smart Alert System** - Automated notifications for low stock, expiring medicines, and urgent prescriptions
- **Role-Based Access Control** - Separate permissions for doctors, pharmacists, and administrators
- **Telegram Integration** - Real-time notifications via Telegram bot
- **Comprehensive Logging** - Full audit trail of inventory changes
- **RESTful API** - Clean, well-documented API endpoints

## 📋 Table of Contents

- [Project Structure](#project-structure)
- [Installation](#installation)
- [Configuration](#configuration)
- [API Endpoints](#api-endpoints)
- [Models Overview](#models-overview)
- [Alert System](#alert-system)
- [Management Commands](#management-commands)
- [Authentication](#authentication)
- [Usage Examples](#usage-examples)
- [Contributing](#contributing)

## 📁 Project Structure

```
Pharmacy_Inventory_API/
├── Pharmacy_Inventory_API/          # Main project configuration
│   ├── __init__.py
│   ├── settings.py                  # Django settings and configuration
│   ├── urls.py                      # Main URL routing
│   ├── wsgi.py                      # WSGI configuration
│   └── asgi.py                      # ASGI configuration
├── core/                            # Core application (User management)
│   ├── models.py                    # User model with role-based permissions
│   ├── views.py                     # Authentication and user management views
│   ├── urls.py                      # Core app URL patterns
│   ├── serializers.py               # User serializers
│   ├── permissions.py               # Custom permission classes
│   └── telegram_service.py          # Telegram bot integration
├── medicines/                       # Medicine inventory management
│   ├── models.py                    # Medicine, Supplier, Patient, InventoryLog models
│   ├── views.py                     # Medicine CRUD operations
│   ├── urls.py                      # Medicine app URL patterns
│   ├── serializers.py               # Medicine serializers
│   └── admin.py                     # Django admin configuration
├── prescriptions/                   # Prescription management
│   ├── models.py                    # Prescription and related models
│   ├── views.py                     # Prescription handling views
│   ├── urls.py                      # Prescription URL patterns
│   └── serializers.py               # Prescription serializers
├── alerts/                          # Alert and notification system
│   ├── models.py                    # AlertLog and AlertPreference models
│   ├── views.py                     # Alert management views
│   ├── urls.py                      # Alert URL patterns
│   ├── serializers.py               # Alert serializers
│   └── management/
│       └── commands/
│           └── send_daily_digest.py # Daily alert digest command
└── manage.py                        # Django management script
```

## 🛠 Installation

### Prerequisites

- Python 3.8+
- PostgreSQL (for production) or SQLite (for development)
- Django 5.2.5
- Django REST Framework

### Setup Steps

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd ALX_BE_Capstone_project/Pharmacy_Inventory_API
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install django djangorestframework djangorestframework-simplejwt psycopg2-binary python-telegram-bot
   ```

4. **Environment Configuration**
   Create a `.env` file in the project root:
   ```env
   SECRET_KEY=your-secret-key-here
   DEBUG=True
   DB_USER=your-db-user
   DB_PASSWORD=your-db-password
   DB_HOST=localhost
   TELEGRAM_BOT_TOKEN=your-telegram-bot-token
   TELEGRAM_CHAT_ID=your-telegram-chat-id
   ```

5. **Database Setup**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   python manage.py createsuperuser
   ```

6. **Run the server**
   ```bash
   python manage.py runserver
   ```

## ⚙️ Configuration

### Database Configuration

The project supports both SQLite (development) and PostgreSQL (production). Configuration is in [`settings.py`](Pharmacy_Inventory_API/settings.py).

### JWT Authentication

JWT tokens are configured with:
- **Access Token Lifetime**: 1 hour
- **Refresh Token Lifetime**: 7 days

### Telegram Integration

Configure Telegram notifications by setting:
- `TELEGRAM_BOT_TOKEN`: Your bot token from BotFather
- `TELEGRAM_CHAT_ID`: Default chat ID for notifications

## 🔗 API Endpoints

### Authentication
- `POST /api/core/auth/login/` - User login
- `POST /api/core/auth/refresh/` - Refresh JWT token
- `POST /api/core/auth/register/` - User registration

### Medicine Management
- `GET /api/medicines/` - List all medicines
- `POST /api/medicines/` - Create new medicine
- `GET /api/medicines/{id}/` - Get medicine details
- `PUT /api/medicines/{id}/` - Update medicine
- `DELETE /api/medicines/{id}/` - Delete medicine

### Prescription Management
- `GET /api/prescriptions/` - List prescriptions
- `POST /api/prescriptions/` - Create prescription
- `GET /api/prescriptions/{id}/` - Get prescription details
- `PUT /api/prescriptions/{id}/fulfill/` - Fulfill prescription

### Alert Management
- `GET /api/alerts/` - List alerts
- `POST /api/alerts/{id}/resolve/` - Resolve alert
- `GET /api/alerts/preferences/` - Get user alert preferences
- `PUT /api/alerts/preferences/` - Update alert preferences

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

**Built with ❤️ using Django REST Framework**