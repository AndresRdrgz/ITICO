# Documentación de Admin.py - Aplicación Debida Diligencia

## Descripción General

El archivo `admin.py` de la aplicación debida_diligencia está actualmente en su configuración básica, con solo el comentario estándar de Django. Esta documentación describe la configuración recomendada para el Django Admin que debería implementarse para gestionar eficientemente los modelos de debida diligencia.

## Estado Actual

```python
from django.contrib import admin

# Register your models here.
```

**Características**:
- **Configuración básica**: Solo importación del módulo admin
- **Sin registros**: Ningún modelo registrado actualmente
- **Implementación pendiente**: Requiere configuración completa

## Configuración Recomendada

### 1. Configuración de DebidaDiligencia

#### DebidaDiligenciaAdmin
```python
@admin.register(DebidaDiligencia)
class DebidaDiligenciaAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'miembro_display', 'estado_badge', 'nivel_riesgo_badge',
        'fecha_solicitud', 'duracion_dias', 'aprobado_badge', 'solicitado_por'
    ]
    list_filter = [
        'estado', 'nivel_riesgo', 'aprobado', 'fecha_solicitud',
        'fecha_resultado', 'solicitado_por', 'aprobado_por'
    ]
    search_fields = [
        'miembro__nombre', 'miembro__contraparte__nombre',
        'resumen_ia', 'comentarios_analista', 'makito_request_id'
    ]
    ordering = ['-fecha_solicitud']
    readonly_fields = ['fecha_solicitud', 'fecha_actualizacion', 'duracion_dias']
    date_hierarchy = 'fecha_solicitud'
    inlines = [BusquedaInline, AnalisisIAInline]
```

**Características**:
- **List Display**: Información clave con badges personalizados
- **Filtros**: Por estado, nivel de riesgo, fechas y usuarios
- **Búsqueda**: Por miembro, contraparte, resumen IA y comentarios
- **Ordenamiento**: Por fecha de solicitud descendente
- **Campos de Solo Lectura**: Fechas de auditoría y duración
- **Jerarquía de Fechas**: Navegación por fecha de solicitud
- **Inlines**: Búsquedas y análisis IA relacionados

**Métodos Personalizados**:
```python
def miembro_display(self, obj):
    """Muestra información del miembro y contraparte"""
    return f"{obj.miembro.nombre} ({obj.miembro.contraparte.nombre})"
miembro_display.short_description = 'Miembro'

def estado_badge(self, obj):
    """Muestra el estado con colores"""
    colors = {
        'pendiente': '#fbbf24',  # yellow
        'en_proceso': '#3b82f6',  # blue
        'completada': '#10b981',  # green
        'fallida': '#ef4444',  # red
        'cancelada': '#6b7280',  # gray
    }
    color = colors.get(obj.estado, '#6b7280')
    return format_html(
        '<span style="background-color: {}; color: white; padding: 2px 8px; '
        'border-radius: 4px; font-size: 11px; font-weight: bold;">{}</span>',
        color, obj.get_estado_display()
    )
estado_badge.short_description = 'Estado'

def nivel_riesgo_badge(self, obj):
    """Muestra el nivel de riesgo con colores"""
    if not obj.nivel_riesgo:
        return format_html('<span style="color: gray;">-</span>')
    
    colors = {
        'bajo': '#10b981',  # green
        'medio': '#f59e0b',  # yellow
        'alto': '#f97316',  # orange
        'critico': '#ef4444',  # red
    }
    color = colors.get(obj.nivel_riesgo, '#6b7280')
    return format_html(
        '<span style="background-color: {}; color: white; padding: 2px 8px; '
        'border-radius: 4px; font-size: 11px; font-weight: bold;">{}</span>',
        color, obj.get_nivel_riesgo_display()
    )
nivel_riesgo_badge.short_description = 'Riesgo'

def duracion_dias(self, obj):
    """Muestra la duración del proceso en días"""
    duracion = obj.duracion_proceso
    if duracion is not None:
        return f"{duracion} días"
    return "-"
duracion_dias.short_description = 'Duración'

def aprobado_badge(self, obj):
    """Muestra el estado de aprobación"""
    if obj.aprobado is None:
        return format_html('<span style="color: gray;">Pendiente</span>')
    elif obj.aprobado:
        return format_html(
            '<span style="color: green; font-weight: bold;">✓ Aprobado</span>'
        )
    else:
        return format_html(
            '<span style="color: red; font-weight: bold;">✗ Rechazado</span>'
        )
aprobado_badge.short_description = 'Aprobación'
```

