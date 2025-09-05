# Documentación de Views.py - Aplicación Contrapartes

## Descripción General

El archivo `views.py` contiene todas las vistas de la aplicación contrapartes, organizadas en 4 categorías principales: vistas CRUD básicas, vistas AJAX para operaciones dinámicas, vistas especializadas y vistas para balance sheets. Utiliza Class-Based Views (CBV) para máxima reutilización y mantenibilidad.

## Estructura de Vistas

### 1. Vistas CRUD Básicas

#### Gestión de Tipos de Contraparte

##### TipoContraparteListView
```python
class TipoContraparteListView(LoginRequiredMixin, ListView):
    model = TipoContraparte
    template_name = 'contrapartes/tipo_lista.html'
    context_object_name = 'tipos'
    paginate_by = 20
```

**Funcionalidad**:
- Lista paginada de tipos de contraparte
- Filtrado por estado activo
- Búsqueda por código y nombre
- Ordenamiento por nombre

**Métodos**:
- `get_queryset()`: Filtra tipos activos y aplica búsqueda

##### TipoContraparteCreateView
```python
class TipoContraparteCreateView(LoginRequiredMixin, CreateView):
    model = TipoContraparte
    form_class = TipoContraparteForm
    template_name = 'contrapartes/tipo_crear.html'
    success_url = reverse_lazy('contrapartes:tipo_lista')
```

**Funcionalidad**:
- Creación de nuevos tipos de contraparte
- Asignación automática del usuario creador
- Validación de formulario
- Redirección a lista tras éxito

**Métodos**:
- `form_valid(form)`: Asigna `creado_por` al usuario actual

##### TipoContraparteUpdateView
```python
class TipoContraparteUpdateView(LoginRequiredMixin, UpdateView):
    model = TipoContraparte
    form_class = TipoContraparteForm
    template_name = 'contrapartes/tipo_editar.html'
    success_url = reverse_lazy('contrapartes:tipo_lista')
```

**Funcionalidad**:
- Edición de tipos existentes
- Preservación de datos de auditoría
- Validación de cambios

##### TipoContraparteDeleteView
```python
class TipoContraparteDeleteView(LoginRequiredMixin, DeleteView):
    model = TipoContraparte
    template_name = 'contrapartes/tipo_eliminar.html'
    success_url = reverse_lazy('contrapartes:tipo_lista')
```

**Funcionalidad**:
- Eliminación con confirmación
- Verificación de dependencias
- Contexto adicional para validación

**Métodos**:
- `get_context_data()`: Agrega información de contrapartes relacionadas

#### Gestión de Estados de Contraparte

##### EstadoContraparteListView
```python
class EstadoContraparteListView(LoginRequiredMixin, ListView):
    model = EstadoContraparte
    template_name = 'contrapartes/estado_lista.html'
    context_object_name = 'estados'
    paginate_by = 20
```

**Funcionalidad**:
- Lista paginada de estados
- Filtrado por estado activo
- Búsqueda por código, nombre y descripción
- Ordenamiento por nombre

**Métodos**:
- `get_queryset()`: Filtra estados activos y aplica búsqueda

##### EstadoContraparteCreateView, UpdateView, DeleteView
**Funcionalidad**: Similar a tipos de contraparte pero para estados
- Creación con asignación de usuario
- Edición preservando auditoría
- Eliminación con verificación de dependencias

#### Gestión de Tipos de Documento

##### TipoDocumentoListView
```python
class TipoDocumentoListView(LoginRequiredMixin, ListView):
    model = TipoDocumento
    template_name = 'contrapartes/tipo_documento_lista.html'
    context_object_name = 'tipos'
    paginate_by = 20
```

**Funcionalidad**:
- Lista paginada de tipos de documento
- Filtrado por estado activo
- Búsqueda por código, nombre y descripción
- Ordenamiento por nombre

**Métodos**:
- `get_queryset()`: Filtra tipos activos y aplica búsqueda

##### TipoDocumentoCreateView, UpdateView, DeleteView
**Funcionalidad**: CRUD completo para tipos de documento
- Campos: código, nombre, descripción, requiere_expiracion, activo
- Asignación automática de usuario creador
- Validación de dependencias en eliminación

