
import os
from dotenv import load_dotenv

# Load environment variables from .env file
# This allows us to use environment variables without exposing sensitive data in the code
load_dotenv()

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
# BASE_DIR is the absolute path to the project root directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# SECURITY WARNING: keep the secret key used in production secret!
# The secret key is used for cryptographic signing and should be kept secure
# Using environment variable allows different keys for different environments
SECRET_KEY = os.getenv('SECRET_KEY', 'django-insecure-change-this-in-production')

# SECURITY WARNING: don't run with debug turned on in production!
# Debug mode provides detailed error pages and should never be used in production
# Using environment variable allows easy toggling between development and production
DEBUG = os.getenv('DEBUG', 'True').lower() == 'true'

# ALLOWED_HOSTS specifies the host/domain names that this Django site can serve
# This is a security measure to prevent HTTP Host header attacks
# Using environment variable allows different allowed hosts for different environments
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',')

# Application definition
# INSTALLED_APPS lists all Django applications that are activated in this project
# Core Django apps provide essential functionality like admin, auth, sessions, etc.
# Third-party apps extend functionality: rest_framework (API), corsheaders (CORS), drf_yasg (Swagger)
# Custom apps: employees, attendance, performance, analytics (part of this project)
INSTALLED_APPS = [
    'django.contrib.admin',          # Django admin interface for managing data
    'django.contrib.auth',           # Authentication system for user management
    'django.contrib.contenttypes',    # Content type framework for permissions
    'django.contrib.sessions',        # Session framework for managing user sessions
    'django.contrib.messages',       # Message framework for displaying notifications
    'django.contrib.staticfiles',     # Static file management
    'rest_framework',                 # Django REST Framework for building APIs
    'corsheaders',                    # Cross-Origin Resource Sharing headers
    'drf_yasg',                      # Swagger/OpenAPI documentation for APIs
    'apps.employees',                 # Employee management application
    'apps.attendance',               # Attendance tracking application
    'apps.performance',               # Performance evaluation application
    'apps.analytics',                 # Analytics and reporting application
]

# MIDDLEWARE defines the order in which middleware processes requests
# Middleware components provide various functionalities like security, sessions, etc.
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',      # Handles Cross-Origin Resource Sharing
    'django.middleware.security.SecurityMiddleware',  # Provides security features
    'django.contrib.sessions.middleware.SessionMiddleware',  # Manages user sessions
    'django.middleware.common.CommonMiddleware',  # Common middleware for request/response processing
    'django.middleware.csrf.CsrfViewMiddleware',  # Cross-Site Request Forgery protection
    'django.contrib.auth.middleware.AuthenticationMiddleware',  # User authentication
    'django.contrib.messages.middleware.MessageMiddleware',  # Message framework
    'django.middleware.clickjacking.XFrameOptionsMiddleware',  # Clickjacking protection
]

# ROOT_URLCONF specifies the Python module where the URLconf for the project is located
# This file defines the URL patterns for the entire application
ROOT_URLCONF = 'employee_analytics.urls'

# TEMPLATES configuration defines how Django handles template rendering
# This project uses Django's built-in template engine
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',  # Template engine to use
        'DIRS': [],  # List of directories where Django looks for template files
        'APP_DIRS': True,  # Whether to look for templates inside each app directory
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',      # Adds debug information to templates
                'django.template.context_processors.request',    # Adds request information to templates
                'django.contrib.auth.context_processors.auth',   # Adds authentication context to templates
                'django.contrib.messages.context_processors.messages',  # Adds message context to templates
            ],
        },
    },
]

# WSGI_APPLICATION specifies the WSGI application to be used for serving the project
# This is used for production deployment with WSGI servers like Gunicorn or uWSGI
WSGI_APPLICATION = 'employee_analytics.wsgi.application'

