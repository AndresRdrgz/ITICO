# Documentación de Models.py - Aplicación Contrapartes

## Descripción General

El archivo `models.py` define la estructura completa de datos de la aplicación contrapartes, incluyendo 12 modelos principales que cubren desde la gestión básica de contrapartes hasta funcionalidades avanzadas como balance sheets multi-moneda y detección de PEP.

## Modelos Principales

### 1. TipoContraparte

**Propósito**: Define los tipos de contrapartes disponibles en el sistema.

```python
class TipoContraparte(models.Model):
    codigo = models.CharField(max_length=20, unique=True)
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)
    activo = models.BooleanField(default=True)
    # Campos de auditoría
    creado_por = models.ForeignKey(User, on_delete=models.PROTECT)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
```

**Características**:
- Código único para identificación
- Control de disponibilidad con campo `activo`
- Auditoría completa de creación y modificaciones
- Relación con User para tracking de responsabilidad

**Uso**: Categorizar contrapartes (empresa, ONG, institución financiera, etc.)

### 2. EstadoContraparte

**Propósito**: Define los estados de una contraparte en el flujo de trabajo.

```python
class EstadoContraparte(models.Model):
    codigo = models.CharField(max_length=20, unique=True)
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)
    color = models.CharField(max_length=7, default='#6B7280')
    activo = models.BooleanField(default=True)
    # Campos de auditoría
    creado_por = models.ForeignKey(User, on_delete=models.PROTECT)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
```

**Características**:
- Color hexadecimal para indicadores visuales
- Estados configurables (activa, pendiente, suspendida, etc.)
- Control de disponibilidad

**Uso**: Controlar el flujo de trabajo y estado actual de contrapartes

### 3. Contraparte (Modelo Principal)

**Propósito**: Modelo central que almacena toda la información de una contraparte.

#### Secciones del Modelo:

##### Información General
```python
full_company_name = models.CharField(max_length=255)
trading_name = models.CharField(max_length=255, blank=True, null=True)
company_website = models.URLField(blank=True, null=True)
```

##### Información Regulatoria
```python
home_regulatory_body = models.CharField(max_length=255, blank=True, null=True)
is_licensed_by_regulatory_body = models.BooleanField(null=True, blank=True)
is_publicly_listed = models.BooleanField(null=True, blank=True)
publicly_listed_country = models.CharField(max_length=100, blank=True, null=True)
is_holding_company = models.BooleanField(null=True, blank=True)
external_auditors = models.TextField(blank=True, null=True)
```

##### Direcciones
```python
registered_address = models.TextField()
business_address = models.TextField(blank=True, null=True)
```

##### Contacto
```python
contact_telephone = models.CharField(max_length=50, blank=True, null=True)
contact_email = models.EmailField(blank=True, null=True)
```

##### Información Empresarial
```python
company_nature_business = models.TextField()
domicile = models.CharField(max_length=100)
company_incorporation_registration = models.CharField(max_length=100)
date_incorporation = models.DateField()
number_of_employees = models.PositiveIntegerField(null=True, blank=True)
```

##### Campos Legacy (Compatibilidad)
```python
nombre = models.CharField(max_length=255, blank=True, null=True)
nacionalidad = models.CharField(max_length=100, blank=True, null=True)
tipo = models.ForeignKey(TipoContraparte, on_delete=models.PROTECT)
estado_nuevo = models.ForeignKey(EstadoContraparte, on_delete=models.PROTECT)
fecha_proxima_dd = models.DateField(null=True, blank=True)
```

**Propiedades Calculadas**:
- `dias_hasta_proxima_dd`: Días restantes hasta próxima debida diligencia
- `requiere_dd_pronto`: Boolean si requiere DD en menos de 30 días
- `comentarios_activos_count`: Número de comentarios activos
- `calificaciones_activas_count`: Número de calificaciones activas

### 4. Miembro

**Propósito**: Gestiona personas asociadas a contrapartes con detección de PEP.

```python
class Miembro(models.Model):
    TIPOS_PERSONA = [
        ('natural', 'Persona Natural'),
        ('juridica', 'Persona Jurídica'),
    ]
    
    CATEGORIAS = [
        ('shareholder', 'Shareholder'),
        ('executive', 'Executive'),
        ('ultimate_beneficial_owner', 'Ultimate Beneficial Owner'),
        ('board_of_director', 'Board of Director'),
    ]
    
    contraparte = models.ForeignKey(Contraparte, on_delete=models.CASCADE)
    tipo_persona = models.CharField(max_length=20, choices=TIPOS_PERSONA)
    nombre = models.CharField(max_length=255)
    numero_identificacion = models.CharField(max_length=50)
    nacionalidad = models.CharField(max_length=100)
    fecha_nacimiento = models.DateField()
    categoria = models.CharField(max_length=30, choices=CATEGORIAS)
    es_pep = models.BooleanField(default=False)
    posicion_pep = models.CharField(max_length=255, blank=True, null=True)
    activo = models.BooleanField(default=True)
```

