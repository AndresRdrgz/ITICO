# Documentación de URLs.py - Aplicación Contrapartes

## Descripción General

El archivo `urls.py` define todas las rutas URL de la aplicación contrapartes, organizadas por funcionalidad y siguiendo un patrón RESTful. Incluye rutas para CRUD básico, operaciones AJAX, gestión de balance sheets, y funcionalidades especializadas como búsqueda y exportación.

## Estructura de URLs

### 1. Configuración Base

```python
"""
URLs para la aplicación de contrapartes
"""
from django.urls import path
from . import views

app_name = 'contrapartes'
```

**Características**:
- **Namespace**: `contrapartes` para evitar conflictos
- **Importación**: Vistas importadas desde el módulo views
- **Organización**: Rutas agrupadas por funcionalidad

### 2. Gestión de Tipos de Contraparte

```python
# Gestión de tipos de contraparte
path('tipos/', views.TipoContraparteListView.as_view(), name='tipo_lista'),
path('tipos/crear/', views.TipoContraparteCreateView.as_view(), name='tipo_crear'),
path('tipos/<int:pk>/editar/', views.TipoContraparteUpdateView.as_view(), name='tipo_editar'),
path('tipos/<int:pk>/eliminar/', views.TipoContraparteDeleteView.as_view(), name='tipo_eliminar'),
```

**Patrón de URLs**:
- **Lista**: `/tipos/` - Lista todos los tipos
- **Crear**: `/tipos/crear/` - Formulario de creación
- **Editar**: `/tipos/<id>/editar/` - Formulario de edición
- **Eliminar**: `/tipos/<id>/eliminar/` - Confirmación de eliminación

**Parámetros**:
- `<int:pk>`: ID del tipo de contraparte
- **Nombres**: `tipo_lista`, `tipo_crear`, `tipo_editar`, `tipo_eliminar`

### 3. Gestión de Estados de Contraparte

```python
# Gestión de estados de contraparte
path('estados/', views.EstadoContraparteListView.as_view(), name='estado_lista'),
path('estados/crear/', views.EstadoContraparteCreateView.as_view(), name='estado_crear'),
path('estados/<int:pk>/editar/', views.EstadoContraparteUpdateView.as_view(), name='estado_editar'),
path('estados/<int:pk>/eliminar/', views.EstadoContraparteDeleteView.as_view(), name='estado_eliminar'),
```

**Patrón de URLs**:
- **Lista**: `/estados/` - Lista todos los estados
- **Crear**: `/estados/crear/` - Formulario de creación
- **Editar**: `/estados/<id>/editar/` - Formulario de edición
- **Eliminar**: `/estados/<id>/eliminar/` - Confirmación de eliminación

**Parámetros**:
- `<int:pk>`: ID del estado de contraparte
- **Nombres**: `estado_lista`, `estado_crear`, `estado_editar`, `estado_eliminar`

### 4. Gestión de Tipos de Documento

```python
# Gestión de tipos de documento
path('tipos-documento/', views.TipoDocumentoListView.as_view(), name='tipo_documento_lista'),
path('tipos-documento/crear/', views.TipoDocumentoCreateView.as_view(), name='tipo_documento_crear'),
path('tipos-documento/<int:pk>/editar/', views.TipoDocumentoUpdateView.as_view(), name='tipo_documento_editar'),
path('tipos-documento/<int:pk>/eliminar/', views.TipoDocumentoDeleteView.as_view(), name='tipo_documento_eliminar'),
```

**Patrón de URLs**:
- **Lista**: `/tipos-documento/` - Lista todos los tipos de documento
- **Crear**: `/tipos-documento/crear/` - Formulario de creación
- **Editar**: `/tipos-documento/<id>/editar/` - Formulario de edición
- **Eliminar**: `/tipos-documento/<id>/eliminar/` - Confirmación de eliminación