**Fieldsets**:
```python
fieldsets = (
    ('Información General', {
        'fields': ('miembro', 'estado', 'nivel_riesgo')
    }),
    ('Proceso', {
        'fields': ('fecha_solicitud', 'fecha_resultado', 'duracion_dias')
    }),
    ('Análisis y Resultados', {
        'fields': ('resumen_ia', 'comentarios_analista'),
        'classes': ('collapse',)
    }),
    ('Aprobación', {
        'fields': ('aprobado', 'aprobado_por', 'fecha_aprobacion')
    }),
    ('Integración Técnica', {
        'fields': ('makito_request_id',),
        'classes': ('collapse',)
    }),
    ('Auditoría', {
        'fields': ('solicitado_por', 'fecha_actualizacion'),
        'classes': ('collapse',)
    }),
)
```

### 2. Configuración de Busqueda

#### BusquedaInline
```python
class BusquedaInline(admin.TabularInline):
    model = Busqueda
    extra = 0
    fields = ['fuente', 'estado', 'coincidencias_encontradas', 'fecha_busqueda']
    readonly_fields = ['fecha_busqueda']
    can_delete = False
```

**Características**:
- **Inline Tabular**: Vista compacta para búsquedas
- **Campos Específicos**: Solo campos relevantes para la vista
- **Campos de Solo Lectura**: Fecha de búsqueda
- **Sin Eliminación**: No se pueden eliminar búsquedas desde inline

#### BusquedaAdmin
```python
@admin.register(Busqueda)
class BusquedaAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'debida_diligencia_display', 'fuente_badge', 'estado_badge',
        'coincidencias_encontradas', 'fecha_busqueda', 'es_positiva_badge'
    ]
    list_filter = [
        'fuente', 'estado', 'fecha_busqueda', 'debida_diligencia__estado'
    ]
    search_fields = [
        'debida_diligencia__miembro__nombre',
        'debida_diligencia__miembro__contraparte__nombre',
        'resultado', 'url_fuente'
    ]
    ordering = ['-fecha_busqueda']
    readonly_fields = ['fecha_busqueda']
    date_hierarchy = 'fecha_busqueda'
```

**Métodos Personalizados**:
```python
def debida_diligencia_display(self, obj):
    """Muestra información de la debida diligencia"""
    return f"DD {obj.debida_diligencia.id} - {obj.debida_diligencia.miembro.nombre}"
debida_diligencia_display.short_description = 'Debida Diligencia'

def fuente_badge(self, obj):
    """Muestra la fuente con colores"""
    colors = {
        'ofac': '#dc2626',  # red
        'onu': '#2563eb',  # blue
        'ue': '#059669',  # green
        'interpol': '#7c3aed',  # purple
        'pep': '#ea580c',  # orange
        'medios': '#0891b2',  # cyan
        'google': '#16a34a',  # green
        'otra': '#6b7280',  # gray
    }
    color = colors.get(obj.fuente, '#6b7280')
    return format_html(
        '<span style="background-color: {}; color: white; padding: 2px 8px; '
        'border-radius: 4px; font-size: 11px; font-weight: bold;">{}</span>',
        color, obj.get_fuente_display()
    )
fuente_badge.short_description = 'Fuente'

def estado_badge(self, obj):
    """Muestra el estado de la búsqueda"""
    colors = {
        'exitosa': '#10b981',  # green
        'con_error': '#f59e0b',  # yellow
        'coincidencia_positiva': '#ef4444',  # red
        'sin_coincidencias': '#6b7280',  # gray
        'timeout': '#f97316',  # orange
    }
    color = colors.get(obj.estado, '#6b7280')
    return format_html(
        '<span style="background-color: {}; color: white; padding: 2px 8px; '
        'border-radius: 4px; font-size: 11px; font-weight: bold;">{}</span>',
        color, obj.get_estado_display()
    )
estado_badge.short_description = 'Estado'

def es_positiva_badge(self, obj):
    """Muestra si la búsqueda es positiva"""
    if obj.es_positiva:
        return format_html(
            '<span style="color: red; font-weight: bold;">⚠ Coincidencia</span>'
        )
    else:
        return format_html(
            '<span style="color: green; font-weight: bold;">✓ Sin coincidencias</span>'
        )
es_positiva_badge.short_description = 'Resultado'
```

### 3. Configuración de AnalisisIA

#### AnalisisIAInline
```python
class AnalisisIAInline(admin.TabularInline):
    model = AnalisisIA
    extra = 0
    fields = ['tipo_analisis', 'confianza', 'fecha_analisis']
    readonly_fields = ['fecha_analisis']
    can_delete = False
```

