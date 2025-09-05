"""
Configuración de Django para el proyecto ITICO.

Portal Interno de Contrapartes – App Pacífico (Cotizador Web)
Sistema de gestión de contrapartes con debida diligencia automatizada.

ESTRUCTURA DE CONFIGURACIÓN:
1. Configuración básica (SECRET_KEY, DEBUG, ALLOWED_HOSTS)
2. Base de datos (PostgreSQL para producción, SQLite para desarrollo)
3. Aplicaciones instaladas (Django apps + apps personalizadas)
4. Middleware (seguridad, sesiones, CORS, HTMX)
5. Templates y archivos estáticos/media
6. Configuraciones específicas de ITICO (Celery, APIs externas)
7. Configuraciones de seguridad y producción

Para más información sobre configuración de Django:
https://docs.djangoproject.com/en/5.0/topics/settings/
"""

from pathlib import Path
from decouple import config
import os
import dj_database_url

# =============================================================================
# CONFIGURACIÓN BÁSICA DE DJANGO
# =============================================================================

# Directorio base del proyecto
BASE_DIR = Path(__file__).resolve().parent.parent

# Clave secreta para firmar cookies y tokens
# IMPORTANTE: Cambiar en producción usando variable de entorno SECRET_KEY
SECRET_KEY = config('SECRET_KEY', default='django-insecure-change-this-in-production')

# Modo debug - SOLO habilitar en desarrollo
# En producción debe estar en False
DEBUG = False
# =============================================================================
# CONFIGURACIÓN DE BASE DE DATOS
# =============================================================================

# Configuración de base de datos usando dj_database_url
# Formato: postgresql://usuario:contraseña@host:puerto/nombre_db
# Para cambiar la configuración, usar variable de entorno DATABASE_URL

if DEBUG:
    # Base de datos para desarrollo
    DATABASES = {
        'default': dj_database_url.config(
            default='postgresql://postgres:FP.h05t1l3@localhost:5432/itico',
            conn_max_age=600,  # Mantener conexión por 10 minutos
        )
    }
else:
    # Base de datos para producción
    DATABASES = {
        'default': dj_database_url.config(
            default='postgresql://postgres:FP.h05t1l3@localhost:5432/itico',
            conn_max_age=600,
        )
    }

# Configuraciones alternativas comentadas:
# SQLite para desarrollo local (más simple)
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

# Hosts permitidos para el servidor
if DEBUG:
    ALLOWED_HOSTS = ['*']  # Permitir todos los hosts en desarrollo
else:
    ALLOWED_HOSTS = [
        'app.iticore.com',  # Dominio de producción
        'localhost',        # Para pruebas locales
        '127.0.0.1',       # Para pruebas locales
    ]

# =============================================================================
# APLICACIONES INSTALADAS
# =============================================================================

INSTALLED_APPS = [
    # Aplicaciones core de Django
    'django.contrib.admin',        # Panel de administración
    'django.contrib.auth',         # Sistema de autenticación
    'django.contrib.contenttypes', # Framework de tipos de contenido
    'django.contrib.sessions',     # Manejo de sesiones
    'django.contrib.messages',     # Sistema de mensajes
    'django.contrib.staticfiles',  # Manejo de archivos estáticos
    
    # Aplicaciones de terceros
    'rest_framework',              # Django REST Framework para APIs
    'corsheaders',                # Manejo de CORS para APIs
    'crispy_forms',               # Formularios con mejor presentación
    'crispy_tailwind',            # Integración con Tailwind CSS
    'django_htmx',                # Soporte para HTMX (interactividad)
    'django_extensions',          # Herramientas adicionales de Django
    
    # Aplicaciones locales del proyecto ITICO
    'contrapartes',               # Gestión de contrapartes
    'debida_diligencia',          # Procesos de debida diligencia
    'notificaciones',             # Sistema de notificaciones
    'dashboard',                  # Panel principal
    'api',                        # APIs REST
    'usuarios',                   # Gestión de usuarios
    'django_celery_beat',         # Tareas periódicas con Celery
]

# =============================================================================
# CONFIGURACIÓN DE APLICACIONES DE TERCEROS
# =============================================================================