**Parámetros**:
- `<int:pk>`: ID del tipo de documento
- **Nombres**: `tipo_documento_lista`, `tipo_documento_crear`, `tipo_documento_editar`, `tipo_documento_eliminar`

### 5. Gestión de Calificadores

```python
# Gestión de calificadores
path('calificadores/', views.CalificadorListView.as_view(), name='calificador_lista'),
path('calificadores/crear/', views.CalificadorCreateView.as_view(), name='calificador_crear'),
path('calificadores/<int:pk>/editar/', views.CalificadorUpdateView.as_view(), name='calificador_editar'),
path('calificadores/<int:pk>/eliminar/', views.CalificadorDeleteView.as_view(), name='calificador_eliminar'),
```

**Patrón de URLs**:
- **Lista**: `/calificadores/` - Lista todos los calificadores
- **Crear**: `/calificadores/crear/` - Formulario de creación
- **Editar**: `/calificadores/<id>/editar/` - Formulario de edición
- **Eliminar**: `/calificadores/<id>/eliminar/` - Confirmación de eliminación

**Parámetros**:
- `<int:pk>`: ID del calificador
- **Nombres**: `calificador_lista`, `calificador_crear`, `calificador_editar`, `calificador_eliminar`

### 6. Gestión de Outlooks

```python
# Gestión de outlooks
path('outlooks/', views.OutlookListView.as_view(), name='outlook_lista'),
path('outlooks/crear/', views.OutlookCreateView.as_view(), name='outlook_crear'),
path('outlooks/<int:pk>/editar/', views.OutlookUpdateView.as_view(), name='outlook_editar'),
path('outlooks/<int:pk>/eliminar/', views.OutlookDeleteView.as_view(), name='outlook_eliminar'),
```

**Patrón de URLs**:
- **Lista**: `/outlooks/` - Lista todos los outlooks
- **Crear**: `/outlooks/crear/` - Formulario de creación
- **Editar**: `/outlooks/<id>/editar/` - Formulario de edición
- **Eliminar**: `/outlooks/<id>/eliminar/` - Confirmación de eliminación

**Parámetros**:
- `<int:pk>`: ID del outlook
- **Nombres**: `outlook_lista`, `outlook_crear`, `outlook_editar`, `outlook_eliminar`

### 7. Gestión Principal de Contrapartes

```python
# Lista y gestión de contrapartes
path('', views.ContraparteListView.as_view(), name='lista'),
path('crear/', views.ContraparteCreateView.as_view(), name='crear'),
path('<int:pk>/', views.ContraparteDetailView.as_view(), name='detalle'),
path('<int:pk>/editar/', views.ContraparteUpdateView.as_view(), name='editar'),
path('<int:pk>/eliminar/', views.ContraparteDeleteView.as_view(), name='eliminar'),
```

**Patrón de URLs**:
- **Lista**: `/` - Lista todas las contrapartes (URL raíz)
- **Crear**: `/crear/` - Formulario de creación
- **Detalle**: `/<id>/` - Vista detallada de contraparte
- **Editar**: `/<id>/editar/` - Formulario de edición
- **Eliminar**: `/<id>/eliminar/` - Confirmación de eliminación

**Parámetros**:
- `<int:pk>`: ID de la contraparte
- **Nombres**: `lista`, `crear`, `detalle`, `editar`, `eliminar`

**Características Especiales**:
- **URL Raíz**: La lista de contrapartes es la URL principal
- **RESTful**: Sigue convenciones REST
- **Jerarquía**: URLs anidadas para recursos relacionados

### 8. Gestión de Miembros

```python
# Gestión de miembros
path('<int:contraparte_pk>/miembros/crear/', views.MiembroCreateView.as_view(), name='miembro_crear'),
path('<int:contraparte_pk>/miembros/ajax/crear/', views.MiembroCreateAjaxView.as_view(), name='miembro_crear_ajax'),
path('miembros/<int:pk>/', views.MiembroDetailView.as_view(), name='miembro_detalle'),
path('miembros/<int:pk>/editar/', views.MiembroUpdateView.as_view(), name='miembro_editar'),
path('miembros/<int:pk>/eliminar/', views.MiembroDeleteView.as_view(), name='miembro_eliminar'),
```

