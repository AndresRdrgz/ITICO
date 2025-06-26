# ITICO - Instalación y Configuración

## 🚀 Inicio Rápido

El entorno ya está configurado y listo para usar. Sigue estos pasos para ejecutar la aplicación:

### 1. Activar el servidor de desarrollo

```bash
cd /Users/andresrdrgz_/Documents/GitHub/ITICO
.venv/bin/python manage.py runserver
```

### 2. Acceder a la aplicación

Abre tu navegador y visita: http://127.0.0.1:8000/

### 3. Credenciales de acceso

**Usuario Administrador:**
- Usuario: `admin`
- Contraseña: [la que configuraste durante la instalación]

**Usuario de Prueba (Oficial de Cumplimiento):**
- Usuario: `gabriela`
- Contraseña: `test123`

**Panel de Administración Django:**
- URL: http://127.0.0.1:8000/admin/
- Usar credenciales de administrador

---

## 📁 Estructura del Proyecto

```
ITICO/
├── itico/                 # Configuración principal del proyecto
│   ├── settings.py        # Configuraciones de Django
│   ├── urls.py           # URLs principales
│   ├── celery.py         # Configuración de Celery
│   └── wsgi.py           # WSGI para producción
├── contrapartes/         # App de gestión de contrapartes
├── debida_diligencia/    # App de procesos de DD
├── notificaciones/       # App de sistema de notificaciones
├── dashboard/            # App del dashboard principal
├── api/                  # App de APIs REST
├── templates/            # Plantillas HTML globales
├── static/               # Archivos estáticos (CSS, JS, imágenes)
├── media/                # Archivos subidos por usuarios
├── requirements.txt      # Dependencias de Python
├── .env                  # Variables de entorno
└── manage.py            # Script de gestión de Django
```

---

## 🛠️ Comandos Útiles

### Gestión de la Base de Datos

```bash
# Crear migraciones
.venv/bin/python manage.py makemigrations

# Aplicar migraciones
.venv/bin/python manage.py migrate

# Crear superusuario
.venv/bin/python manage.py createsuperuser

# Cargar datos de prueba
.venv/bin/python manage.py cargar_datos_prueba

# Resetear y cargar datos de prueba
.venv/bin/python manage.py cargar_datos_prueba --reset
```

### Servidor de Desarrollo

```bash
# Ejecutar servidor en puerto 8000
.venv/bin/python manage.py runserver

# Ejecutar en puerto específico
.venv/bin/python manage.py runserver 8080

# Ejecutar accesible desde la red local
.venv/bin/python manage.py runserver 0.0.0.0:8000
```

### Celery (Tareas Asincrónicas)

```bash
# Ejecutar worker de Celery
.venv/bin/python -m celery -A itico worker --loglevel=info

# Ejecutar Beat (programador de tareas)
.venv/bin/python -m celery -A itico beat --loglevel=info

# Monitor de Celery (Flower)
.venv/bin/python -m celery -A itico flower
```

### Testing

```bash
# Ejecutar todos los tests
.venv/bin/python manage.py test

# Ejecutar tests de una app específica
.venv/bin/python manage.py test contrapartes

# Ejecutar con cobertura
coverage run --source='.' manage.py test
coverage report
coverage html
```

---

## 🔧 Configuración Avanzada

### Variables de Entorno

Edita el archivo `.env` para configurar:

```env
# Django Settings
SECRET_KEY=tu-clave-secreta-aqui
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database (SQLite por defecto, cambiar para PostgreSQL)
DB_ENGINE=django.db.backends.postgresql
DB_NAME=itico_db
DB_USER=itico_user
DB_PASSWORD=password
DB_HOST=localhost
DB_PORT=5432

# Redis para Celery
REDIS_URL=redis://localhost:6379/0

# Integración RPA Makito
MAKITO_API_URL=http://localhost:8080/api
MAKITO_API_KEY=tu-api-key-makito

# Servicio de IA
AI_SERVICE_URL=http://localhost:8081/api
AI_SERVICE_KEY=tu-ai-service-key

# Email
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=tu-email@gmail.com
EMAIL_HOST_PASSWORD=tu-password-email
```

