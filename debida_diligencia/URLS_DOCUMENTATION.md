# Documentación de URLs.py - Aplicación Debida Diligencia

## Descripción General

El archivo `urls.py` define todas las rutas URL de la aplicación debida_diligencia, organizadas por funcionalidad y siguiendo un patrón RESTful. Incluye rutas para gestión del proceso de debida diligencia, análisis y búsquedas, funcionalidades especializadas como calendario y reportes, y endpoints API para integración con sistemas externos como RPA (Makito).

## Estructura de URLs

### 1. Configuración Base

```python
"""
URLs para la aplicación de debida diligencia
"""
from django.urls import path
from . import views

app_name = 'debida_diligencia'
```

**Características**:
- **Namespace**: `debida_diligencia` para evitar conflictos
- **Importación**: Vistas importadas desde el módulo views
- **Organización**: Rutas agrupadas por funcionalidad

### 2. Gestión Principal de Debidas Diligencias

```python
# Lista de debidas diligencias
path('', views.DebidaDiligenciaListView.as_view(), name='lista'),
path('<int:pk>/', views.DebidaDiligenciaDetailView.as_view(), name='detalle'),
```

**Patrón de URLs**:
- **Lista**: `/` - Lista todas las debidas diligencias (URL raíz)
- **Detalle**: `/<id>/` - Vista detallada de debida diligencia

**Parámetros**:
- `<int:pk>`: ID de la debida diligencia
- **Nombres**: `lista`, `detalle`

**Características Especiales**:
- **URL Raíz**: La lista de debidas diligencias es la URL principal
- **RESTful**: Sigue convenciones REST
- **Jerarquía**: URLs anidadas para recursos relacionados

### 3. Solicitud de Nueva Debida Diligencia

```python
# Solicitar nueva debida diligencia
path('solicitar/<int:miembro_pk>/', views.SolicitarDDView.as_view(), name='solicitar'),
```

**Patrón de URLs**:
- **Solicitar**: `/solicitar/<miembro_id>/` - Formulario de solicitud para miembro específico

**Parámetros**:
- `<int:miembro_pk>`: ID del miembro para evaluar
- **Nombres**: `solicitar`

**Características Especiales**:
- **URL Anidada**: Miembro específico en la URL
- **Acción Específica**: Solicitud de nueva DD
- **Contexto**: Miembro pre-seleccionado

### 4. Gestión del Proceso de Trabajo

```python
# Gestión de proceso
path('<int:pk>/revisar/', views.RevisarDDView.as_view(), name='revisar'),
path('<int:pk>/aprobar/', views.AprobarDDView.as_view(), name='aprobar'),
path('<int:pk>/rechazar/', views.RechazarDDView.as_view(), name='rechazar'),
```

**Patrón de URLs**:
- **Revisar**: `/<dd_id>/revisar/` - Formulario de revisión de resultados
- **Aprobar**: `/<dd_id>/aprobar/` - Confirmación de aprobación
- **Rechazar**: `/<dd_id>/rechazar/` - Confirmación de rechazo

**Parámetros**:
- `<int:pk>`: ID de la debida diligencia
- **Nombres**: `revisar`, `aprobar`, `rechazar`

**Características Especiales**:
- **Flujo de Trabajo**: URLs que representan el flujo del proceso
- **Acciones Específicas**: Cada URL representa una acción del proceso
- **Jerarquía**: Acciones anidadas bajo la DD específica

### 5. Búsquedas y Análisis

```python
# Búsquedas y análisis
path('<int:pk>/busquedas/', views.BusquedaListView.as_view(), name='busquedas'),
path('busquedas/<int:pk>/', views.BusquedaDetailView.as_view(), name='busqueda_detalle'),
path('<int:pk>/analisis-ia/', views.AnalisisIAView.as_view(), name='analisis_ia'),
```

**Patrón de URLs**:
- **Lista de Búsquedas**: `/<dd_id>/busquedas/` - Búsquedas de una DD específica
- **Detalle de Búsqueda**: `/busquedas/<busqueda_id>/` - Detalle de búsqueda específica
- **Análisis IA**: `/<dd_id>/analisis-ia/` - Análisis de IA de una DD

**Parámetros**:
- `<int:pk>`: ID de la debida diligencia o búsqueda
- **Nombres**: `busquedas`, `busqueda_detalle`, `analisis_ia`

**Características Especiales**:
- **URLs Anidadas**: Búsquedas anidadas bajo DD
- **URLs Independientes**: Detalle de búsqueda independiente
- **Funcionalidad Específica**: Análisis IA como sub-recurso

### 6. Funcionalidades Especializadas

```python
# Calendario
path('calendario/', views.CalendarioDDView.as_view(), name='calendario'),

# Reportes
path('reportes/', views.ReportesDDView.as_view(), name='reportes'),
```