**Patrón de URLs**:
- **Crear**: `/<contraparte_id>/miembros/crear/` - Formulario de creación
- **Crear AJAX**: `/<contraparte_id>/miembros/ajax/crear/` - Creación via AJAX
- **Detalle**: `/miembros/<id>/` - Vista detallada de miembro
- **Editar**: `/miembros/<id>/editar/` - Formulario de edición
- **Eliminar**: `/miembros/<id>/eliminar/` - Confirmación de eliminación

**Parámetros**:
- `<int:contraparte_pk>`: ID de la contraparte padre
- `<int:pk>`: ID del miembro
- **Nombres**: `miembro_crear`, `miembro_crear_ajax`, `miembro_detalle`, `miembro_editar`, `miembro_eliminar`

**Características Especiales**:
- **URLs Anidadas**: Miembros anidados bajo contrapartes
- **AJAX**: Endpoint específico para operaciones AJAX
- **Jerarquía**: Relación padre-hijo clara

### 9. Gestión de Documentos

```python
# Gestión de documentos
path('<int:contraparte_pk>/documentos/ajax/crear/', views.DocumentoCreateAjaxView.as_view(), name='documento_crear_ajax'),
path('documentos/<int:pk>/ajax/editar/', views.DocumentoUpdateAjaxView.as_view(), name='documento_editar_ajax'),
path('documentos/<int:pk>/eliminar/', views.DocumentoDeleteView.as_view(), name='documento_eliminar'),
```

**Patrón de URLs**:
- **Crear AJAX**: `/<contraparte_id>/documentos/ajax/crear/` - Creación via AJAX
- **Editar AJAX**: `/documentos/<id>/ajax/editar/` - Edición via AJAX
- **Eliminar**: `/documentos/<id>/eliminar/` - Eliminación

**Parámetros**:
- `<int:contraparte_pk>`: ID de la contraparte padre
- `<int:pk>`: ID del documento
- **Nombres**: `documento_crear_ajax`, `documento_editar_ajax`, `documento_eliminar`

**Características Especiales**:
- **Solo AJAX**: Operaciones dinámicas sin recarga
- **URLs Anidadas**: Documentos anidados bajo contrapartes
- **Eliminación Directa**: Eliminación sin AJAX para confirmación

### 10. Gestión de Comentarios

```python
# Gestión de comentarios
path('<int:contraparte_pk>/comentarios/ajax/crear/', views.ComentarioCreateAjaxView.as_view(), name='comentario_crear_ajax'),
path('comentarios/<int:pk>/ajax/editar/', views.ComentarioUpdateAjaxView.as_view(), name='comentario_editar_ajax'),
path('comentarios/<int:pk>/ajax/eliminar/', views.ComentarioDeleteAjaxView.as_view(), name='comentario_eliminar_ajax'),
```

**Patrón de URLs**:
- **Crear AJAX**: `/<contraparte_id>/comentarios/ajax/crear/` - Creación via AJAX
- **Editar AJAX**: `/comentarios/<id>/ajax/editar/` - Edición via AJAX
- **Eliminar AJAX**: `/comentarios/<id>/ajax/eliminar/` - Eliminación via AJAX

**Parámetros**:
- `<int:contraparte_pk>`: ID de la contraparte padre
- `<int:pk>`: ID del comentario
- **Nombres**: `comentario_crear_ajax`, `comentario_editar_ajax`, `comentario_eliminar_ajax`

**Características Especiales**:
- **Solo AJAX**: Todas las operaciones son dinámicas
- **URLs Anidadas**: Comentarios anidados bajo contrapartes
- **Operaciones Rápidas**: Sin confirmaciones adicionales

