# Documentación de Models.py - Aplicación Debida Diligencia

## Descripción General

El archivo `models.py` define la estructura de datos para el proceso automatizado de debida diligencia, incluyendo 3 modelos principales que gestionan el flujo completo desde la solicitud hasta la aprobación, con integración de RPA, análisis de IA y múltiples fuentes de información.

## Modelos Principales

### 1. DebidaDiligencia (Modelo Principal)

**Propósito**: Gestiona el proceso completo de debida diligencia para un miembro específico, incluyendo estados, resultados de IA, niveles de riesgo y aprobaciones.

```python
class DebidaDiligencia(models.Model):
    ESTADOS = [
        ('pendiente', 'Pendiente'),
        ('en_proceso', 'En Proceso'),
        ('completada', 'Completada'),
        ('fallida', 'Fallida'),
        ('cancelada', 'Cancelada'),
    ]
    
    NIVELES_RIESGO = [
        ('bajo', 'Bajo'),
        ('medio', 'Medio'),
        ('alto', 'Alto'),
        ('critico', 'Crítico'),
    ]
```

#### Campos Principales

##### Relación con Miembro
```python
miembro = models.ForeignKey(
    Miembro,
    on_delete=models.CASCADE,
    related_name='debidas_diligencias',
    verbose_name="Miembro"
)
```
- **Relación**: Una debida diligencia pertenece a un miembro específico
- **Cascada**: Si se elimina el miembro, se eliminan sus DD
- **Relación inversa**: `miembro.debidas_diligencias.all()`

##### Fechas del Proceso
```python
fecha_solicitud = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de solicitud")
fecha_resultado = models.DateTimeField(null=True, blank=True, verbose_name="Fecha de resultado")
fecha_aprobacion = models.DateTimeField(null=True, blank=True, verbose_name="Fecha de aprobación")
fecha_actualizacion = models.DateTimeField(auto_now=True, verbose_name="Última actualización")
```

**Características**:
- **fecha_solicitud**: Se establece automáticamente al crear
- **fecha_resultado**: Se establece cuando el estado cambia a 'completada'
- **fecha_aprobacion**: Se establece cuando se aprueba/rechaza
- **fecha_actualizacion**: Se actualiza en cada modificación

##### Estado del Proceso
```python
estado = models.CharField(
    max_length=20,
    choices=ESTADOS,
    default='pendiente',
    verbose_name="Estado"
)
```

**Estados del Proceso**:
- **pendiente**: Proceso iniciado, esperando procesamiento por RPA
- **en_proceso**: Proceso en ejecución por el sistema RPA (Makito)
- **completada**: Proceso completado exitosamente con resultados
- **fallida**: Proceso falló por algún error técnico o de datos
- **cancelada**: Proceso cancelado manualmente por el usuario

##### Análisis y Evaluación
```python
resumen_ia = models.TextField(
    blank=True,
    null=True,
    verbose_name="Resumen generado por IA"
)
nivel_riesgo = models.CharField(
    max_length=20,
    choices=NIVELES_RIESGO,
    null=True,
    blank=True,
    verbose_name="Nivel de riesgo detectado"
)
comentarios_analista = models.TextField(
    blank=True,
    null=True,
    verbose_name="Comentarios del analista"
)
```

**Características**:
- **resumen_ia**: Resumen automático generado por IA de los resultados
- **nivel_riesgo**: Clasificación automática del nivel de riesgo detectado
- **comentarios_analista**: Comentarios manuales del analista humano

##### Sistema de Aprobación
```python
aprobado = models.BooleanField(
    null=True,
    blank=True,
    verbose_name="¿Aprobado?"
)
aprobado_por = models.ForeignKey(
    User,
    on_delete=models.PROTECT,
    null=True,
    blank=True,
    related_name='dd_aprobadas',
    verbose_name="Aprobado por"
)
```

**Características**:
- **aprobado**: Decisión final (True/False/None para pendiente)
- **aprobado_por**: Usuario que tomó la decisión de aprobación
- **PROTECT**: No se puede eliminar usuario que aprobó