**Características**:
- Detección de PEP (Personas Políticamente Expuestas)
- Categorización de miembros (accionistas, ejecutivos, etc.)
- Validación de posición PEP cuando es marcado como PEP
- Cálculo automático de edad

**Propiedades**:
- `edad`: Edad calculada automáticamente

### 5. TipoDocumento

**Propósito**: Define tipos de documentos con control de expiración.

```python
class TipoDocumento(models.Model):
    codigo = models.CharField(max_length=20, unique=True)
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)
    requiere_expiracion = models.BooleanField(default=False)
    activo = models.BooleanField(default=True)
    # Campos de auditoría
    creado_por = models.ForeignKey(User, on_delete=models.PROTECT)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
```

**Características**:
- Control si el documento requiere fecha de expiración
- Código único para identificación
- Control de disponibilidad

### 6. Documento

**Propósito**: Gestiona archivos de documentos con categorización y control de vencimientos.

```python
class Documento(models.Model):
    CATEGORIAS = [
        ('compliance', 'Compliance'),
        ('general_financial', 'General and Financial Information'),
        ('opportunities', 'Opportunities'),
        ('info_requested', 'Information Requested from ITICO'),
    ]
    
    contraparte = models.ForeignKey(Contraparte, on_delete=models.CASCADE)
    descripcion = models.TextField(blank=True, null=True)
    tipo = models.ForeignKey(TipoDocumento, on_delete=models.PROTECT)
    categoria = models.CharField(max_length=20, choices=CATEGORIAS)
    archivo = models.FileField(upload_to=documento_upload_path)
    fecha_emision = models.DateField(null=True, blank=True)
    fecha_expiracion = models.DateField(null=True, blank=True)
    subido_por = models.ForeignKey(User, on_delete=models.PROTECT)
    fecha_subida = models.DateTimeField(auto_now_add=True)
    activo = models.BooleanField(default=True)
```

**Características**:
- Validación de extensiones de archivo
- Categorización automática
- Control de fechas de expiración
- Función de upload personalizada

**Propiedades**:
- `esta_vencido`: Boolean si el documento está vencido
- `dias_hasta_expiracion`: Días restantes hasta expiración
- `expira_pronto`: Boolean si expira en menos de 30 días
- `extension`: Extensión del archivo
- `tamaño_legible`: Tamaño del archivo en formato legible
- `icono_tipo`: Icono según tipo de archivo

### 7. Comentario

**Propósito**: Sistema de comentarios y notas para contrapartes.

```python
class Comentario(models.Model):
    contraparte = models.ForeignKey(Contraparte, on_delete=models.CASCADE)
    usuario = models.ForeignKey(User, on_delete=models.PROTECT)
    contenido = models.TextField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    editado = models.BooleanField(default=False)
    activo = models.BooleanField(default=True)
```

**Características**:
- Control de edición (marca si fue editado)
- Soft delete con campo `activo`
- Auditoría de fechas

### 8. Calificador

**Propósito**: Gestiona agencias de calificación crediticia.

```python
class Calificador(models.Model):
    nombre = models.CharField(max_length=255)
    creado_por = models.ForeignKey(User, on_delete=models.PROTECT)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    activo = models.BooleanField(default=True)
```

**Uso**: Almacenar agencias como Standard & Poor's, Moody's, Fitch

### 9. Outlook

**Propósito**: Define perspectivas de calificaciones.

```python
class Outlook(models.Model):
    outlook = models.CharField(max_length=50)
    creado_por = models.ForeignKey(User, on_delete=models.PROTECT)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    activo = models.BooleanField(default=True)
```

**Uso**: Perspectivas como Positivo, Estable, Negativo, En observación

### 10. Calificacion

**Propósito**: Almacena calificaciones crediticias de contrapartes.

```python
class Calificacion(models.Model):
    TIPOS_CALIFICACION = [
        ('nacional', 'Nacional'),
        ('internacional', 'Internacional'),
        ('no aplica', 'No aplica'),
    ]
    
    contraparte = models.ForeignKey(Contraparte, on_delete=models.CASCADE)
    calificador = models.ForeignKey(Calificador, on_delete=models.PROTECT)
    outlook = models.ForeignKey(Outlook, on_delete=models.PROTECT)
    calificacion = models.CharField(max_length=10)
    tipo = models.CharField(max_length=15, choices=TIPOS_CALIFICACION)
    fecha = models.DateField()
    documento_soporte = models.FileField(upload_to='calificaciones/', blank=True, null=True)
    activo = models.BooleanField(default=True)
```

**Características**:
- Tipos de calificación (nacional/internacional)
- Documento de soporte opcional
- Fecha de la calificación

### 11. Moneda