### 11. Gestión de Fechas de Debida Diligencia

```python
# Fecha DD
path('<int:pk>/fecha-dd/ajax/actualizar/', views.ContraparteFechaDDUpdateView.as_view(), name='fecha_dd_actualizar_ajax'),
```

**Patrón de URLs**:
- **Actualizar AJAX**: `/<contraparte_id>/fecha-dd/ajax/actualizar/` - Actualización via AJAX

**Parámetros**:
- `<int:pk>`: ID de la contraparte
- **Nombres**: `fecha_dd_actualizar_ajax`

**Características Especiales**:
- **Operación Específica**: Solo para actualizar fecha de DD
- **AJAX**: Operación dinámica
- **URL Descriptiva**: Indica claramente la funcionalidad

### 12. Gestión de Calificaciones

```python
# Gestión de calificaciones
path('<int:contraparte_pk>/calificaciones/ajax/crear/', views.CalificacionCreateAjaxView.as_view(), name='calificacion_crear_ajax'),
path('calificaciones/<int:pk>/ajax/editar/', views.CalificacionUpdateAjaxView.as_view(), name='calificacion_editar_ajax'),
path('calificaciones/<int:pk>/ajax/eliminar/', views.CalificacionDeleteAjaxView.as_view(), name='calificacion_eliminar_ajax'),
```

**Patrón de URLs**:
- **Crear AJAX**: `/<contraparte_id>/calificaciones/ajax/crear/` - Creación via AJAX
- **Editar AJAX**: `/calificaciones/<id>/ajax/editar/` - Edición via AJAX
- **Eliminar AJAX**: `/calificaciones/<id>/ajax/eliminar/` - Eliminación via AJAX

**Parámetros**:
- `<int:contraparte_pk>`: ID de la contraparte padre
- `<int:pk>`: ID de la calificación
- **Nombres**: `calificacion_crear_ajax`, `calificacion_editar_ajax`, `calificacion_eliminar_ajax`

**Características Especiales**:
- **Solo AJAX**: Todas las operaciones son dinámicas
- **URLs Anidadas**: Calificaciones anidadas bajo contrapartes
- **Operaciones Rápidas**: Sin confirmaciones adicionales

### 13. Funcionalidades de Búsqueda y Exportación

```python
# Búsqueda y filtros
path('buscar/', views.ContraparteBuscarView.as_view(), name='buscar'),

# Exportar datos
path('exportar/', views.ExportarContrapartesView.as_view(), name='exportar'),
```

**Patrón de URLs**:
- **Búsqueda**: `/buscar/` - Página de búsqueda avanzada
- **Exportación**: `/exportar/` - Página de exportación de datos

**Parámetros**:
- **Nombres**: `buscar`, `exportar`

**Características Especiales**:
- **Funcionalidades Especializadas**: No siguen patrón CRUD
- **URLs Descriptivas**: Indican claramente la funcionalidad
- **Acceso Directo**: URLs simples para funcionalidades comunes

### 14. Carga de Documentos

```python
# Carga de documentos
path('carga-documentos/', views.CargaDocumentosView.as_view(), name='carga_documentos'),
```

**Patrón de URLs**:
- **Carga**: `/carga-documentos/` - Página de carga masiva de documentos

**Parámetros**:
- **Nombres**: `carga_documentos`

**Características Especiales**:
- **Funcionalidad Especializada**: Carga masiva de documentos
- **URL Descriptiva**: Indica claramente la funcionalidad
- **Acceso Directo**: URL simple para funcionalidad común

### 15. Gestión de Balance Sheets