##### Integración Técnica
```python
makito_request_id = models.CharField(
    max_length=100,
    blank=True,
    null=True,
    verbose_name="ID de solicitud en Makito"
)
```

**Características**:
- **makito_request_id**: Identificador único en el sistema RPA Makito
- **Integración**: Permite seguimiento del proceso en sistemas externos
- **Trazabilidad**: Vinculación entre sistemas internos y externos

##### Auditoría
```python
solicitado_por = models.ForeignKey(
    User,
    on_delete=models.PROTECT,
    related_name='dd_solicitadas',
    verbose_name="Solicitado por"
)
```

**Características**:
- **solicitado_por**: Usuario que inició el proceso de DD
- **PROTECT**: No se puede eliminar usuario que solicitó
- **Auditoría**: Seguimiento completo de responsabilidades

#### Métodos Personalizados

##### save()
```python
def save(self, *args, **kwargs):
    """
    Actualiza automáticamente la fecha de resultado cuando el estado cambia a 'completada'.
    """
    if self.estado == 'completada' and not self.fecha_resultado:
        self.fecha_resultado = timezone.now()
    super().save(*args, **kwargs)
```

**Funcionalidad**:
- **Actualización automática**: Establece fecha_resultado cuando se completa
- **Lógica de negocio**: Encapsula reglas de negocio en el modelo
- **Consistencia**: Asegura que las fechas sean consistentes

##### Propiedades Calculadas

```python
@property
def duracion_proceso(self):
    """
    Retorna la duración del proceso en días.
    
    Returns:
        int or None: Número de días que duró el proceso o None si no está completado
    """
    if self.fecha_resultado:
        delta = self.fecha_resultado - self.fecha_solicitud
        return delta.days
    return None

@property
def tiene_coincidencias(self):
    """
    Retorna True si hay búsquedas con coincidencias positivas.
    
    Returns:
        bool: True si se encontraron coincidencias en alguna búsqueda
    """
    return self.busquedas.filter(estado='coincidencia_positiva').exists()
```

**Propiedades**:
- **duracion_proceso**: Calcula días transcurridos en el proceso
- **tiene_coincidencias**: Verifica si hay coincidencias en búsquedas
- **Optimización**: Consultas eficientes con filtros

### 2. Busqueda

**Propósito**: Almacena cada búsqueda específica realizada por el sistema RPA en diferentes fuentes de información.

```python
class Busqueda(models.Model):
    FUENTES = [
        ('ofac', 'OFAC (Office of Foreign Assets Control)'),
        ('onu', 'Lista de Sanciones de la ONU'),
        ('ue', 'Lista de Sanciones de la UE'),
        ('interpol', 'INTERPOL'),
        ('pep', 'Personas Expuestas Políticamente (PEP)'),
        ('medios', 'Búsqueda en Medios'),
        ('google', 'Búsqueda en Google'),
        ('otra', 'Otra fuente'),
    ]
    
    ESTADOS_BUSQUEDA = [
        ('exitosa', 'Exitosa'),
        ('con_error', 'Con Error'),
        ('coincidencia_positiva', 'Coincidencia Positiva'),
        ('sin_coincidencias', 'Sin Coincidencias'),
        ('timeout', 'Tiempo Agotado'),
    ]
```

#### Campos Principales

##### Relación con Debida Diligencia
```python
debida_diligencia = models.ForeignKey(
    DebidaDiligencia,
    on_delete=models.CASCADE,
    related_name='busquedas',
    verbose_name="Debida Diligencia"
)
```

**Características**:
- **Relación**: Una búsqueda pertenece a una debida diligencia
- **Cascada**: Si se elimina la DD, se eliminan sus búsquedas
- **Relación inversa**: `dd.busquedas.all()`