**Patrón de URLs**:
- **Calendario**: `/calendario/` - Vista de calendario con fechas importantes
- **Reportes**: `/reportes/` - Reportes estadísticos y métricas

**Parámetros**:
- **Nombres**: `calendario`, `reportes`

**Características Especiales**:
- **Funcionalidades Especializadas**: No siguen patrón CRUD
- **URLs Descriptivas**: Indican claramente la funcionalidad
- **Acceso Directo**: URLs simples para funcionalidades comunes

### 7. API Endpoints para Integración

```python
# API endpoints para integración con RPA
path('api/webhook/makito/', views.MakitoWebhookView.as_view(), name='makito_webhook'),
path('api/resultado/<int:dd_pk>/', views.RecibirResultadoView.as_view(), name='recibir_resultado'),
```

**Patrón de URLs**:
- **Webhook Makito**: `/api/webhook/makito/` - Endpoint para webhooks del sistema RPA
- **Recibir Resultado**: `/api/resultado/<dd_id>/` - Endpoint para recibir resultados de DD

**Parámetros**:
- `<int:dd_pk>`: ID de la debida diligencia
- **Nombres**: `makito_webhook`, `recibir_resultado`

**Características Especiales**:
- **Namespace API**: URLs bajo `/api/` para endpoints de integración
- **Webhooks**: Endpoint específico para notificaciones externas
- **Integración**: URLs para comunicación con sistemas RPA

## Patrones de Diseño Utilizados

### 1. RESTful URLs
- **Recursos**: URLs representan recursos (DD, búsquedas, análisis)
- **Verbos HTTP**: GET, POST, PUT, DELETE
- **Jerarquía**: Recursos anidados bajo padres
- **Consistencia**: Patrones consistentes

### 2. Hierarchical URLs
- **Anidamiento**: Recursos anidados bajo padres
- **Jerarquía**: Relaciones padre-hijo claras
- **Contexto**: Contexto implícito en URL
- **Navegación**: Navegación intuitiva

### 3. Action-Based URLs
- **Acciones**: URLs que representan acciones específicas
- **Flujo de Trabajo**: Proceso estructurado de DD
- **Estados**: Transiciones de estado del proceso
- **Funcionalidad**: Acciones específicas del dominio

### 4. API Pattern
- **Endpoints API**: URLs específicas para integración
- **Webhooks**: Comunicación asíncrona
- **Integración**: Con sistemas externos
- **Separación**: APIs separadas de vistas web

## Consideraciones de Seguridad

### 1. Autenticación
- **Login Required**: Todas las vistas requieren autenticación
- **Verificación de Usuario**: Usuario autenticado
- **Redirección**: Redirección a login si no autenticado
- **Sesión**: Manejo de sesiones

### 2. Autorización
- **Permisos**: Verificación de permisos por usuario
- **Acceso a Recursos**: Control de acceso a recursos
- **Validación**: Validación de parámetros de URL
- **Protección**: Protección contra acceso no autorizado

### 3. Validación
- **Parámetros**: Validación de parámetros de URL
- **Tipos**: Validación de tipos de datos
- **Rangos**: Validación de rangos de valores
- **Sanitización**: Sanitización de entrada

### 4. API Security
- **Webhooks**: Validación de origen de webhooks
- **APIs**: Autenticación de endpoints API
- **Tokens**: Tokens de autenticación
- **Rate Limiting**: Limitación de velocidad

## Consideraciones de Rendimiento

### 1. Caché
- **Caché de URLs**: Caché de patrones de URL
- **Caché de Vistas**: Caché de vistas frecuentes
- **Invalidación**: Invalidación inteligente
- **Optimización**: Optimización de consultas

### 2. Paginación
- **Listas Paginadas**: Para grandes datasets
- **Navegación**: Navegación eficiente
- **Carga**: Carga bajo demanda
- **Rendimiento**: Mejora de rendimiento

### 3. AJAX
- **Operaciones Asíncronas**: Sin recarga de página
- **Respuestas Rápidas**: Respuestas inmediatas
- **UX**: Experiencia de usuario mejorada
- **Eficiencia**: Eficiencia del servidor

### 4. Optimización
- **Consultas**: Consultas optimizadas
- **Índices**: Índices de base de datos
- **Lazy Loading**: Carga diferida
- **Compresión**: Compresión de respuestas

## Mantenimiento

### 1. Documentación
- **Comentarios**: Comentarios en código
- **README**: Documentación de usuario
- **API Docs**: Documentación de API
- **Changelog**: Historial de cambios

### 2. Testing
- **Unit Tests**: Tests de URLs
- **Integration Tests**: Tests de integración
- **URL Tests**: Tests de patrones de URL
- **Regression Tests**: Tests de regresión