# Configuración de Crispy Forms (formularios con mejor presentación)
CRISPY_ALLOWED_TEMPLATE_PACKS = "tailwind"  # Usar Tailwind CSS
CRISPY_TEMPLATE_PACK = "tailwind"

# Configuración de Django REST Framework (APIs)
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,  # 20 elementos por página
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',  # Requiere autenticación
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',  # Autenticación por sesión
        'rest_framework.authentication.BasicAuthentication',    # Autenticación básica
    ],
}

# =============================================================================
# MIDDLEWARE (PROCESAMIENTO DE PETICIONES)
# =============================================================================

MIDDLEWARE = [
    # Seguridad
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Servir archivos estáticos
    
    # Sesiones y autenticación
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    
    # CORS y comunicación
    'corsheaders.middleware.CorsMiddleware',        # Manejo de CORS
    'django.middleware.common.CommonMiddleware',    # Procesamiento común
    
    # Seguridad web
    'django.middleware.csrf.CsrfViewMiddleware',    # Protección CSRF
    'django.middleware.clickjacking.XFrameOptionsMiddleware',  # Protección clickjacking
    
    # Funcionalidades adicionales
    'django_htmx.middleware.HtmxMiddleware',        # Soporte HTMX
    'django.contrib.messages.middleware.MessageMiddleware',  # Sistema de mensajes
]

# Configuración de URLs principal
ROOT_URLCONF = 'itico.urls'

# =============================================================================
# CONFIGURACIÓN DE TEMPLATES
# =============================================================================

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],  # Directorio global de templates
        'APP_DIRS': True,  # Buscar templates en cada app
        'OPTIONS': {
            'context_processors': [
                # Procesadores de contexto disponibles en todos los templates
                'django.template.context_processors.debug',      # Información de debug
                'django.template.context_processors.request',    # Objeto request
                'django.contrib.auth.context_processors.auth',   # Usuario autenticado
                'django.contrib.messages.context_processors.messages',  # Mensajes
            ],
        },
    },
]

# Aplicación WSGI para servidores web
WSGI_APPLICATION = 'itico.wsgi.application'


# =============================================================================
# VALIDACIÓN DE CONFIGURACIÓN DE BASE DE DATOS
# =============================================================================

# Verificar configuración de base de datos al iniciar
db_config = DATABASES['default']
db_engine = db_config.get('ENGINE', 'Unknown')
db_name = db_config.get('NAME', 'Unknown')

print(f"[ITICO] Database Engine: {db_engine}")
print(f"[ITICO] Database Name: {db_name}")

# Validar que se use PostgreSQL en producción
if not DEBUG and 'postgresql' not in db_engine:
    print(f"[ITICO] WARNING: Not using PostgreSQL in production! Engine: {db_engine}")
elif not DEBUG:
    print(f"[ITICO] PostgreSQL configured correctly for production")


# =============================================================================
# VALIDACIÓN DE CONTRASEÑAS
# =============================================================================

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

# =============================================================================
# INTERNACIONALIZACIÓN
# =============================================================================

LANGUAGE_CODE = 'es-pa'  # Español Panamá
TIME_ZONE = config('TIME_ZONE', default='America/Panama')  # Zona horaria de Panamá
USE_I18N = True   # Habilitar internacionalización
USE_TZ = True     # Usar zona horaria


# =============================================================================
# ARCHIVOS ESTÁTICOS (CSS, JavaScript, Imágenes)
# =============================================================================

STATIC_URL = '/static/'                    # URL para servir archivos estáticos
STATIC_ROOT = BASE_DIR / 'staticfiles'     # Directorio donde se recopilan archivos estáticos

# Directorios donde buscar archivos estáticos
STATICFILES_DIRS = [
    BASE_DIR / 'static',  # Directorio global de archivos estáticos
]

# =============================================================================
# ARCHIVOS MEDIA (Subidas de usuarios)
# =============================================================================

MEDIA_URL = '/media/'                       # URL para servir archivos media
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')  # Directorio donde se almacenan archivos subidos

# Crear directorio media si no existe
os.makedirs(MEDIA_ROOT, exist_ok=True)