# Database configuration
# This project uses NeonDB, a cloud-based PostgreSQL service
# Using environment variables for database credentials enhances security
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',  # Database backend to use
        'NAME': os.getenv('DB_NAME', 'neondb'),     # Database name from environment variable
        'USER': os.getenv('DB_USER', 'neondb_owner'),  # Database username from environment variable
        'PASSWORD': os.getenv('DB_PASSWORD', 'npg_ZU7WFBto9mfV'),  # Database password from environment variable
        'HOST': os.getenv('DB_HOST', 'ep-old-bread-adivkbla-pooler.c-2.us-east-1.aws.neon.tech'),  # Database host from environment variable
        'PORT': os.getenv('DB_PORT', '5432'),       # Database port from environment variable
        'OPTIONS': {
            'sslmode': 'require',  # Enforce SSL connection for security
        },
    }
}

# Password validation
# AUTH_PASSWORD_VALIDATORS defines the rules for validating user passwords
# These validators ensure passwords meet security requirements
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',  # Checks password similarity to user attributes
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',  # Enforces minimum password length
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',  # Prevents common passwords
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',  # Prevents entirely numeric passwords
    },
]

# Internationalization settings
# These settings control how Django handles language and time zones
LANGUAGE_CODE = 'en-us'  # Default language code for the project
TIME_ZONE = 'UTC'  # Default time zone for the project
USE_I18N = True  # Enables internationalization features
USE_TZ = True  # Enables timezone-aware datetimes

# Static files configuration
# These settings control how Django handles static files (CSS, JavaScript, images)
STATIC_URL = '/static/'  # URL prefix for static files
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')  # Directory for collecting static files in production
STATICFILES_DIRS = [  # Additional directories where static files are stored
    os.path.join(BASE_DIR, 'static'),
]

# Default primary key field type
# DEFAULT_AUTO_FIELD specifies the default type for auto-created primary key fields
# Using BigAutoField provides a 64-bit integer field for better scalability
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Django REST Framework settings
# These settings configure the behavior of the REST API
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',  # Token-based authentication for API clients
        'rest_framework.authentication.SessionAuthentication',  # Session authentication for web clients
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',  # Requires authentication for all API endpoints
    ],
    'DEFAULT_PAGINATION_CLASS': 'utils.pagination.StandardResultsSetPagination',  # Custom pagination class
    'PAGE_SIZE': 20,  # Number of items per page in paginated responses
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.ScopedRateThrottle',  # Enables rate limiting for API endpoints
    ],
    'DEFAULT_THROTTLE_RATES': {
        'user': os.getenv('API_RATE_LIMIT', '100/day'),  # Default rate limit for API requests
        'burst': os.getenv('API_BURST_RATE', '10/hour'),  # Burst rate limit for API requests
    },
    'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.coreapi.AutoSchema'  # Schema class for API documentation
}

# CORS (Cross-Origin Resource Sharing) settings
# These settings control which origins are allowed to access the API
# CORS is necessary when the frontend and backend are on different domains or ports
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",   # Local development frontend (React/Vue/Angular)
    "http://127.0.0.1:3000",   # Alternative localhost frontend
    "http://localhost:8000",   # Local development backend
    "http://127.0.0.1:8000",   # Alternative localhost backend
]
CORS_ALLOW_CREDENTIALS = True  # Allows cookies to be included in cross-origin requests

# Swagger/OpenAPI documentation settings
# These settings configure the API documentation interface
SWAGGER_SETTINGS = {
    'SECURITY_DEFINITIONS': {
        'Token': {
            'type': 'apiKey',       # Authentication type (API key)
            'name': 'Authorization', # Header name for the token
            'in': 'header'           # Where the token should be sent (header)
        }
    },
    'USE_SESSION_AUTH': True,  # Enables session-based authentication in Swagger UI
    'JSON_EDITOR': True,       # Enables JSON editor in Swagger UI
    'IS_AUTHENTICATED': False,  # Whether authentication is required to view the API docs
}