**Características**:
- **Inline Tabular**: Vista compacta para análisis
- **Campos Específicos**: Solo campos relevantes
- **Campos de Solo Lectura**: Fecha de análisis
- **Sin Eliminación**: No se pueden eliminar análisis desde inline

#### AnalisisIAAdmin
```python
@admin.register(AnalisisIA)
class AnalisisIAAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'debida_diligencia_display', 'tipo_analisis_badge',
        'confianza_display', 'fecha_analisis', 'palabras_clave_count'
    ]
    list_filter = [
        'tipo_analisis', 'fecha_analisis', 'debida_diligencia__estado'
    ]
    search_fields = [
        'debida_diligencia__miembro__nombre',
        'texto_analizado', 'palabras_clave_detectadas'
    ]
    ordering = ['-fecha_analisis']
    readonly_fields = ['fecha_analisis']
    date_hierarchy = 'fecha_analisis'
```

**Métodos Personalizados**:
```python
def debida_diligencia_display(self, obj):
    """Muestra información de la debida diligencia"""
    return f"DD {obj.debida_diligencia.id} - {obj.debida_diligencia.miembro.nombre}"
debida_diligencia_display.short_description = 'Debida Diligencia'

def tipo_analisis_badge(self, obj):
    """Muestra el tipo de análisis con colores"""
    colors = {
        'texto': '#3b82f6',  # blue
        'documento': '#10b981',  # green
        'resumen': '#f59e0b',  # yellow
        'clasificacion': '#ef4444',  # red
    }
    color = colors.get(obj.tipo_analisis, '#6b7280')
    return format_html(
        '<span style="background-color: {}; color: white; padding: 2px 8px; '
        'border-radius: 4px; font-size: 11px; font-weight: bold;">{}</span>',
        color, obj.get_tipo_analisis_display()
    )
tipo_analisis_badge.short_description = 'Tipo'

def confianza_display(self, obj):
    """Muestra el nivel de confianza con colores"""
    confianza = obj.confianza
    if confianza >= 0.8:
        color = '#10b981'  # green
    elif confianza >= 0.6:
        color = '#f59e0b'  # yellow
    else:
        color = '#ef4444'  # red
    
    return format_html(
        '<span style="color: {}; font-weight: bold;">{:.1%}</span>',
        color, confianza
    )
confianza_display.short_description = 'Confianza'

def palabras_clave_count(self, obj):
    """Muestra el número de palabras clave detectadas"""
    if isinstance(obj.palabras_clave_detectadas, list):
        return len(obj.palabras_clave_detectadas)
    return 0
palabras_clave_count.short_description = 'Palabras Clave'
```

## Funcionalidades Avanzadas

### 1. Acciones Personalizadas

#### Acciones para DebidaDiligencia
```python
@admin.action(description='Marcar como completadas')
def marcar_completadas(modeladmin, request, queryset):
    """Marca las debidas diligencias seleccionadas como completadas"""
    updated = queryset.filter(estado='en_proceso').update(
        estado='completada',
        fecha_resultado=timezone.now()
    )
    modeladmin.message_user(
        request,
        f'{updated} debidas diligencias marcadas como completadas.'
    )

@admin.action(description='Generar reporte de riesgo')
def generar_reporte_riesgo(modeladmin, request, queryset):
    """Genera un reporte de riesgo para las DD seleccionadas"""
    # Implementar lógica de generación de reporte
    modeladmin.message_user(
        request,
        f'Reporte de riesgo generado para {queryset.count()} debidas diligencias.'
    )

# Agregar acciones al admin
DebidaDiligenciaAdmin.actions = [marcar_completadas, generar_reporte_riesgo]
```

### 2. Filtros Personalizados