# Configuración adicional para archivos media
MEDIA_FILES_MAX_SIZE = 50 * 1024 * 1024  # Tamaño máximo: 50MB

# Extensiones de archivos permitidas para subida
ALLOWED_MEDIA_EXTENSIONS = [
    # Imágenes
    'jpg', 'jpeg', 'png', 'gif', 'bmp', 'svg',
    # Documentos
    'pdf', 'doc', 'docx', 'xls', 'xlsx', 'ppt', 'pptx',
    # Archivos de texto
    'txt', 'csv', 'json', 'xml',
    # Videos
    'mp4', 'avi', 'mov', 'wmv', 'flv', 'webm',
    # Audio
    'mp3', 'wav', 'ogg', 'aac',
    # Archivos comprimidos
    'zip', 'rar', '7z', 'tar', 'gz',
]

# =============================================================================
# CONFIGURACIÓN DE SEGURIDAD PARA ARCHIVOS
# =============================================================================

# Configuración de seguridad para archivos según el entorno
if not DEBUG:
    # Configuración para producción - más restrictiva
    FILE_UPLOAD_MAX_MEMORY_SIZE = 52428800   # 50MB máximo en memoria
    DATA_UPLOAD_MAX_MEMORY_SIZE = 52428800   # 50MB máximo para datos
    FILE_UPLOAD_PERMISSIONS = 0o644          # Permisos de archivo
    FILE_UPLOAD_DIRECTORY_PERMISSIONS = 0o755 # Permisos de directorio
    print(f"File upload permissions set to: {FILE_UPLOAD_PERMISSIONS}")
else:
    # Configuración para desarrollo - más permisiva
    FILE_UPLOAD_MAX_MEMORY_SIZE = 104857600  # 100MB para desarrollo
    DATA_UPLOAD_MAX_MEMORY_SIZE = 104857600  # 100MB para desarrollo
    FILE_UPLOAD_PERMISSIONS = 0o644
    FILE_UPLOAD_DIRECTORY_PERMISSIONS = 0o755
    print(f"Media files max size: {MEDIA_FILES_MAX_SIZE // (1024*1024)}MB")

# =============================================================================
# CONFIGURACIÓN GENERAL DE DJANGO
# =============================================================================

# Tipo de campo de clave primaria por defecto
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# =============================================================================
# CONFIGURACIONES ESPECÍFICAS DE ITICO
# =============================================================================

# =============================================================================
# CELERY (TAREAS ASÍNCRONAS)
# =============================================================================

# Configuración de Celery para tareas en segundo plano
CELERY_BROKER_URL = config('REDIS_URL', default='redis://localhost:6379/0')      # Broker Redis
CELERY_RESULT_BACKEND = config('REDIS_URL', default='redis://localhost:6379/0')  # Backend de resultados
CELERY_ACCEPT_CONTENT = ['application/json']  # Formato de contenido aceptado
CELERY_TASK_SERIALIZER = 'json'               # Serializador de tareas
CELERY_RESULT_SERIALIZER = 'json'             # Serializador de resultados
CELERY_TIMEZONE = TIME_ZONE                   # Zona horaria para tareas

# =============================================================================
# INTEGRACIÓN CON SERVICIOS EXTERNOS
# =============================================================================

# Integración con RPA Makito (automatización de procesos)
MAKITO_API_URL = config('MAKITO_API_URL', default='http://localhost:8080/api')
MAKITO_API_KEY = config('MAKITO_API_KEY', default='')

# Servicio de IA para análisis de documentos
AI_SERVICE_URL = config('AI_SERVICE_URL', default='http://localhost:8081/api')
AI_SERVICE_KEY = config('AI_SERVICE_KEY', default='')

# =============================================================================
# CONFIGURACIÓN DE CORREO ELECTRÓNICO
# =============================================================================

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'  # Backend SMTP
EMAIL_HOST = config('EMAIL_HOST', default='smtp.gmail.com')     # Servidor SMTP
EMAIL_PORT = config('EMAIL_PORT', default=587, cast=int)       # Puerto SMTP
EMAIL_USE_TLS = config('EMAIL_USE_TLS', default=True, cast=bool)  # Usar TLS
EMAIL_HOST_USER = config('EMAIL_HOST_USER', default='')        # Usuario SMTP
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD', default='') # Contraseña SMTP