#### Gestión de Calificadores

##### CalificadorListView
```python
class CalificadorListView(LoginRequiredMixin, ListView):
    model = Calificador
    template_name = 'contrapartes/calificador_lista.html'
    context_object_name = 'calificadores'
    paginate_by = 20
```

**Funcionalidad**:
- Lista paginada de calificadores
- Filtrado por estado activo
- Búsqueda por nombre
- Ordenamiento por nombre

**Métodos**:
- `get_queryset()`: Filtra calificadores activos y aplica búsqueda

##### CalificadorCreateView, UpdateView, DeleteView
**Funcionalidad**: CRUD completo para calificadores
- Campos: nombre, activo
- Asignación automática de usuario creador
- Verificación de dependencias en eliminación

#### Gestión de Outlooks

##### OutlookListView
```python
class OutlookListView(LoginRequiredMixin, ListView):
    model = Outlook
    template_name = 'contrapartes/outlook_lista.html'
    context_object_name = 'outlooks'
    paginate_by = 20
```

**Funcionalidad**:
- Lista paginada de outlooks
- Filtrado por estado activo
- Búsqueda por outlook
- Ordenamiento por outlook

**Métodos**:
- `get_queryset()`: Filtra outlooks activos y aplica búsqueda

##### OutlookCreateView, UpdateView, DeleteView
**Funcionalidad**: CRUD completo para outlooks
- Campos: outlook, activo
- Asignación automática de usuario creador
- Verificación de dependencias en eliminación

### 2. Gestión de Contrapartes

#### ContraparteListView
```python
class ContraparteListView(LoginRequiredMixin, ListView):
    model = Contraparte
    template_name = 'contrapartes/lista.html'
    context_object_name = 'object_list'
    paginate_by = 20
```

**Funcionalidad**:
- Lista paginada de contrapartes
- Filtrado por tipo, estado, nacionalidad
- Búsqueda por nombre y descripción
- Ordenamiento por fecha de creación

**Métodos**:
- `get_context_data()`: Agrega filtros, tipos, estados y estadísticas

**Contexto Adicional**:
- `tipos`: Tipos de contraparte activos
- `estados`: Estados de contraparte activos
- `nacionalidades`: Lista única de nacionalidades
- `total_contrapartes`: Contador total
- `filtros_aplicados`: Filtros activos

#### ContraparteDetailView
```python
class ContraparteDetailView(LoginRequiredMixin, DetailView):
    model = Contraparte
    template_name = 'contrapartes/detalle.html'
```

**Funcionalidad**:
- Vista detallada de una contraparte
- Información completa corporativa
- Lista de miembros, documentos, comentarios
- Calificaciones y balance sheets

#### ContraparteCreateView
```python
class ContraparteCreateView(LoginRequiredMixin, CreateView):
    model = Contraparte
    form_class = ContraparteForm
    template_name = 'contrapartes/crear.html'
    success_url = reverse_lazy('contrapartes:lista')
```

**Funcionalidad**:
- Creación de nuevas contrapartes
- Formulario completo con validaciones
- Asignación automática de usuario creador
- Redirección a lista tras éxito

**Métodos**:
- `form_valid(form)`: Asigna `creado_por` al usuario actual

#### ContraparteUpdateView
```python
class ContraparteUpdateView(LoginRequiredMixin, UpdateView):
    model = Contraparte
    form_class = ContraparteForm
    template_name = 'contrapartes/editar.html'
    success_url = reverse_lazy('contrapartes:lista')
```

**Funcionalidad**:
- Edición de contrapartes existentes
- Preservación de datos de auditoría
- Validación de cambios
- Redirección a lista tras éxito

**Métodos**:
- `get_context_data()`: Agrega información adicional para el formulario

#### ContraparteDeleteView
```python
class ContraparteDeleteView(LoginRequiredMixin, DeleteView):
    model = Contraparte
    template_name = 'contrapartes/eliminar.html'
    success_url = reverse_lazy('contrapartes:lista')
```

