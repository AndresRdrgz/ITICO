# Documentación de la Aplicación Contrapartes

## Descripción General

La aplicación `contrapartes` es el núcleo del sistema ITICO, encargada de gestionar toda la información relacionada con las contrapartes comerciales, incluyendo datos corporativos, miembros, documentos, calificaciones y balance sheets. Esta aplicación proporciona una interfaz completa para el cumplimiento regulatorio y la gestión de riesgos.

## Estructura de Archivos

### 1. models.py
Define todos los modelos de datos de la aplicación, incluyendo:
- **TipoContraparte**: Tipos de contrapartes (empresa, ONG, etc.)
- **EstadoContraparte**: Estados de las contrapartes (activa, pendiente, etc.)
- **Contraparte**: Modelo principal con información corporativa completa
- **Miembro**: Personas asociadas a las contrapartes (PEP detection)
- **Documento**: Gestión de documentos con categorización
- **Comentario**: Sistema de comentarios y notas
- **Calificacion**: Calificaciones crediticias y de riesgo
- **BalanceSheet**: Estados financieros multi-moneda
- **Moneda** y **TipoCambio**: Gestión de monedas y conversiones

### 2. views.py
Contiene todas las vistas de la aplicación organizadas por funcionalidad:
- **CRUD básico**: Lista, crear, editar, eliminar para todos los modelos
- **Vistas AJAX**: Para operaciones dinámicas sin recarga de página
- **Vistas especializadas**: Búsqueda, exportación, carga de documentos
- **Balance Sheets**: Gestión completa de estados financieros

### 3. admin.py
Configuración del Django Admin con:
- **Interfaces personalizadas** para cada modelo
- **Filtros y búsquedas** optimizadas
- **Badges visuales** para estados y categorías
- **Inlines** para relaciones padre-hijo
- **Validaciones** y restricciones de acceso

### 4. urls.py
Definición de todas las rutas URL organizadas por funcionalidad:
- **Gestión de tipos y estados**
- **CRUD de contrapartes y miembros**
- **Endpoints AJAX** para operaciones dinámicas
- **Balance Sheets y monedas**
- **Búsqueda y exportación**

### 5. forms.py
Formularios personalizados con:
- **Validaciones específicas** por modelo
- **Widgets estilizados** con Tailwind CSS
- **FormSets** para relaciones complejas
- **Validaciones de archivos** y fechas

### 6. apiDocumentos.py
API especializada para gestión de documentos con:
- **Endpoints AJAX** para CRUD de documentos
- **Validación de archivos** en tiempo real
- **Agrupación por categorías**
- **Gestión de permisos** por usuario

## Características Principales

### 1. Gestión de Contrapartes
- Información corporativa completa (direcciones, contactos, incorporación)
- Estados y tipos configurables
- Fechas de debida diligencia
- Sistema de comentarios y notas

### 2. Detección de PEP
- Identificación de Personas Políticamente Expuestas
- Categorización de miembros (accionistas, ejecutivos, etc.)
- Validaciones específicas para PEP

### 3. Gestión de Documentos
- Categorización automática
- Control de fechas de expiración
- Validación de tipos de archivo
- Sistema de permisos por usuario

### 4. Calificaciones Crediticias
- Múltiples calificadores (S&P, Moody's, Fitch)
- Outlooks (Positivo, Estable, Negativo)
- Documentos de soporte
- Historial de calificaciones

### 5. Balance Sheets Multi-moneda
- Soporte para múltiples monedas
- Conversiones automáticas a USD
- Items categorizados (Assets, Liabilities, Equity)
- Historial por año

### 6. Sistema de Auditoría
- Seguimiento de creación y modificaciones
- Usuario responsable de cada acción
- Timestamps automáticos
- Soft delete para preservar historial

## Tecnologías Utilizadas

- **Django 4.x**: Framework web principal
- **PostgreSQL**: Base de datos en producción
- **SQLite**: Base de datos en desarrollo
- **Tailwind CSS**: Estilos y componentes
- **HTMX**: Interactividad dinámica
- **JavaScript**: Funcionalidades AJAX

## Patrones de Diseño

### 1. Model-View-Template (MVT)
Separación clara entre modelos, vistas y plantillas.

### 2. Class-Based Views (CBV)
Uso extensivo de vistas basadas en clases para reutilización.

### 3. AJAX Pattern
Operaciones dinámicas sin recarga de página.

### 4. Soft Delete
Preservación de datos históricos mediante campos de estado.

### 5. Audit Trail
Seguimiento completo de cambios y responsabilidades.

## Consideraciones de Seguridad

- **Autenticación requerida** en todas las vistas
- **Validación de permisos** por usuario
- **Sanitización de archivos** subidos
- **Protección CSRF** en formularios
- **Validación de tipos de archivo**

## Escalabilidad

- **Paginación** en listas grandes
- **Índices de base de datos** optimizados
- **Consultas eficientes** con select_related
- **Caché** para datos frecuentemente accedidos
- **Separación de responsabilidades** por módulo

## Mantenimiento

- **Documentación completa** en código
- **Tests unitarios** para funcionalidades críticas
- **Logging** de operaciones importantes
- **Migraciones** versionadas
- **Comandos de gestión** para tareas administrativas