```python
# Balance Sheets
path('<int:contraparte_pk>/balance-sheets/', views.BalanceSheetListView.as_view(), name='balance_sheet_lista'),
path('<int:contraparte_pk>/balance-sheets/crear/', views.BalanceSheetCreateView.as_view(), name='balance_sheet_crear'),
path('balance-sheets/<int:pk>/', views.BalanceSheetDetailView.as_view(), name='balance_sheet_detalle'),
path('balance-sheets/<int:pk>/editar/', views.BalanceSheetUpdateView.as_view(), name='balance_sheet_editar'),
path('balance-sheets/<int:pk>/eliminar/', views.BalanceSheetDeleteView.as_view(), name='balance_sheet_eliminar'),
```

**Patrón de URLs**:
- **Lista**: `/<contraparte_id>/balance-sheets/` - Lista balance sheets de contraparte
- **Crear**: `/<contraparte_id>/balance-sheets/crear/` - Formulario de creación
- **Detalle**: `/balance-sheets/<id>/` - Vista detallada de balance sheet
- **Editar**: `/balance-sheets/<id>/editar/` - Formulario de edición
- **Eliminar**: `/balance-sheets/<id>/eliminar/` - Confirmación de eliminación

**Parámetros**:
- `<int:contraparte_pk>`: ID de la contraparte padre
- `<int:pk>`: ID del balance sheet
- **Nombres**: `balance_sheet_lista`, `balance_sheet_crear`, `balance_sheet_detalle`, `balance_sheet_editar`, `balance_sheet_eliminar`

**Características Especiales**:
- **URLs Anidadas**: Balance sheets anidados bajo contrapartes
- **RESTful**: Sigue convenciones REST
- **Jerarquía**: Relación padre-hijo clara
- **Híbrido**: Lista y crear anidados, detalle/editar/eliminar independientes

### 16. Endpoints AJAX para Balance Sheets

```python
# AJAX endpoints para Balance Sheets
path('ajax/tipos-cambio/', views.TipoCambioAjaxView.as_view(), name='tipos_cambio_ajax'),
```

**Patrón de URLs**:
- **AJAX**: `/ajax/tipos-cambio/` - Endpoint AJAX para tipos de cambio

**Parámetros**:
- **Nombres**: `tipos_cambio_ajax`

**Características Especiales**:
- **Endpoint AJAX**: Para funcionalidades dinámicas
- **URL Descriptiva**: Indica claramente la funcionalidad
- **Acceso Directo**: URL simple para endpoint AJAX

### 17. Gestión de Monedas

```python
# Gestión de monedas
path('monedas/', views.MonedaListView.as_view(), name='moneda_lista'),
path('monedas/crear/', views.MonedaCreateView.as_view(), name='moneda_crear'),
path('monedas/<int:pk>/editar/', views.MonedaUpdateView.as_view(), name='moneda_editar'),
path('monedas/<int:pk>/eliminar/', views.MonedaDeleteView.as_view(), name='moneda_eliminar'),
```

**Patrón de URLs**:
- **Lista**: `/monedas/` - Lista todas las monedas
- **Crear**: `/monedas/crear/` - Formulario de creación
- **Editar**: `/monedas/<id>/editar/` - Formulario de edición
- **Eliminar**: `/monedas/<id>/eliminar/` - Confirmación de eliminación

**Parámetros**:
- `<int:pk>`: ID de la moneda
- **Nombres**: `moneda_lista`, `moneda_crear`, `moneda_editar`, `moneda_eliminar`

### 18. Gestión de Tipos de Cambio

```python
# Gestión de tipos de cambio
path('tipos-cambio/', views.TipoCambioListView.as_view(), name='tipo_cambio_lista'),
path('tipos-cambio/crear/', views.TipoCambioCreateView.as_view(), name='tipo_cambio_crear'),
path('tipos-cambio/<int:pk>/editar/', views.TipoCambioUpdateView.as_view(), name='tipo_cambio_editar'),
path('tipos-cambio/<int:pk>/eliminar/', views.TipoCambioDeleteView.as_view(), name='tipo_cambio_eliminar'),
```