**Funcionalidad**:
- Eliminación con confirmación
- Verificación de dependencias
- Contexto adicional para validación

**Métodos**:
- `get_context_data()`: Agrega información de dependencias

### 3. Gestión de Miembros

#### MiembroCreateView
```python
class MiembroCreateView(LoginRequiredMixin, CreateView):
    model = Miembro
    form_class = MiembroForm
    template_name = 'contrapartes/miembro_crear.html'
```

**Funcionalidad**:
- Creación de miembros para una contraparte específica
- Formulario con validaciones PEP
- Redirección a detalle de contraparte

**Métodos**:
- `get_context_data()`: Agrega información de la contraparte
- `form_valid(form)`: Asigna la contraparte al miembro
- `get_success_url()`: Redirección a detalle de contraparte

#### MiembroDetailView
```python
class MiembroDetailView(LoginRequiredMixin, DetailView):
    model = Miembro
    template_name = 'contrapartes/miembro_detalle.html'
```

**Funcionalidad**:
- Vista detallada de un miembro
- Información personal y PEP
- Historial de cambios

#### MiembroUpdateView
```python
class MiembroUpdateView(LoginRequiredMixin, UpdateView):
    model = Miembro
    form_class = MiembroForm
    template_name = 'contrapartes/miembro_editar.html'
```

**Funcionalidad**:
- Edición de miembros existentes
- Validaciones PEP
- Redirección a detalle de contraparte

**Métodos**:
- `get_success_url()`: Redirección a detalle de contraparte

#### MiembroDeleteView
```python
class MiembroDeleteView(LoginRequiredMixin, DeleteView):
    model = Miembro
    template_name = 'contrapartes/miembro_eliminar.html'
```

**Funcionalidad**:
- Eliminación de miembros
- Verificación de dependencias
- Redirección a detalle de contraparte

**Métodos**:
- `get_success_url()`: Redirección a detalle de contraparte

### 4. Vistas AJAX

#### MiembroCreateAjaxView
```python
class MiembroCreateAjaxView(LoginRequiredMixin, View):
    def get(self, request, contraparte_pk):
        # Carga formulario para nuevo miembro
    def post(self, request, contraparte_pk):
        # Procesa creación de miembro via AJAX
```

**Funcionalidad**:
- Creación de miembros sin recarga de página
- Validación de formulario
- Respuesta JSON con resultado
- Actualización dinámica de lista

**Métodos**:
- `get()`: Retorna formulario HTML
- `post()`: Procesa creación y retorna JSON

#### DocumentoCreateAjaxView
```python
class DocumentoCreateAjaxView(LoginRequiredMixin, View):
    def get(self, request, contraparte_pk):
        # Carga formulario para nuevo documento
    def post(self, request, contraparte_pk):
        # Procesa creación de documento via AJAX
```

**Funcionalidad**:
- Creación de documentos sin recarga de página
- Validación de archivos
- Respuesta JSON con resultado
- Actualización dinámica de lista

**Métodos**:
- `get()`: Retorna formulario HTML
- `post()`: Procesa creación y retorna JSON

#### DocumentoUpdateAjaxView
```python
class DocumentoUpdateAjaxView(LoginRequiredMixin, View):
    def get(self, request, pk):
        # Carga formulario para editar documento
    def post(self, request, pk):
        # Procesa edición de documento via AJAX
```

**Funcionalidad**:
- Edición de documentos sin recarga de página
- Validación de permisos
- Respuesta JSON con resultado
- Actualización dinámica de lista

**Métodos**:
- `get()`: Retorna formulario HTML con datos existentes
- `post()`: Procesa edición y retorna JSON

#### DocumentoDeleteView
```python
class DocumentoDeleteView(LoginRequiredMixin, View):
    def post(self, request, pk):
        # Elimina documento (soft delete)
```

**Funcionalidad**:
- Eliminación de documentos via AJAX
- Soft delete (marca como inactivo)
- Validación de permisos
- Respuesta JSON con resultado

**Métodos**:
- `post()`: Procesa eliminación y retorna JSON

#### ComentarioCreateAjaxView
```python
class ComentarioCreateAjaxView(LoginRequiredMixin, View):
    def post(self, request, contraparte_pk):
        # Crea nuevo comentario via AJAX
```