##### Información de la Búsqueda
```python
fuente = models.CharField(
    max_length=20,
    choices=FUENTES,
    verbose_name="Fuente de búsqueda"
)
estado = models.CharField(
    max_length=30,
    choices=ESTADOS_BUSQUEDA,
    default='exitosa',
    verbose_name="Estado de la búsqueda"
)
fecha_busqueda = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de búsqueda")
```

**Fuentes de Búsqueda**:
- **ofac**: Office of Foreign Assets Control (EE.UU.)
- **onu**: Lista de Sanciones de la ONU
- **ue**: Lista de Sanciones de la UE
- **interpol**: Base de datos de INTERPOL
- **pep**: Personas Expuestas Políticamente
- **medios**: Búsqueda en medios de comunicación
- **google**: Búsqueda en Google
- **otra**: Otras fuentes personalizadas

**Estados de Búsqueda**:
- **exitosa**: Búsqueda completada sin errores
- **con_error**: Búsqueda completada con errores
- **coincidencia_positiva**: Se encontraron coincidencias
- **sin_coincidencias**: No se encontraron coincidencias
- **timeout**: Búsqueda agotó el tiempo límite

##### Resultados de la Búsqueda
```python
resultado = models.TextField(
    blank=True,
    null=True,
    verbose_name="Resultado de la búsqueda"
)
documento_adjunto = models.FileField(
    upload_to='busquedas/%Y/%m/%d/',
    blank=True,
    null=True,
    verbose_name="Documento adjunto (PDF/HTML)"
)
coincidencias_encontradas = models.PositiveIntegerField(
    default=0,
    verbose_name="Número de coincidencias encontradas"
)
```

**Características**:
- **resultado**: Descripción textual de los resultados
- **documento_adjunto**: Archivo con resultados detallados
- **coincidencias_encontradas**: Contador numérico de coincidencias
- **Upload personalizado**: Organización por año/mes/día

##### Metadatos
```python
url_fuente = models.URLField(
    blank=True,
    null=True,
    verbose_name="URL de la fuente"
)
```

**Características**:
- **url_fuente**: Enlace a la fuente original de la búsqueda
- **Trazabilidad**: Permite verificar la fuente original
- **Auditoría**: Facilita la verificación de resultados

#### Métodos Personalizados

##### Propiedad Calculada
```python
@property
def es_positiva(self):
    """
    Retorna True si la búsqueda encontró coincidencias.
    
    Returns:
        bool: True si el estado es 'coincidencia_positiva' o si se encontraron coincidencias
    """
    return self.estado == 'coincidencia_positiva' or self.coincidencias_encontradas > 0
```

**Funcionalidad**:
- **Lógica de negocio**: Determina si la búsqueda es positiva
- **Múltiples criterios**: Considera tanto estado como contador
- **Optimización**: Evita consultas adicionales

### 3. AnalisisIA

**Propósito**: Almacena análisis detallados generados por IA sobre los datos de debida diligencia.

```python
class AnalisisIA(models.Model):
    TIPOS_ANALISIS = [
        ('texto', 'Análisis de Texto'),
        ('documento', 'Análisis de Documento'),
        ('resumen', 'Resumen Automatizado'),
        ('clasificacion', 'Clasificación de Riesgo'),
    ]
```

#### Campos Principales

##### Relación con Debida Diligencia
```python
debida_diligencia = models.ForeignKey(
    DebidaDiligencia,
    on_delete=models.CASCADE,
    related_name='analisis_ia',
    verbose_name="Debida Diligencia"
)
```

**Características**:
- **Relación**: Un análisis pertenece a una debida diligencia
- **Cascada**: Si se elimina la DD, se eliminan sus análisis
- **Relación inversa**: `dd.analisis_ia.all()`

##### Información del Análisis
```python
tipo_analisis = models.CharField(
    max_length=20,
    choices=TIPOS_ANALISIS,
    verbose_name="Tipo de análisis"
)
texto_analizado = models.TextField(verbose_name="Texto analizado")
fecha_analisis = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de análisis")
```

