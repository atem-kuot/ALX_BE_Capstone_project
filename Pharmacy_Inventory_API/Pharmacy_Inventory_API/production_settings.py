# production_settings.py
from .settings import *

DEBUG = False
ALLOWED_HOSTS = ['AtemKuot.pythonanywhere.com', 'localhost']

 # MySQL database configuration for PythonAnywhere
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.getenv('DB_NAME', 'yourusername$pharmacy_db'),
        'USER': os.getenv('DB_USER', 'yourusername'),
        'PASSWORD': os.getenv('DB_PASSWORD', ''),
        'HOST': os.getenv('DB_HOST', 'yourusername.mysql.pythonanywhere-services.com'),
        'PORT': os.getenv('DB_PORT', '3306'),
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
            'charset': 'utf8mb4',
        }
    }
}

# Static files
STATIC_ROOT = '/home/yourusername/pharmacy_api/static'
STATIC_URL = '/static/'

# Security settings
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
SECURE_SSL_REDIRECT = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True

# For MySQL compatibility
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'