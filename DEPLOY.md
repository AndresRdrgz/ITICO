# Guía de Despliegue en Render para ITICO

Este documento describe cómo desplegar la aplicación ITICO (Portal Interno de Contrapartes) en Render.

## Archivos de Configuración Creados

### 1. `render.yaml`
Archivo de configuración Blueprint que define todos los servicios necesarios:
- **Web Service**: Aplicación Django principal
- **Worker Service**: Procesador de tareas Celery
- **Beat Service**: Programador de tareas Celery
- **Redis Service**: Cola de mensajes para Celery
- **PostgreSQL Database**: Base de datos principal

### 2. Dependencias Actualizadas
Se agregaron las siguientes dependencias a `requirements.txt`:
- `gunicorn==21.2.0` - Servidor WSGI para producción
- `psycopg2-binary==2.9.9` - Driver PostgreSQL
- `whitenoise==6.6.0` - Servir archivos estáticos
- `dj-database-url==2.1.0` - Configuración de base de datos desde URL
- `django-celery-beat==2.5.0` - Programador de tareas Celery

### 3. Configuración de Producción
Se actualizó `itico/settings.py` con:
- Configuración de base de datos usando `dj-database-url`
- Middleware WhiteNoise para archivos estáticos
- Configuraciones de seguridad para producción
- Soporte para variables de entorno

## Pasos para Desplegar

### 1. Preparar el Repositorio
```bash
# Asegúrate de que todos los cambios estén commitados
git add .
git commit -m "Add Render deployment configuration"
git push origin main
```

### 2. Crear Blueprint en Render
1. Ve a [Render Dashboard](https://dashboard.render.com)
2. Haz clic en "New +" y selecciona "Blueprint"
3. Conecta tu repositorio GitHub
4. Render detectará automáticamente el archivo `render.yaml`
5. Revisa la configuración y haz clic en "Apply"

### 3. Configurar Variables de Entorno
Una vez desplegado, configura las siguientes variables en Render:

#### Variables Requeridas:
- `EMAIL_HOST_USER`: Tu email para notificaciones
- `EMAIL_HOST_PASSWORD`: Contraseña de aplicación de Gmail
- `MAKITO_API_KEY`: Clave API para integración Makito
- `AI_SERVICE_KEY`: Clave para servicio de IA

#### Variables Opcionales (ya configuradas por defecto):
- `SECRET_KEY`: Se genera automáticamente
- `DEBUG`: false
- `ALLOWED_HOSTS`: .onrender.com
- `DATABASE_URL`: Se configura automáticamente desde PostgreSQL
- `REDIS_URL`: Se configura automáticamente desde Redis

### 4. Servicios que se Crearán
1. **itico-web**: Aplicación web principal
2. **itico-worker**: Procesador de tareas en segundo plano
3. **itico-beat**: Programador de tareas periódicas
4. **itico-redis**: Servicio Redis para colas
5. **itico-db**: Base de datos PostgreSQL

## Configuración Local

### 1. Archivo .env
Copia `.env.example` a `.env` y configura las variables para desarrollo local:
```bash
cp .env.example .env
```

### 2. Variables Importantes para Desarrollo
```env
DEBUG=True
SECRET_KEY=tu-clave-secreta-local
DATABASE_URL=sqlite:///db.sqlite3
REDIS_URL=redis://localhost:6379/0
```

## Comandos de Desarrollo

### Ejecutar localmente
```bash
# Activar entorno virtual
source .venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt

# Migraciones
python manage.py migrate

# Crear superusuario
python manage.py createsuperuser

# Ejecutar servidor
python manage.py runserver
```

### Celery (en terminales separadas)
```bash
# Worker
celery -A itico worker --loglevel=info

# Beat
celery -A itico beat --loglevel=info --scheduler django_celery_beat.schedulers:DatabaseScheduler
```

## Monitoreo y Logs

### En Render:
1. Ve a tu dashboard de servicios
2. Selecciona cada servicio para ver logs
3. Usa la pestaña "Events" para ver el historial de despliegues

### Logs de la aplicación:
- Los logs se escriben en `logs/itico.log` (configurado en settings)
- En producción, usa los logs de Render para monitoreo

## Solución de Problemas

### Error de Migraciones
Si hay problemas con migraciones en el primer despliegue:
1. Ve al servicio web en Render
2. Usa "Manual Deploy" para ejecutar solo: `python manage.py migrate`

### Error de Archivos Estáticos
Si los archivos estáticos no se cargan:
1. Verifica que WhiteNoise esté en MIDDLEWARE
2. Ejecuta: `python manage.py collectstatic --noinput`

### Error de Celery
Si los workers no se conectan:
1. Verifica que Redis esté ejecutándose
2. Revisa las variables de entorno REDIS_URL

## URLs del Proyecto Desplegado

Una vez desplegado, tu aplicación estará disponible en:
- URL principal: `https://itico-web.onrender.com`
- Admin Django: `https://itico-web.onrender.com/admin/`
- API: `https://itico-web.onrender.com/api/`

## Características de Producción

### Seguridad
- HTTPS forzado
- Cookies seguras
- Headers de seguridad configurados
- Variables de entorno para datos sensibles

### Performance
- Archivos estáticos comprimidos (WhiteNoise)
- Conexiones de base de datos persistentes
- Redis para cache y colas

### Escalabilidad
- Workers Celery separados
- Base de datos PostgreSQL
- Posibilidad de escalar servicios independientemente

## Mantenimiento

### Actualizaciones
1. Haz cambios en tu código local
2. Commit y push a GitHub
3. Render desplegará automáticamente

### Backups
- PostgreSQL en Render incluye backups automáticos
- Archivos media se almacenan en el servicio web

### Monitoreo
- Configura alertas en Render
- Revisa logs regularmente
- Monitorea uso de recursos
