"""
Django settings for itico project.

Portal Interno de Contrapartes – App Pacífico (Cotizador Web)
Sistema de gestión de contrapartes con debida diligencia automatizada.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

from pathlib import Path
from decouple import config
import os
import dj_database_url

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY', default='django-insecure-change-this-in-production')

# SECURITY WARNING: don't run with debug turned on in production!
#database production settings db name "itico", username "itico", password "postgres"
DEBUG = True
if DEBUG:
    DATABASES = {
        'default': dj_database_url.config(
            default='postgresql://postgres:FP.h05t1l3@localhost:5432/itico',
            conn_max_age=600,
        )
    }
else:
    DATABASES = {
        'default': dj_database_url.config(
            default='postgresql://postgres:FP.h05t1l3@localhost:5432/itico',
            conn_max_age=600,
        )
    }

    """
     DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
    DATABASES = {
        'default': dj_database_url.config(
            default='postgresql://itico:FP.h05t1l3@localhost:5432/itico',
            conn_max_age=600,
        )
    }
    """

# ALLOWED_HOSTS configuration for production
if DEBUG:
    ALLOWED_HOSTS = ['*']  # Allow all hosts in development
else:
    ALLOWED_HOSTS = [
        'app.iticore.com',
        'localhost',
        '127.0.0.1',
    ]

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Third party apps
    'rest_framework',
    'corsheaders',
    'crispy_forms',
    'crispy_tailwind',
    'django_htmx',
    'django_extensions',
    
    # Local apps
    'contrapartes',
    'debida_diligencia',
    'notificaciones',
    'dashboard',
    'api',
    'usuarios',
    'django_celery_beat',  # For Celery periodic tasks
]

# Crispy Forms
CRISPY_ALLOWED_TEMPLATE_PACKS = "tailwind"
CRISPY_TEMPLATE_PACK = "tailwind"

# Django REST Framework
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ],
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Add this for static files
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django_htmx.middleware.HtmxMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'itico.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'itico.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

# Use different databases for development and production

# Debug database configuration
db_config = DATABASES['default']
db_engine = db_config.get('ENGINE', 'Unknown')
db_name = db_config.get('NAME', 'Unknown')

print(f"[ITICO] Database Engine: {db_engine}")
print(f"[ITICO] Database Name: {db_name}")

# Validate production database
if not DEBUG and 'postgresql' not in db_engine:
    print(f"[ITICO] WARNING: Not using PostgreSQL in production! Engine: {db_engine}")
elif not DEBUG:
    print(f"[ITICO] PostgreSQL configured correctly for production")


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'es-co'

TIME_ZONE = config('TIME_ZONE', default='America/Bogota')

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

# Media files
# Media files configuration (user uploads)
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Ensure media directory exists
os.makedirs(MEDIA_ROOT, exist_ok=True)

# Additional media settings for better handling
MEDIA_FILES_MAX_SIZE = 50 * 1024 * 1024  # 50MB
ALLOWED_MEDIA_EXTENSIONS = [
    'jpg', 'jpeg', 'png', 'gif', 'bmp', 'svg',  # Images
    'pdf', 'doc', 'docx', 'xls', 'xlsx', 'ppt', 'pptx',  # Documents
    'txt', 'csv', 'json', 'xml',  # Text files
    'mp4', 'avi', 'mov', 'wmv', 'flv', 'webm',  # Videos
    'mp3', 'wav', 'ogg', 'aac',  # Audio
    'zip', 'rar', '7z', 'tar', 'gz',  # Archives
]

# Media file security settings for production
if not DEBUG:
    # In production, consider additional security for media files
    # Maximum file size for uploads (50MB)
    FILE_UPLOAD_MAX_MEMORY_SIZE = 52428800  # 50MB
    DATA_UPLOAD_MAX_MEMORY_SIZE = 52428800  # 50MB
    
    # File upload permissions
    FILE_UPLOAD_PERMISSIONS = 0o644
    FILE_UPLOAD_DIRECTORY_PERMISSIONS = 0o755
else:
    # Development settings - more permissive
    FILE_UPLOAD_MAX_MEMORY_SIZE = 104857600  # 100MB for development
    DATA_UPLOAD_MAX_MEMORY_SIZE = 104857600  # 100MB for development

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# =============================================================================
# CONFIGURACIONES ESPECÍFICAS DE ITICO
# =============================================================================

# Celery Configuration
CELERY_BROKER_URL = config('REDIS_URL', default='redis://localhost:6379/0')
CELERY_RESULT_BACKEND = config('REDIS_URL', default='redis://localhost:6379/0')
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = TIME_ZONE

# RPA Makito Integration
MAKITO_API_URL = config('MAKITO_API_URL', default='http://localhost:8080/api')
MAKITO_API_KEY = config('MAKITO_API_KEY', default='')

# AI Service Configuration
AI_SERVICE_URL = config('AI_SERVICE_URL', default='http://localhost:8081/api')
AI_SERVICE_KEY = config('AI_SERVICE_KEY', default='')

# Email Configuration
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = config('EMAIL_HOST', default='smtp.gmail.com')
EMAIL_PORT = config('EMAIL_PORT', default=587, cast=int)
EMAIL_USE_TLS = config('EMAIL_USE_TLS', default=True, cast=bool)
EMAIL_HOST_USER = config('EMAIL_HOST_USER', default='')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD', default='')

# Login/Logout URLs
LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/dashboard/'
LOGOUT_REDIRECT_URL = '/login/'

# Security Settings
CORS_ALLOW_ALL_ORIGINS = DEBUG  # Solo para desarrollo
if DEBUG:
    CORS_ALLOWED_ORIGINS = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:8000",
        "http://127.0.0.1:8000",
    ]
else:
    CORS_ALLOWED_ORIGINS = [
        "https://app.iticore.com",
    ]

# CSRF Settings
CSRF_TRUSTED_ORIGINS = [
    "https://app.iticore.com",
    "http://localhost:8000",
    "http://127.0.0.1:8000",
]

# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': BASE_DIR / 'logs' / 'itico.log',
            'formatter': 'verbose',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'itico': {
            'handlers': ['file', 'console'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}

# Crear directorio de logs si no existe
LOGS_DIR = BASE_DIR / 'logs'
LOGS_DIR.mkdir(exist_ok=True)

# Debug Toolbar (solo para desarrollo)
if DEBUG and not config('DISABLE_DEBUG_TOOLBAR', default=False, cast=bool):
    INSTALLED_APPS += ['debug_toolbar']
    MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware']
    INTERNAL_IPS = ['127.0.0.1', 'localhost']

# =============================================================================
# PRODUCTION SETTINGS
# =============================================================================

# Static files configuration for production
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Security settings for production
if not DEBUG:
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    X_FRAME_OPTIONS = 'DENY'
    
    # Only enable HTTPS settings in actual production (not local testing)
    IS_PRODUCTION = config('IS_PRODUCTION', default=False, cast=bool)
    
    if IS_PRODUCTION:
        SECURE_HSTS_SECONDS = 31536000
        SECURE_HSTS_INCLUDE_SUBDOMAINS = True
        SECURE_HSTS_PRELOAD = True
        SECURE_SSL_REDIRECT = True
        SESSION_COOKIE_SECURE = True
        CSRF_COOKIE_SECURE = True