**Propósito**: Gestiona monedas para balance sheets multi-moneda.

```python
class Moneda(models.Model):
    codigo = models.CharField(max_length=3, unique=True)
    nombre = models.CharField(max_length=100)
    simbolo = models.CharField(max_length=10)
    activo = models.BooleanField(default=True)
    creado_por = models.ForeignKey(User, on_delete=models.PROTECT)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
```

**Uso**: Códigos ISO 4217 (USD, EUR, COP) con símbolos

### 12. TipoCambio

**Propósito**: Historial de tipos de cambio para conversiones.

```python
class TipoCambio(models.Model):
    moneda = models.ForeignKey(Moneda, on_delete=models.CASCADE)
    tasa_usd = models.DecimalField(max_digits=15, decimal_places=6)
    fecha = models.DateField()
    creado_por = models.ForeignKey(User, on_delete=models.PROTECT)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['moneda', 'fecha']
```

**Características**:
- Restricción única por moneda y fecha
- Tasa de cambio a USD
- Historial completo

### 13. BalanceSheet

**Propósito**: Estados financieros de contrapartes con soporte multi-moneda.

```python
class BalanceSheet(models.Model):
    contraparte = models.ForeignKey(Contraparte, on_delete=models.CASCADE)
    año = models.PositiveIntegerField()
    moneda_local = models.ForeignKey(Moneda, on_delete=models.PROTECT, null=True, blank=True)
    tipo_cambio = models.ForeignKey(TipoCambio, on_delete=models.PROTECT, null=True, blank=True)
    solo_usd = models.BooleanField(default=True)
    activo = models.BooleanField(default=True)
    
    class Meta:
        unique_together = ['contraparte', 'año']
```

**Propiedades Calculadas**:
- `total_assets_usd`: Total de activos en USD
- `total_liabilities_usd`: Total de pasivos en USD
- `total_equity_usd`: Total de patrimonio en USD

### 14. BalanceSheetItem

**Propósito**: Items individuales de balance sheets.

```python
class BalanceSheetItem(models.Model):
    CATEGORIAS = [
        ('assets', 'Assets'),
        ('liabilities', 'Liabilities'),
        ('equity', 'Equity'),
    ]
    
    balance_sheet = models.ForeignKey(BalanceSheet, on_delete=models.CASCADE)
    descripcion = models.CharField(max_length=255)
    nota = models.TextField(blank=True, null=True)
    categoria = models.CharField(max_length=20, choices=CATEGORIAS)
    monto_usd = models.DecimalField(max_digits=20, decimal_places=2)
    monto_local = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    orden = models.PositiveIntegerField(default=0)
    activo = models.BooleanField(default=True)
```

**Características**:
- Montos en moneda local y USD
- Orden de visualización personalizable
- Categorización (Assets, Liabilities, Equity)

## Funciones Auxiliares

### documento_upload_path
```python
def documento_upload_path(instance, filename):
    """Genera ruta de upload para documentos"""
    return f'contrapartes/{instance.contraparte.id}/documentos/{filename}'
```

## Patrones de Diseño Utilizados

### 1. Soft Delete
- Campo `activo` en modelos críticos
- Preservación de datos históricos
- Filtrado automático en consultas

### 2. Audit Trail
- Campos `creado_por`, `fecha_creacion`, `fecha_actualizacion`
- Seguimiento completo de responsabilidades
- Protección con `on_delete=models.PROTECT`

### 3. Unique Constraints
- Restricciones únicas para integridad de datos
- `unique_together` para combinaciones complejas

### 4. Property Methods
- Cálculos automáticos sin almacenamiento
- Propiedades derivadas para UI
- Validaciones dinámicas

## Consideraciones de Rendimiento

### 1. Índices de Base de Datos
- Campos `unique=True` crean índices automáticamente
- `unique_together` crea índices compuestos
- Campos de búsqueda frecuente

### 2. Relaciones Optimizadas
- `select_related` para ForeignKeys
- `prefetch_related` para ManyToMany
- Lazy loading por defecto

### 3. Validaciones
- Validaciones a nivel de modelo
- Validaciones de archivos con `FileExtensionValidator`
- Restricciones de base de datos

## Migraciones y Evolución

### 1. Compatibilidad Legacy
- Campos legacy mantenidos para compatibilidad
- Migraciones graduales
- Deprecación controlada

### 2. Versionado
- Migraciones numeradas secuencialmente
- Rollback seguro
- Datos de prueba incluidos

## Seguridad

### 1. Validación de Archivos
- Extensiones permitidas específicas
- Validación de tamaño
- Sanitización de nombres

### 2. Permisos
- Protección de relaciones críticas
- Auditoría de usuarios
- Control de acceso por usuario

### 3. Integridad de Datos
- Restricciones de base de datos
- Validaciones de modelo
- Transacciones atómicas