**Funcionalidad**:
- Creación de comentarios sin recarga de página
- Asignación automática de usuario
- Validación de contenido
- Respuesta JSON con resultado

**Métodos**:
- `post()`: Procesa creación y retorna JSON

#### ComentarioUpdateAjaxView
```python
class ComentarioUpdateAjaxView(LoginRequiredMixin, View):
    def get(self, request, pk):
        # Carga formulario para editar comentario
    def post(self, request, pk):
        # Procesa edición de comentario via AJAX
```

**Funcionalidad**:
- Edición de comentarios sin recarga de página
- Validación de permisos
- Marca como editado
- Respuesta JSON con resultado

**Métodos**:
- `get()`: Retorna formulario HTML con contenido existente
- `post()`: Procesa edición y retorna JSON

#### ComentarioDeleteAjaxView
```python
class ComentarioDeleteAjaxView(LoginRequiredMixin, View):
    def post(self, request, pk):
        # Elimina comentario (soft delete)
```

**Funcionalidad**:
- Eliminación de comentarios via AJAX
- Soft delete (marca como inactivo)
- Validación de permisos
- Respuesta JSON con resultado

**Métodos**:
- `post()`: Procesa eliminación y retorna JSON

#### ContraparteFechaDDUpdateView
```python
class ContraparteFechaDDUpdateView(LoginRequiredMixin, View):
    def post(self, request, pk):
        # Actualiza fecha de próxima DD via AJAX
```

**Funcionalidad**:
- Actualización de fecha de debida diligencia
- Validación de fecha
- Respuesta JSON con resultado
- Actualización dinámica de UI

**Métodos**:
- `post()`: Procesa actualización y retorna JSON

#### CalificacionCreateAjaxView
```python
class CalificacionCreateAjaxView(LoginRequiredMixin, View):
    def get(self, request, contraparte_pk):
        # Carga formulario para nueva calificación
    def post(self, request, contraparte_pk):
        # Procesa creación de calificación via AJAX
```

**Funcionalidad**:
- Creación de calificaciones sin recarga de página
- Validación de formulario
- Respuesta JSON con resultado
- Actualización dinámica de lista

**Métodos**:
- `get()`: Retorna formulario HTML
- `post()`: Procesa creación y retorna JSON

#### CalificacionUpdateAjaxView
```python
class CalificacionUpdateAjaxView(LoginRequiredMixin, View):
    def get(self, request, pk):
        # Carga formulario para editar calificación
    def post(self, request, pk):
        # Procesa edición de calificación via AJAX
```

**Funcionalidad**:
- Edición de calificaciones sin recarga de página
- Validación de permisos
- Respuesta JSON con resultado
- Actualización dinámica de lista

**Métodos**:
- `get()`: Retorna formulario HTML con datos existentes
- `post()`: Procesa edición y retorna JSON

#### CalificacionDeleteAjaxView
```python
class CalificacionDeleteAjaxView(LoginRequiredMixin, View):
    def post(self, request, pk):
        # Elimina calificación (soft delete)
```

**Funcionalidad**:
- Eliminación de calificaciones via AJAX
- Soft delete (marca como inactivo)
- Validación de permisos
- Respuesta JSON con resultado

**Métodos**:
- `post()`: Procesa eliminación y retorna JSON

### 5. Vistas Especializadas

#### ContraparteBuscarView
```python
class ContraparteBuscarView(LoginRequiredMixin, TemplateView):
    template_name = 'contrapartes/buscar.html'
```

**Funcionalidad**:
- Página de búsqueda avanzada
- Múltiples criterios de filtrado
- Resultados en tiempo real
- Exportación de resultados

#### ExportarContrapartesView
```python
class ExportarContrapartesView(LoginRequiredMixin, TemplateView):
    template_name = 'contrapartes/exportar.html'
```

**Funcionalidad**:
- Exportación de datos de contrapartes
- Múltiples formatos (CSV, Excel, PDF)
- Filtros personalizables
- Descarga directa