**Patrón de URLs**:
- **Lista**: `/tipos-cambio/` - Lista todos los tipos de cambio
- **Crear**: `/tipos-cambio/crear/` - Formulario de creación
- **Editar**: `/tipos-cambio/<id>/editar/` - Formulario de edición
- **Eliminar**: `/tipos-cambio/<id>/eliminar/` - Confirmación de eliminación

**Parámetros**:
- `<int:pk>`: ID del tipo de cambio
- **Nombres**: `tipo_cambio_lista`, `tipo_cambio_crear`, `tipo_cambio_editar`, `tipo_cambio_eliminar`

## Patrones de Diseño Utilizados

### 1. RESTful URLs
- **Recursos**: URLs representan recursos
- **Verbos HTTP**: GET, POST, PUT, DELETE
- **Jerarquía**: Recursos anidados
- **Consistencia**: Patrones consistentes

### 2. Hierarchical URLs
- **Anidamiento**: Recursos anidados bajo padres
- **Jerarquía**: Relaciones padre-hijo claras
- **Contexto**: Contexto implícito en URL
- **Navegación**: Navegación intuitiva

### 3. AJAX Pattern
- **Endpoints AJAX**: URLs específicas para AJAX
- **Operaciones Dinámicas**: Sin recarga de página
- **Respuestas JSON**: Respuestas estructuradas
- **UX Mejorada**: Experiencia de usuario fluida

### 4. Naming Convention
- **Nombres Descriptivos**: Nombres claros y descriptivos
- **Consistencia**: Patrones consistentes
- **Legibilidad**: URLs legibles por humanos
- **SEO Friendly**: URLs amigables para SEO

## Consideraciones de Seguridad

### 1. Autenticación
- **Login Required**: Todas las vistas requieren autenticación
- **Verificación de Usuario**: Usuario autenticado
- **Redirección**: Redirección a login si no autenticado
- **Sesión**: Manejo de sesiones

### 2. Autorización
- **Permisos**: Verificación de permisos por usuario
- **Acceso a Recursos**: Control de acceso a recursos
- **Validación**: Validación de parámetros
- **Protección**: Protección contra acceso no autorizado

### 3. Validación
- **Parámetros**: Validación de parámetros de URL
- **Tipos**: Validación de tipos de datos
- **Rangos**: Validación de rangos de valores
- **Sanitización**: Sanitización de entrada

### 4. CSRF Protection
- **Tokens**: Tokens CSRF en formularios
- **Verificación**: Verificación en vistas POST
- **Protección**: Protección contra ataques CSRF
- **Configuración**: Configuración automática

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
# Lista de contrapartes
reverse('contrapartes:lista')

# Detalle de contraparte
reverse('contrapartes:detalle', kwargs={'pk': 1})

# Crear nueva contraparte
reverse('contrapartes:crear')
```

### 2. Operaciones AJAX
```python
# Crear miembro via AJAX
reverse('contrapartes:miembro_crear_ajax', kwargs={'contraparte_pk': 1})

# Editar documento via AJAX
reverse('contrapartes:documento_editar_ajax', kwargs={'pk': 1})

# Actualizar fecha DD via AJAX
reverse('contrapartes:fecha_dd_actualizar_ajax', kwargs={'pk': 1})
```

### 3. Balance Sheets
```python
# Lista de balance sheets
reverse('contrapartes:balance_sheet_lista', kwargs={'contraparte_pk': 1})

# Crear balance sheet
reverse('contrapartes:balance_sheet_crear', kwargs={'contraparte_pk': 1})

# Detalle de balance sheet
reverse('contrapartes:balance_sheet_detalle', kwargs={'pk': 1})
```

### 4. Funcionalidades Especializadas
```python
# Búsqueda
reverse('contrapartes:buscar')

# Exportación
reverse('contrapartes:exportar')

# Carga de documentos
reverse('contrapartes:carga_documentos')
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