# =============================================================================
# CONFIGURACIÓN DE AUTENTICACIÓN
# =============================================================================

# URLs de autenticación
LOGIN_URL = '/login/'              # URL de login
LOGIN_REDIRECT_URL = '/dashboard/' # URL después del login exitoso
LOGOUT_REDIRECT_URL = '/login/'    # URL después del logout

# =============================================================================
# CONFIGURACIÓN DE SEGURIDAD
# =============================================================================

# Configuración CORS (Cross-Origin Resource Sharing)
CORS_ALLOW_ALL_ORIGINS = DEBUG  # Solo permitir todos los orígenes en desarrollo
if DEBUG:
    CORS_ALLOWED_ORIGINS = [
        "http://localhost:3000",  # React dev server
        "http://127.0.0.1:3000",
        "http://localhost:8000",  # Django dev server
        "http://127.0.0.1:8000",
    ]
else:
    CORS_ALLOWED_ORIGINS = [
        "https://app.iticore.com",  # Dominio de producción
    ]

# Configuración CSRF (Cross-Site Request Forgery)
CSRF_TRUSTED_ORIGINS = [
    "https://app.iticore.com",  # Dominio de producción
    "http://localhost:8000",    # Desarrollo local
    "http://127.0.0.1:8000",   # Desarrollo local
]

# =============================================================================
# CONFIGURACIÓN DE LOGGING
# =============================================================================

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
            'filename': BASE_DIR / 'logs' / 'itico.log',  # Archivo de log
            'formatter': 'verbose',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',  # Salida a consola
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'itico': {
            'handlers': ['file', 'console'],  # Escribir a archivo y consola
            'level': 'INFO',
            'propagate': True,
        },
    },
}

# Crear directorio de logs si no existe
LOGS_DIR = BASE_DIR / 'logs'
LOGS_DIR.mkdir(exist_ok=True)

# =============================================================================
# HERRAMIENTAS DE DESARROLLO
# =============================================================================

# Debug Toolbar (solo para desarrollo)
if DEBUG and not config('DISABLE_DEBUG_TOOLBAR', default=False, cast=bool):
    INSTALLED_APPS += ['debug_toolbar']  # Agregar debug toolbar
    MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware']  # Middleware
    INTERNAL_IPS = ['127.0.0.1', 'localhost']  # IPs donde mostrar el toolbar

# =============================================================================
# CONFIGURACIONES DE PRODUCCIÓN
# =============================================================================

# Configuración de archivos estáticos para producción
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# =============================================================================
# CONFIGURACIONES DE SEGURIDAD PARA PRODUCCIÓN
# =============================================================================

# Configuraciones de seguridad que solo se aplican cuando DEBUG=False
if not DEBUG:
    # Configuraciones básicas de seguridad
    SECURE_BROWSER_XSS_FILTER = True      # Filtro XSS del navegador
    SECURE_CONTENT_TYPE_NOSNIFF = True    # Prevenir MIME type sniffing
    X_FRAME_OPTIONS = 'DENY'              # Prevenir clickjacking
    
    # Configuraciones HTTPS (solo en producción real)
    IS_PRODUCTION = config('IS_PRODUCTION', default=False, cast=bool)
    
    if IS_PRODUCTION:
        # HTTP Strict Transport Security (HSTS)
        SECURE_HSTS_SECONDS = 31536000        # 1 año
        SECURE_HSTS_INCLUDE_SUBDOMAINS = True # Incluir subdominios
        SECURE_HSTS_PRELOAD = True            # Preload en navegadores
        
        # Redirección HTTPS
        SECURE_SSL_REDIRECT = True            # Redirigir HTTP a HTTPS
        
        # Cookies seguras
        SESSION_COOKIE_SECURE = True          # Cookies de sesión solo HTTPS
        CSRF_COOKIE_SECURE = True             # Cookies CSRF solo HTTPS