#### CargaDocumentosView
```python
class CargaDocumentosView(LoginRequiredMixin, CreateView):
    model = Documento
    form_class = CargaDocumentoForm
    template_name = 'contrapartes/carga_documentos.html'
```

**Funcionalidad**:
- Carga masiva de documentos
- Selección de contraparte
- Validación de archivos
- Procesamiento en lote

**Métodos**:
- `get_success_url()`: Redirección a página de carga
- `form_valid(form)`: Procesa documento y asigna usuario
- `form_invalid(form)`: Maneja errores de validación
- `get_context_data()`: Agrega estadísticas y filtros

### 6. Vistas de Balance Sheets

#### BalanceSheetListView
```python
class BalanceSheetListView(LoginRequiredMixin, ListView):
    model = BalanceSheet
    template_name = 'contrapartes/balance_sheet_lista.html'
    context_object_name = 'balance_sheets'
    paginate_by = 20
```

**Funcionalidad**:
- Lista de balance sheets de una contraparte
- Filtrado por año
- Ordenamiento por año descendente
- Paginación

**Métodos**:
- `get_queryset()`: Filtra por contraparte
- `get_context_data()`: Agrega información de contraparte

#### BalanceSheetDetailView
```python
class BalanceSheetDetailView(LoginRequiredMixin, DetailView):
    model = BalanceSheet
    template_name = 'contrapartes/balance_sheet_detalle.html'
    context_object_name = 'balance_sheet'
```

**Funcionalidad**:
- Vista detallada de balance sheet
- Items agrupados por categoría
- Totales calculados
- Información de moneda

**Métodos**:
- `get_context_data()`: Agrega items agrupados y totales

#### BalanceSheetCreateView
```python
class BalanceSheetCreateView(LoginRequiredMixin, CreateView):
    model = BalanceSheet
    form_class = BalanceSheetForm
    template_name = 'contrapartes/balance_sheet_crear.html'
```

**Funcionalidad**:
- Creación de balance sheets
- Validación de año único por contraparte
- Asignación automática de usuario
- Redirección a detalle

**Métodos**:
- `dispatch()`: Verifica contraparte válida
- `form_valid(form)`: Asigna contraparte y usuario
- `get_success_url()`: Redirección a detalle
- `get_context_data()`: Agrega información de contraparte

#### BalanceSheetUpdateView
```python
class BalanceSheetUpdateView(LoginRequiredMixin, UpdateView):
    model = BalanceSheet
    form_class = BalanceSheetForm
    template_name = 'contrapartes/balance_sheet_editar.html'
```

**Funcionalidad**:
- Edición de balance sheets con items
- FormSet para items
- Validación de totales
- Preservación de auditoría

**Métodos**:
- `get_context_data()`: Agrega FormSet de items
- `form_valid(form)`: Procesa FormSet
- `get_success_url()`: Redirección a detalle

#### BalanceSheetDeleteView
```python
class BalanceSheetDeleteView(LoginRequiredMixin, DeleteView):
    model = BalanceSheet
    template_name = 'contrapartes/balance_sheet_eliminar.html'
```

**Funcionalidad**:
- Eliminación de balance sheets
- Verificación de dependencias
- Redirección a lista

**Métodos**:
- `get_success_url()`: Redirección a lista
- `delete()`: Eliminación con verificación

### 7. Vistas de Monedas y Tipos de Cambio

#### MonedaListView
```python
class MonedaListView(LoginRequiredMixin, ListView):
    model = Moneda
    template_name = 'contrapartes/moneda_lista.html'
    context_object_name = 'monedas'
    paginate_by = 20
```

**Funcionalidad**:
- Lista paginada de monedas
- Filtrado por estado activo
- Búsqueda por código y nombre
- Ordenamiento por código

**Métodos**:
- `get_queryset()`: Filtra monedas activas y aplica búsqueda

#### MonedaCreateView, UpdateView, DeleteView
**Funcionalidad**: CRUD completo para monedas
- Campos: código, nombre, símbolo, activo
- Asignación automática de usuario creador
- Verificación de dependencias en eliminación