### 3. Refactoring
- **Separación**: Separación de responsabilidades
- **Reutilización**: Reutilización de patrones
- **Optimización**: Optimización continua
- **Estandarización**: Estándares de código

### 4. Versionado
- **Versionado**: Versionado de URLs
- **Compatibilidad**: Compatibilidad hacia atrás
- **Migración**: Migración de URLs
- **Deprecación**: Deprecación controlada

## Ejemplos de Uso

### 1. Navegación Básica
```python
# Lista de debidas diligencias
reverse('debida_diligencia:lista')

# Detalle de debida diligencia
reverse('debida_diligencia:detalle', kwargs={'pk': 1})

# Solicitar nueva DD para miembro
reverse('debida_diligencia:solicitar', kwargs={'miembro_pk': 1})
```

### 2. Flujo de Proceso
```python
# Revisar debida diligencia
reverse('debida_diligencia:revisar', kwargs={'pk': 1})

# Aprobar debida diligencia
reverse('debida_diligencia:aprobar', kwargs={'pk': 1})

# Rechazar debida diligencia
reverse('debida_diligencia:rechazar', kwargs={'pk': 1})
```

### 3. Análisis y Búsquedas
```python
# Búsquedas de una DD
reverse('debida_diligencia:busquedas', kwargs={'pk': 1})

# Detalle de búsqueda específica
reverse('debida_diligencia:busqueda_detalle', kwargs={'pk': 1})

# Análisis IA de una DD
reverse('debida_diligencia:analisis_ia', kwargs={'pk': 1})
```

### 4. Funcionalidades Especializadas
```python
# Calendario
reverse('debida_diligencia:calendario')

# Reportes
reverse('debida_diligencia:reportes')
```

### 5. API Endpoints
```python
# Webhook de Makito
reverse('debida_diligencia:makito_webhook')

# Recibir resultado de DD
reverse('debida_diligencia:recibir_resultado', kwargs={'dd_pk': 1})
```

## Mejores Prácticas

### 1. Naming
- **Descriptivo**: Nombres claros y descriptivos
- **Consistente**: Patrones consistentes
- **Legible**: URLs legibles por humanos
- **SEO Friendly**: Amigables para SEO

### 2. Estructura
- **Jerárquica**: Estructura jerárquica clara
- **RESTful**: Sigue convenciones REST
- **Lógica**: Organización lógica
- **Escalable**: Fácil de escalar

### 3. Mantenimiento
- **Documentación**: Documentación completa
- **Testing**: Tests exhaustivos
- **Refactoring**: Refactoring regular
- **Versionado**: Versionado controlado

### 4. Seguridad
- **Autenticación**: Autenticación requerida
- **Autorización**: Control de acceso
- **Validación**: Validación de entrada
- **Protección**: Protección contra ataques

## Flujo de URLs del Proceso

### 1. Solicitud de DD
```
1. /debida-diligencia/solicitar/<miembro_id>/  # Formulario de solicitud
2. POST → Crear DD → Redirect a detalle
3. /debida-diligencia/<dd_id>/  # Vista de detalle
```

### 2. Proceso de Trabajo
```
1. /debida-diligencia/<dd_id>/  # Estado: pendiente
2. Webhook → /api/webhook/makito/  # Estado: en_proceso
3. /debida-diligencia/<dd_id>/  # Estado: completada
4. /debida-diligencia/<dd_id>/revisar/  # Revisión de resultados
5. /debida-diligencia/<dd_id>/aprobar/  # Aprobación
6. /debida-diligencia/<dd_id>/  # Estado: aprobada
```

### 3. Análisis y Búsquedas
```
1. /debida-diligencia/<dd_id>/busquedas/  # Lista de búsquedas
2. /debida-diligencia/busquedas/<busqueda_id>/  # Detalle de búsqueda
3. /debida-diligencia/<dd_id>/analisis-ia/  # Análisis de IA
```

### 4. Funcionalidades Adicionales
```
1. /debida-diligencia/calendario/  # Vista de calendario
2. /debida-diligencia/reportes/  # Reportes estadísticos
```

## Integración con Sistemas Externos

### 1. Makito RPA
- **Webhook**: `/api/webhook/makito/` para notificaciones
- **Resultados**: `/api/resultado/<dd_id>/` para recibir datos
- **Autenticación**: Validación de origen
- **Procesamiento**: Asíncrono

### 2. Sistemas de IA
- **Análisis**: Integración con servicios de IA
- **Resultados**: Almacenamiento en formato JSON
- **Confianza**: Niveles de confianza del análisis
- **Palabras Clave**: Detección automática

### 3. Notificaciones
- **Estados**: Notificaciones por cambio de estado
- **Aprobaciones**: Notificaciones de decisiones
- **Alertas**: Alertas por fechas importantes
- **Reportes**: Notificaciones de reportes