### Base de Datos PostgreSQL

Para usar PostgreSQL en lugar de SQLite:

1. Instalar PostgreSQL
2. Crear base de datos y usuario
3. Actualizar variables en `.env`
4. Instalar psycopg2: `pip install psycopg2-binary`

### Redis (para Celery)

Para habilitar tareas asincrónicas:

1. Instalar Redis: `brew install redis` (macOS)
2. Ejecutar Redis: `redis-server`
3. Configurar REDIS_URL en `.env`

---

## 📋 Funcionalidades Implementadas

### ✅ Completadas

- [x] **Modelos de Datos**: Contrapartes, Miembros, Debida Diligencia, Búsquedas, Notificaciones
- [x] **Django Admin**: Interfaz administrativa completa
- [x] **Autenticación**: Sistema de login/logout
- [x] **Dashboard**: Panel principal con estadísticas
- [x] **Templates Base**: Diseño responsive con Bootstrap
- [x] **Estilos CSS**: Paleta de colores según especificaciones
- [x] **Datos de Prueba**: Comando para cargar datos de ejemplo
- [x] **Estructura URLs**: Rutas organizadas por aplicación
- [x] **Configuración Celery**: Para tareas asincrónicas
- [x] **API REST**: Endpoints básicos con Django REST Framework

### 🚧 En Desarrollo (Próximos Pasos)

- [ ] **Vistas Funcionales**: Implementar CRUD completo para contrapartes
- [ ] **Proceso DD**: Lógica de solicitud y seguimiento de debida diligencia
- [ ] **Integración RPA**: Conexión con sistema Makito
- [ ] **Motor IA**: Análisis automatizado de documentos
- [ ] **Sistema Notificaciones**: Emails y notificaciones en tiempo real
- [ ] **Calendario**: Vista de próximas debidas diligencias
- [ ] **Reportes**: Generación de informes y exportación
- [ ] **API Completa**: Endpoints REST completos
- [ ] **Tests**: Suite de pruebas automatizadas
- [ ] **Documentación**: API docs con Swagger

---

## 🎯 Siguientes Pasos de Desarrollo

### 1. Implementar Vistas CRUD
```bash
# Desarrollar vistas funcionales para:
# - Lista, crear, editar, eliminar contrapartes
# - Gestión de miembros
# - Formularios con validación
```

### 2. Sistema de Debida Diligencia
```bash
# Implementar:
# - Solicitud de DD
# - Integración con RPA Makito
# - Seguimiento de estados
# - Carga de resultados
```

### 3. Motor de IA
```bash
# Integrar:
# - Análisis de documentos PDF
# - Detección de palabras clave
# - Clasificación de riesgos
# - Generación de resúmenes
```

### 4. Notificaciones
```bash
# Desarrollar:
# - Sistema de notificaciones en tiempo real
# - Envío de emails
# - Configuración por usuario
# - Historial de notificaciones
```

---

## 🆘 Resolución de Problemas

### Error: Módulo no encontrado
```bash
# Verificar que el entorno virtual está activado
source .venv/bin/activate

# Reinstalar dependencias
pip install -r requirements.txt
```

### Error: Base de datos bloqueada
```bash
# Eliminar archivo de base de datos
rm db.sqlite3

# Recrear migraciones
.venv/bin/python manage.py migrate
.venv/bin/python manage.py cargar_datos_prueba
```

### Error: Puerto en uso
```bash
# Cambiar puerto
.venv/bin/python manage.py runserver 8080

# O matar proceso en puerto 8000
sudo lsof -t -i tcp:8000 | xargs kill -9
```

---

## 📞 Soporte

Para soporte técnico o preguntas sobre el desarrollo, contactar:

- **Andrés Rodríguez** - Desarrollador Principal
- **Darío Osorio** - Integración y Servidor Web

---

## 📄 Licencia

Este proyecto es propiedad de **App Pacífico** y está destinado únicamente para uso interno de la empresa.