**Tipos de Análisis**:
- **texto**: Análisis de texto libre
- **documento**: Análisis de documentos específicos
- **resumen**: Resumen automatizado de información
- **clasificacion**: Clasificación automática de riesgo

##### Resultados del Análisis
```python
resultado_analisis = models.JSONField(
    default=dict,
    verbose_name="Resultado del análisis (JSON)"
)
confianza = models.FloatField(
    default=0.0,
    verbose_name="Nivel de confianza (0.0 - 1.0)"
)
palabras_clave_detectadas = models.JSONField(
    default=list,
    verbose_name="Palabras clave detectadas"
)
```

**Características**:
- **resultado_analisis**: Datos estructurados en formato JSON
- **confianza**: Nivel de confianza del análisis (0.0 - 1.0)
- **palabras_clave_detectadas**: Lista de palabras clave en JSON
- **Flexibilidad**: JSON permite estructuras complejas

## Patrones de Diseño Utilizados

### 1. State Machine Pattern
- **Estados claramente definidos** en DebidaDiligencia
- **Transiciones controladas** entre estados
- **Validaciones por estado** en métodos save()

### 2. Observer Pattern
- **Notificaciones automáticas** por cambios de estado
- **Webhooks** para sistemas externos
- **Eventos de proceso** para auditoría

### 3. Strategy Pattern
- **Diferentes fuentes** de búsqueda
- **Múltiples tipos** de análisis IA
- **Estrategias de evaluación** de riesgo

### 4. Factory Pattern
- **Creación de búsquedas** por fuente
- **Generación de análisis** por tipo
- **Instanciación de procesos**

## Consideraciones de Rendimiento

### 1. Índices de Base de Datos
- **Campos de búsqueda frecuente**: estado, fecha_solicitud, nivel_riesgo
- **Relaciones optimizadas**: ForeignKeys con select_related
- **Consultas eficientes**: Filtros en propiedades calculadas

### 2. Optimización de Consultas
- **select_related**: Para ForeignKeys en listas
- **prefetch_related**: Para relaciones inversas
- **Filtros optimizados**: En propiedades calculadas

### 3. Almacenamiento JSON
- **Flexibilidad**: Estructuras complejas sin esquema fijo
- **Consultas**: Filtros en campos JSON
- **Rendimiento**: Índices en campos JSON frecuentes

## Consideraciones de Seguridad

### 1. Validación de Datos
- **Choices**: Validación de opciones predefinidas
- **Campos requeridos**: Validación de campos obligatorios
- **Tipos de datos**: Validación de tipos específicos

### 2. Auditoría
- **Campos de auditoría**: Usuario y fechas de creación/modificación
- **PROTECT**: Protección de relaciones críticas
- **Trazabilidad**: Seguimiento completo de cambios

### 3. Integridad de Datos
- **Restricciones**: Validaciones a nivel de modelo
- **Cascada**: Eliminación controlada de datos relacionados
- **Consistencia**: Validaciones de lógica de negocio

## Migraciones y Evolución

### 1. Migración Inicial
- **Estructura base**: Modelos principales con relaciones
- **Campos de auditoría**: Usuario y fechas
- **Integración**: Campos para sistemas externos

### 2. Evolución Futura
- **Nuevas fuentes**: Agregar fuentes de búsqueda
- **Tipos de análisis**: Nuevos tipos de análisis IA
- **Estados**: Nuevos estados del proceso
- **Campos JSON**: Estructuras más complejas

## Testing

### 1. Unit Tests
- **Modelos**: Validación de campos y métodos
- **Propiedades**: Cálculos y lógica de negocio
- **Relaciones**: Integridad referencial

### 2. Integration Tests
- **Flujos completos**: Proceso end-to-end
- **Integraciones**: Webhooks y APIs
- **Estados**: Transiciones de estado

### 3. Performance Tests
- **Consultas**: Optimización de queries
- **JSON**: Rendimiento de campos JSON
- **Escalabilidad**: Carga de datos grandes