#### TipoCambioListView
```python
class TipoCambioListView(LoginRequiredMixin, ListView):
    model = TipoCambio
    template_name = 'contrapartes/tipo_cambio_lista.html'
    context_object_name = 'tipos_cambio'
    paginate_by = 50
```

**Funcionalidad**:
- Lista paginada de tipos de cambio
- Filtrado por moneda y fecha
- Ordenamiento por fecha descendente
- Búsqueda por moneda

**Métodos**:
- `get_queryset()`: Filtra y ordena tipos de cambio

#### TipoCambioCreateView, UpdateView, DeleteView
**Funcionalidad**: CRUD completo para tipos de cambio
- Campos: moneda, tasa_usd, fecha
- Validación de unicidad por moneda y fecha
- Asignación automática de usuario creador

### 8. Vistas AJAX Especializadas

#### TipoCambioAjaxView
```python
class TipoCambioAjaxView(LoginRequiredMixin, View):
    def get(self, request):
        # Retorna tipos de cambio por moneda
```

**Funcionalidad**:
- Endpoint AJAX para tipos de cambio
- Filtrado por moneda
- Respuesta JSON
- Uso en formularios dinámicos

**Métodos**:
- `get()`: Retorna tipos de cambio en formato JSON

## Patrones de Diseño Utilizados

### 1. Class-Based Views (CBV)
- Reutilización de código
- Separación de responsabilidades
- Herencia y mixins
- Métodos especializados

### 2. Mixins
- `LoginRequiredMixin`: Autenticación requerida
- Reutilización de funcionalidad común
- Composición sobre herencia

### 3. AJAX Pattern
- Operaciones sin recarga de página
- Respuestas JSON
- Validación en tiempo real
- UX mejorada

### 4. Template Method Pattern
- Métodos especializados en CBV
- `get_context_data()`, `form_valid()`, etc.
- Personalización por vista

### 5. Strategy Pattern
- Diferentes estrategias de respuesta
- JSON para AJAX, HTML para navegación
- Adaptabilidad según contexto

## Consideraciones de Seguridad

### 1. Autenticación
- `LoginRequiredMixin` en todas las vistas
- Verificación de usuario autenticado
- Redirección a login si no autenticado

### 2. Autorización
- Validación de permisos por usuario
- Verificación de propiedad de recursos
- Restricción de acceso a datos sensibles

### 3. Validación
- Validación de formularios
- Sanitización de entrada
- Protección contra inyección

### 4. CSRF Protection
- Tokens CSRF en formularios
- Verificación en vistas POST
- Protección contra ataques CSRF

## Consideraciones de Rendimiento

### 1. Paginación
- Listas paginadas para grandes datasets
- Configuración por vista
- Navegación eficiente

### 2. Consultas Optimizadas
- `select_related()` para ForeignKeys
- `prefetch_related()` para ManyToMany
- Reducción de consultas N+1

### 3. Caché
- Caché de consultas frecuentes
- Invalidación inteligente
- Optimización de rendimiento

### 4. AJAX
- Operaciones asíncronas
- Reducción de carga del servidor
- UX mejorada

## Manejo de Errores

### 1. Validación de Formularios
- Errores de campo específicos
- Mensajes de error claros
- Validación en cliente y servidor

### 2. Excepciones
- Manejo de errores de base de datos
- Respuestas de error apropiadas
- Logging de errores críticos

### 3. Respuestas AJAX
- Códigos de estado HTTP apropiados
- Mensajes de error en JSON
- Manejo de errores en cliente

## Testing

### 1. Unit Tests
- Tests para cada vista
- Validación de respuestas
- Verificación de contexto

### 2. Integration Tests
- Flujos completos de usuario
- Interacción entre vistas
- Validación de datos

### 3. AJAX Tests
- Tests de endpoints AJAX
- Validación de respuestas JSON
- Manejo de errores

## Mantenimiento

### 1. Documentación
- Docstrings en métodos
- Comentarios explicativos
- Documentación de APIs

### 2. Logging
- Log de operaciones importantes
- Debug de problemas
- Auditoría de acciones

### 3. Refactoring
- Separación de responsabilidades
- Reutilización de código
- Optimización continua
