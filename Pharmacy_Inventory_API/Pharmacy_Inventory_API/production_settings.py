# production_settings.py
from .settings import *

DEBUG = False
ALLOWED_HOSTS = ['AtemKuot.pythonanywhere.com', 'localhost']

# PostgreSQL database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME', 'pharmacy_db'),
        'USER': os.getenv('DB_USER', 'pharmacy_user'),
        'PASSWORD': os.getenv('DB_PASSWORD', ''),
        'HOST': os.getenv('DB_HOST', 'localhost'),
        'PORT': os.getenv('DB_PORT', '5432'),
    }
}

# Static files
STATIC_ROOT = '/home/AtemKuot/Pharmacy_Inventory_API/static'
STATIC_URL = '/static/'

# Media files
MEDIA_ROOT = '/home/AtemKuot/Pharmacy_Inventory_API/media'
MEDIA_URL = '/media/'

# Security settings
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
SECURE_SSL_REDIRECT = True