#### Filtro por Duración
```python
class DuracionFilter(admin.SimpleListFilter):
    title = 'duración del proceso'
    parameter_name = 'duracion'
    
    def lookups(self, request, model_admin):
        return (
            ('rapido', 'Rápido (≤ 1 día)'),
            ('normal', 'Normal (2-7 días)'),
            ('lento', 'Lento (8-30 días)'),
            ('muy_lento', 'Muy lento (> 30 días)'),
        )
    
    def queryset(self, request, queryset):
        if self.value() == 'rapido':
            return queryset.filter(
                fecha_resultado__isnull=False,
                fecha_resultado__lte=F('fecha_solicitud') + timedelta(days=1)
            )
        elif self.value() == 'normal':
            return queryset.filter(
                fecha_resultado__isnull=False,
                fecha_resultado__lte=F('fecha_solicitud') + timedelta(days=7),
                fecha_resultado__gt=F('fecha_solicitud') + timedelta(days=1)
            )
        elif self.value() == 'lento':
            return queryset.filter(
                fecha_resultado__isnull=False,
                fecha_resultado__lte=F('fecha_solicitud') + timedelta(days=30),
                fecha_resultado__gt=F('fecha_solicitud') + timedelta(days=7)
            )
        elif self.value() == 'muy_lento':
            return queryset.filter(
                fecha_resultado__isnull=False,
                fecha_resultado__gt=F('fecha_solicitud') + timedelta(days=30)
            )

# Agregar filtro al admin
DebidaDiligenciaAdmin.list_filter.append(DuracionFilter)
```

### 3. Campos Calculados

#### Campo de Estadísticas
```python
def estadisticas_display(self, obj):
    """Muestra estadísticas de la debida diligencia"""
    total_busquedas = obj.busquedas.count()
    coincidencias = obj.busquedas.filter(estado='coincidencia_positiva').count()
    total_analisis = obj.analisis_ia.count()
    
    return format_html(
        '<div style="font-size: 11px;">'
        '<div>Búsquedas: <strong>{}</strong></div>'
        '<div>Coincidencias: <strong style="color: {};">{}</strong></div>'
        '<div>Análisis IA: <strong>{}</strong></div>'
        '</div>',
        total_busquedas,
        'red' if coincidencias > 0 else 'green',
        coincidencias,
        total_analisis
    )
estadisticas_display.short_description = 'Estadísticas'

# Agregar al list_display
DebidaDiligenciaAdmin.list_display.append('estadisticas_display')
```

## Consideraciones de Seguridad

### 1. Permisos
- **Verificación de Usuario**: Usuario autenticado
- **Permisos por Modelo**: Control granular
- **Permisos por Acción**: Crear, editar, eliminar
- **Permisos por Campo**: Campos sensibles

### 2. Validación
- **Validación de Formularios**: Validación en servidor
- **Validación de Datos**: Integridad de datos
- **Validación de Relaciones**: Consistencia referencial
- **Validación de Estados**: Transiciones válidas

### 3. Auditoría
- **Tracking de Usuario**: Usuario responsable
- **Tracking de Fechas**: Timestamps automáticos
- **Tracking de Cambios**: Historial de modificaciones
- **Logging**: Registro de operaciones

## Consideraciones de Rendimiento

### 1. Consultas Optimizadas
- **Select Related**: Para ForeignKeys
- **Prefetch Related**: Para ManyToMany
- **Consultas Específicas**: Solo campos necesarios
- **Índices**: Campos de búsqueda frecuente

### 2. Paginación
- **Listas Paginadas**: Para grandes datasets
- **Configuración por Modelo**: Tamaño de página
- **Navegación Eficiente**: Enlaces de navegación
- **Carga Diferida**: Carga bajo demanda

### 3. Caché
- **Caché de Consultas**: Consultas frecuentes
- **Caché de Templates**: Templates estáticos
- **Caché de Sesión**: Datos de usuario
- **Invalidación**: Invalidación inteligente

## Personalización Visual

### 1. CSS Personalizado
- **Badges**: Estilos específicos
- **Colores**: Paleta de colores consistente
- **Tipografía**: Fuentes y tamaños
- **Espaciado**: Márgenes y padding

### 2. HTML Personalizado
- **Format HTML**: HTML seguro
- **Estructura**: Estructura semántica
- **Accesibilidad**: Atributos de accesibilidad
- **Responsividad**: Diseño adaptable

### 3. JavaScript
- **Interactividad**: Funcionalidades dinámicas
- **Validación**: Validación en cliente
- **UX**: Experiencia de usuario mejorada
- **Compatibilidad**: Compatibilidad cross-browser

## Mantenimiento

### 1. Documentación
- **Docstrings**: Documentación en código
- **Comentarios**: Explicaciones de lógica
- **README**: Documentación de usuario
- **Changelog**: Historial de cambios

### 2. Testing
- **Unit Tests**: Tests de funcionalidad
- **Integration Tests**: Tests de integración
- **UI Tests**: Tests de interfaz
- **Performance Tests**: Tests de rendimiento

### 3. Refactoring
- **Separación de Responsabilidades**: Código modular
- **Reutilización**: Código reutilizable
- **Optimización**: Optimización continua
- **Estandarización**: Estándares de código
