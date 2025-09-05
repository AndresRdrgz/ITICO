"""
Modelos para la gestión de contrapartes
Portal Interno de Contrapartes – App Pacífico (Cotizador Web)

ESTRUCTURA DE MODELOS:
1. Modelos de configuración: TipoContraparte, EstadoContraparte, TipoDocumento
2. Modelo principal: Contraparte (información completa de la empresa)
3. Modelos relacionados: Miembro, Documento, Comentario
4. Modelos de calificación: Calificador, Outlook, Calificacion
5. Modelos financieros: Moneda, TipoCambio, BalanceSheet, BalanceSheetItem

FUNCIONALIDADES PRINCIPALES:
- Gestión completa de contrapartes con información empresarial
- Sistema de documentos con categorización y expiración
- Calificaciones y outlooks de agencias especializadas
- Balance sheets con soporte multi-moneda
- Sistema de comentarios y auditoría completa
- Detección de PEP (Personas Políticamente Expuestas)
"""

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import datetime, timedelta
import os
from django.core.validators import FileExtensionValidator
from decimal import Decimal


# =============================================================================
# FUNCIONES DE UTILIDAD
# =============================================================================

def documento_upload_path(instance, filename):
    """
    Define la ruta de subida para documentos de contrapartes.
    
    Estructura: media/contrapartes/{contraparte_id}/documentos/{filename}
    
    Args:
        instance: Instancia del modelo Documento
        filename: Nombre original del archivo
    
    Returns:
        str: Ruta completa donde se almacenará el archivo
    """
    # Limpiar nombre del archivo
    name, ext = os.path.splitext(filename)
    
    # Asegurar que la contraparte tenga un ID (guardar si es necesario)
    contraparte_id = instance.contraparte.id if instance.contraparte.id else 'temp'
    
    # Crear ruta: media/contrapartes/{contraparte_id}/documentos/{filename}
    return f'contrapartes/{contraparte_id}/documentos/{name}{ext}'


# =============================================================================
# MODELOS DE CONFIGURACIÓN
# =============================================================================

class TipoContraparte(models.Model):
    """
    Modelo para definir los tipos de contraparte disponibles en el sistema.
    
    Permite categorizar las contrapartes según su naturaleza (empresa, ONG, 
    institución financiera, etc.) para facilitar la gestión y filtrado.
    
    Campos principales:
    - codigo: Identificador único del tipo
    - nombre: Nombre descriptivo del tipo
    - activo: Control de disponibilidad
    """
    codigo = models.CharField(
        max_length=20, 
        unique=True,
        verbose_name="Código",
        help_text="Código único para identificar el tipo (ej: empresa, ong, etc.)"
    )
    nombre = models.CharField(
        max_length=100, 
        verbose_name="Nombre",
        help_text="Nombre descriptivo del tipo de contraparte"
    )
    descripcion = models.TextField(
        blank=True, 
        null=True, 
        verbose_name="Descripción",
        help_text="Descripción detallada del tipo de contraparte"
    )
    activo = models.BooleanField(
        default=True, 
        verbose_name="Activo",
        help_text="Indica si este tipo está disponible para nuevas contrapartes"
    )
    
    # Campos de auditoría
    creado_por = models.ForeignKey(
        User, 
        on_delete=models.PROTECT,
        related_name='tipos_contraparte_creados',
        verbose_name="Creado por"
    )
    fecha_creacion = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    fecha_actualizacion = models.DateTimeField(auto_now=True, verbose_name="Última actualización")
    
    class Meta:
        verbose_name = "Tipo de Contraparte"
        verbose_name_plural = "Tipos de Contraparte"
        ordering = ['nombre']
    
    def __str__(self):
        return self.nombre


class EstadoContraparte(models.Model):
    """
    Modelo para definir los estados de una contraparte en el sistema.
    
    Permite controlar el flujo de trabajo y el estado actual de cada contraparte
    (activa, pendiente, suspendida, etc.) con indicadores visuales.
    
    Campos principales:
    - codigo: Identificador único del estado
    - nombre: Nombre descriptivo del estado
    - color: Color hexadecimal para indicadores visuales
    - activo: Control de disponibilidad
    """
    codigo = models.CharField(
        max_length=20, 
        unique=True,
        verbose_name="Código",
        help_text="Código único para identificar el estado (ej: activa, pendiente, etc.)"
    )
    nombre = models.CharField(
        max_length=100, 
        verbose_name="Nombre",
        help_text="Nombre descriptivo del estado de contraparte"
    )
    descripcion = models.TextField(
        blank=True, 
        null=True, 
        verbose_name="Descripción",
        help_text="Descripción detallada del estado de contraparte"
    )
    color = models.CharField(
        max_length=7,
        default='#6B7280',
        verbose_name="Color",
        help_text="Color hexadecimal para mostrar el estado (ej: #10B981 para verde)"
    )
    activo = models.BooleanField(
        default=True, 
        verbose_name="Activo",
        help_text="Indica si este estado está disponible para contrapartes"
    )
    
    # Campos de auditoría
    creado_por = models.ForeignKey(
        User, 
        on_delete=models.PROTECT,
        related_name='estados_contraparte_creados',
        verbose_name="Creado por"
    )
    fecha_creacion = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    fecha_actualizacion = models.DateTimeField(auto_now=True, verbose_name="Última actualización")
    
    class Meta:
        verbose_name = "Estado de Contraparte"
        verbose_name_plural = "Estados de Contraparte"
        ordering = ['nombre']
    
    def __str__(self):
        return self.nombre


# =============================================================================
# MODELO PRINCIPAL
# =============================================================================

class Contraparte(models.Model):
    """
    Modelo principal para la gestión de contrapartes.
    
    Almacena toda la información empresarial y legal de una contraparte,
    incluyendo datos corporativos, direcciones, información de contacto,
    y detalles de incorporación. Soporta tanto campos nuevos como legacy
    para compatibilidad con datos existentes.
    
    Secciones principales:
    - Información general: nombre completo, nombre comercial, sitio web
    - Información regulatoria: autoridad supervisora, licencias, cotización
    - Direcciones: dirección registrada y comercial
    - Contacto: teléfono y email
    - Información empresarial: naturaleza del negocio, domicilio, incorporación
    - Campos legacy: para compatibilidad con datos existentes
    - Auditoría: seguimiento de creación y modificaciones
    """
    
    # =============================================================================
    # INFORMACIÓN GENERAL
    # =============================================================================
    full_company_name = models.CharField(
        max_length=255, 
        verbose_name="Full Company Name",
        help_text="Complete legal name of the company",
        blank=True,  # Allow empty for backward compatibility
        null=True
    )
    trading_name = models.CharField(
        max_length=255, 
        blank=True, 
        null=True,
        verbose_name="Trading Name",
        help_text="Commercial or trade name if different from legal name"
    )
    company_website = models.URLField(
        blank=True, 
        null=True,
        verbose_name="Company Website",
        help_text="Official company website URL"
    )
    home_regulatory_body = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="Home Regulatory Body or Supervisory Authority",
        help_text="Primary regulatory authority overseeing the company"
    )
    is_licensed_by_regulatory_body = models.BooleanField(
        null=True,
        blank=True,
        verbose_name="Is the company licensed by the Regulatory Body?",
        help_text="Whether the company holds necessary regulatory licenses"
    )
    is_publicly_listed = models.BooleanField(
        null=True,
        blank=True,
        verbose_name="Is the Company publicly listed?",
        help_text="Whether the company is publicly traded"
    )
    publicly_listed_country = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="Country of public listing",
        help_text="Country where the company is publicly listed"
    )
    is_holding_company = models.BooleanField(
        null=True,
        blank=True,
        verbose_name="Is the Company a Holding Company?",
        help_text="Whether the company operates as a holding company"
    )
    external_auditors = models.TextField(
        blank=True,
        null=True,
        verbose_name="Name and Address of External Auditors",
        help_text="Details of the company's external auditing firm"
    )
    
    # =============================================================================
    # INFORMACIÓN DE DIRECCIONES
    # =============================================================================
    registered_address = models.TextField(
        verbose_name="Registered Address",
        help_text="Official registered address of the company",
        blank=True,  # Allow empty for backward compatibility
        null=True
    )
    business_address = models.TextField(
        blank=True,
        null=True,
        verbose_name="Business Address", 
        help_text="Primary business operating address"
    )
    
    # =============================================================================
    # INFORMACIÓN DE CONTACTO
    # =============================================================================
    contact_telephone = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name="Contact Telephone Number",
        help_text="Primary contact phone number"
    )
    contact_email = models.EmailField(
        blank=True,
        null=True,
        verbose_name="Contact E-mail Address",
        help_text="Primary contact email address"
    )
    
    # =============================================================================
    # INFORMACIÓN EMPRESARIAL
    # =============================================================================
    company_nature_business = models.TextField(
        verbose_name="Company Nature and Type of Business",
        help_text="Description of the company's business activities and nature",
        blank=True,  # Allow empty for backward compatibility
        null=True
    )
    domicile = models.CharField(
        max_length=100,
        verbose_name="Domicile",
        help_text="Legal domicile or jurisdiction of incorporation",
        blank=True,  # Allow empty for backward compatibility
        null=True
    )
    company_incorporation_registration = models.CharField(
        max_length=100,
        verbose_name="Company Incorporation/Registration",
        help_text="Registration or incorporation number",
        blank=True,  # Allow empty for backward compatibility
        null=True
    )
    date_incorporation = models.DateField(
        verbose_name="Date of Incorporation/Registration",
        help_text="Date when the company was legally incorporated",
        blank=True,  # Allow empty for backward compatibility
        null=True
    )
    number_of_employees = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name="Number of Employees",
        help_text="Current number of employees"
    )
    
    # =============================================================================
    # CAMPOS LEGACY (COMPATIBILIDAD)
    # =============================================================================
    nombre = models.CharField(
        max_length=255, 
        verbose_name="Nombre",
        blank=True,
        null=True,
        help_text="Legacy field - use full_company_name instead"
    )
    nacionalidad = models.CharField(
        max_length=100, 
        verbose_name="Nacionalidad",
        blank=True,
        null=True,
        help_text="Legacy field - use domicile instead"
    )
    tipo = models.ForeignKey(
        TipoContraparte,
        on_delete=models.PROTECT,
        related_name='contrapartes',
        verbose_name="Tipo",
        limit_choices_to={'activo': True},
        help_text="Tipo de contraparte"
    )
    estado_nuevo = models.ForeignKey(
        EstadoContraparte,
        on_delete=models.PROTECT,
        related_name='contrapartes',
        verbose_name="Estado",
        limit_choices_to={'activo': True},
        help_text="Estado de la contraparte",
        null=True,
        blank=True
    )
    fecha_proxima_dd = models.DateField(
        verbose_name="Próxima Debida Diligencia",
        null=True,
        blank=True,
        help_text="Fecha de la próxima renovación de debida diligencia"
    )
    
    # =============================================================================
    # CAMPOS DE AUDITORÍA
    # =============================================================================
    creado_por = models.ForeignKey(
        User, 
        on_delete=models.PROTECT,
        related_name='contrapartes_creadas',
        verbose_name="Creado por"
    )
    fecha_creacion = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    fecha_actualizacion = models.DateTimeField(auto_now=True, verbose_name="Última actualización")
    
    # =============================================================================
    # INFORMACIÓN ADICIONAL
    # =============================================================================
    descripcion = models.TextField(blank=True, null=True, verbose_name="Descripción")
    notas = models.TextField(blank=True, null=True, verbose_name="Notas adicionales")
    
    class Meta:
        verbose_name = "Contraparte"
        verbose_name_plural = "Contrapartes"
        ordering = ['-fecha_creacion']
    
    def __str__(self):
        return f"{self.nombre} ({self.tipo.nombre})"
    
    def save(self, *args, **kwargs):
        # Si no hay fecha de próxima DD, establecer en 12 meses
        if not self.fecha_proxima_dd:
            self.fecha_proxima_dd = timezone.now().date() + timedelta(days=365)
        super().save(*args, **kwargs)
    
    @property
    def dias_hasta_proxima_dd(self):
        """Retorna los días hasta la próxima debida diligencia"""
        if self.fecha_proxima_dd:
            delta = self.fecha_proxima_dd - timezone.now().date()
            return delta.days
        return None
    
    @property
    def requiere_dd_pronto(self):
        """Retorna True si la DD vence en menos de 30 días"""
        dias = self.dias_hasta_proxima_dd
        return dias is not None and dias <= 30
    
    @property
    def comentarios_activos_count(self):
        """Retorna el número de comentarios activos"""
        return self.comentarios.filter(activo=True).count()
    
    @property
    def calificaciones_activas_count(self):
        """Retorna el número de calificaciones activas"""
        return self.calificaciones.filter(activo=True).count()
    
    def get_documentos_por_categoria(self):
        """Retorna los documentos agrupados por categoría"""
        from django.db.models import Q
        documentos_activos = self.documentos.filter(activo=True).order_by('categoria', '-fecha_subida')
        
        # Group by category
        categorias = {}
        for documento in documentos_activos:
            categoria = documento.get_categoria_display()
            if categoria not in categorias:
                categorias[categoria] = []
            categorias[categoria].append(documento)
        
        return categorias


# =============================================================================
# MODELOS RELACIONADOS
# =============================================================================

class Miembro(models.Model):
    """
    Modelo para gestionar los miembros asociados a una contraparte.
    
    Almacena información de personas naturales y jurídicas relacionadas con
    la contraparte, incluyendo accionistas, ejecutivos, beneficiarios finales
    y miembros de la junta directiva. Incluye detección de PEP (Personas
    Políticamente Expuestas) para cumplimiento regulatorio.
    
    Categorías disponibles:
    - Shareholder: Accionistas
    - Executive: Ejecutivos
    - Ultimate Beneficial Owner: Beneficiarios finales
    - Board of Director: Miembros de junta directiva
    """
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
    
    contraparte = models.ForeignKey(
        Contraparte, 
        on_delete=models.CASCADE,
        related_name='miembros',
        verbose_name="Contraparte"
    )
    tipo_persona = models.CharField(
        max_length=20,
        choices=TIPOS_PERSONA,
        default='natural',
        verbose_name="Tipo de persona"
    )
    nombre = models.CharField(max_length=255, verbose_name="Nombre completo")
    numero_identificacion = models.CharField(
        max_length=50, 
        verbose_name="Número de identificación",
        default="000000000"
    )
    nacionalidad = models.CharField(max_length=100, verbose_name="Nacionalidad")
    fecha_nacimiento = models.DateField(verbose_name="Fecha de nacimiento")
    categoria = models.CharField(
        max_length=30,
        choices=CATEGORIAS,
        default='shareholder',
        verbose_name="Categoría"
    )
    es_pep = models.BooleanField(
        default=False,
        verbose_name="PEP (Politically Exposed Person)",
        help_text="Indica si esta persona es una Persona Políticamente Expuesta"
    )
    posicion_pep = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="Posición como PEP",
        help_text="Cargo o posición política que ocupa o ha ocupado la persona"
    )
    
    # Campos de auditoría
    fecha_creacion = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    fecha_actualizacion = models.DateTimeField(auto_now=True, verbose_name="Última actualización")
    activo = models.BooleanField(default=True, verbose_name="Activo")
    
    class Meta:
        verbose_name = "Miembro"
        verbose_name_plural = "Miembros"
        unique_together = ['contraparte', 'numero_identificacion']
        ordering = ['nombre']
    
    def __str__(self):
        return f"{self.nombre} ({self.get_categoria_display()}) - {self.contraparte.nombre}"
    
    @property
    def edad(self):
        """Calcula la edad del miembro"""
        today = timezone.now().date()
        return today.year - self.fecha_nacimiento.year - (
            (today.month, today.day) < (self.fecha_nacimiento.month, self.fecha_nacimiento.day)
        )


class TipoDocumento(models.Model):
    """
    Modelo para definir los tipos de documentos disponibles en el sistema.
    
    Permite categorizar los documentos según su naturaleza (debida diligencia,
    contratos, certificados, etc.) y controlar si requieren fecha de expiración.
    
    Campos principales:
    - codigo: Identificador único del tipo
    - nombre: Nombre descriptivo del tipo
    - requiere_expiracion: Control si el documento tiene fecha de vencimiento
    - activo: Control de disponibilidad
    """
    codigo = models.CharField(
        max_length=20, 
        unique=True,
        verbose_name="Código",
        help_text="Código único para identificar el tipo (ej: dd, contrato, etc.)"
    )
    nombre = models.CharField(
        max_length=100, 
        verbose_name="Nombre",
        help_text="Nombre descriptivo del tipo de documento"
    )
    descripcion = models.TextField(
        blank=True, 
        null=True, 
        verbose_name="Descripción",
        help_text="Descripción detallada del tipo de documento"
    )
    requiere_expiracion = models.BooleanField(
        default=False,
        verbose_name="Requiere fecha de expiración",
        help_text="Indica si este tipo de documento requiere fecha de expiración"
    )
    activo = models.BooleanField(
        default=True, 
        verbose_name="Activo",
        help_text="Indica si este tipo está disponible para nuevos documentos"
    )
    
    # Campos de auditoría
    creado_por = models.ForeignKey(
        User, 
        on_delete=models.PROTECT,
        related_name='tipos_documento_creados',
        verbose_name="Creado por"
    )
    fecha_creacion = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    fecha_actualizacion = models.DateTimeField(auto_now=True, verbose_name="Última actualización")
    
    class Meta:
        verbose_name = "Tipo de Documento"
        verbose_name_plural = "Tipos de Documento"
        ordering = ['nombre']
    
    def __str__(self):
        return self.nombre


class Comentario(models.Model):
    """
    Modelo para gestionar comentarios asociados a contrapartes.
    
    Permite a los usuarios agregar comentarios, notas y observaciones sobre
    una contraparte específica. Incluye control de edición y auditoría completa
    para seguimiento de cambios.
    
    Características:
    - Vinculación a contraparte y usuario
    - Control de edición (marca si fue editado)
    - Soft delete (campo activo)
    - Auditoría de fechas
    """
    contraparte = models.ForeignKey(
        Contraparte,
        on_delete=models.CASCADE,
        related_name='comentarios',
        verbose_name="Contraparte"
    )
    usuario = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='comentarios_contrapartes',
        verbose_name="Usuario"
    )
    contenido = models.TextField(
        verbose_name="Comentario",
        help_text="Contenido del comentario"
    )
    
    # Campos de auditoría
    fecha_creacion = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Fecha de creación"
    )
    fecha_actualizacion = models.DateTimeField(
        auto_now=True,
        verbose_name="Fecha de actualización"
    )
    editado = models.BooleanField(
        default=False,
        verbose_name="Editado",
        help_text="Indica si el comentario ha sido editado"
    )
    activo = models.BooleanField(
        default=True,
        verbose_name="Activo"
    )
    
    class Meta:
        verbose_name = "Comentario"
        verbose_name_plural = "Comentarios"
        ordering = ['-fecha_creacion']
    
    def __str__(self):
        return f"Comentario de {self.usuario.get_full_name() or self.usuario.username} en {self.contraparte.nombre}"
    
    def save(self, *args, **kwargs):
        # Mark as edited if content is being modified (not on creation)
        if self.pk and self._state.adding is False:
            self.editado = True
        super().save(*args, **kwargs)


class Documento(models.Model):
    """
    Modelo para gestionar documentos asociados a contrapartes.
    
    Almacena archivos de documentos con categorización, fechas de emisión y
    expiración, y validación de extensiones. Incluye propiedades para detectar
    documentos vencidos o próximos a vencer.
    
    Categorías disponibles:
    - Compliance: Documentos de cumplimiento
    - General and Financial Information: Información general y financiera
    - Opportunities: Oportunidades
    - Information Requested from ITICO: Información solicitada por ITICO
    
    Características:
    - Validación de extensiones de archivo
    - Control de fechas de expiración
    - Categorización automática
    - Propiedades para detectar vencimientos
    """
    CATEGORIAS = [
        ('compliance', 'Compliance'),
        ('general_financial', 'General and Financial Information'),
        ('opportunities', 'Opportunities'),
        ('info_requested', 'Information Requested from ITICO'),
    ]

    contraparte = models.ForeignKey(
        Contraparte,
        on_delete=models.CASCADE,
        related_name='documentos',
        verbose_name="Contraparte"
    )
    # nombre field removed - documents are now identified by tipo
    descripcion = models.TextField(
        blank=True,
        null=True,
        verbose_name="Descripción"
    )
    tipo = models.ForeignKey(
        TipoDocumento,
        on_delete=models.PROTECT,
        related_name='documentos',
        verbose_name="Tipo de documento",
        limit_choices_to={'activo': True},
        help_text="Tipo de documento"
    )

    categoria = models.CharField(
        max_length=20,
        choices=CATEGORIAS,
        default='compliance',
        verbose_name="Categoría",
        help_text="Categoría del documento"
    )

    archivo = models.FileField(
        upload_to=documento_upload_path,
        validators=[FileExtensionValidator(
            allowed_extensions=['pdf', 'doc', 'docx', 'xls', 'xlsx', 'txt', 'jpg', 'jpeg', 'png']
        )],
        verbose_name="Archivo"
    )
    
    # Fechas del documento
    fecha_emision = models.DateField(
        null=True,
        blank=True,
        verbose_name="Fecha de emisión",
        help_text="Fecha en que fue emitido el documento"
    )
    fecha_expiracion = models.DateField(
        null=True,
        blank=True,
        verbose_name="Fecha de expiración",
        help_text="Fecha en que expira la validez del documento"
    )
    
    # Campos de auditoría
    subido_por = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='documentos_subidos',
        verbose_name="Subido por"
    )
    fecha_subida = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Fecha de subida"
    )
    fecha_actualizacion = models.DateTimeField(
        auto_now=True,
        verbose_name="Última actualización"
    )
    activo = models.BooleanField(
        default=True,
        verbose_name="Activo"
    )
    
    class Meta:
        verbose_name = "Documento"
        verbose_name_plural = "Documentos"
        ordering = ['-fecha_subida']
    
    def __str__(self):
        return f"{self.tipo.nombre} - {self.contraparte.nombre}"
    
    @property
    def esta_vencido(self):
        """Retorna True si el documento está vencido"""
        if self.fecha_expiracion:
            return self.fecha_expiracion < timezone.now().date()
        return False
    
    @property
    def dias_hasta_expiracion(self):
        """Retorna los días hasta la expiración"""
        if self.fecha_expiracion:
            delta = self.fecha_expiracion - timezone.now().date()
            return delta.days
        return None
    
    @property
    def expira_pronto(self):
        """Retorna True si el documento expira en menos de 30 días"""
        dias = self.dias_hasta_expiracion
        return dias is not None and 0 <= dias <= 30
    
    class Meta:
        verbose_name = "Documento"
        verbose_name_plural = "Documentos"
        ordering = ['-fecha_subida']
    
    def __str__(self):
        return f"{self.tipo.nombre} - {self.contraparte.nombre}"
    
    @property
    def extension(self):
        """Returns the file extension"""
        return os.path.splitext(self.archivo.name)[1].lower()
    
    @property
    def tamaño_legible(self):
        """Returns file size in human readable format"""
        if not self.archivo:
            return "0 B"
        
        size = self.archivo.size
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size < 1024.0:
                return f"{size:.1f} {unit}"
            size /= 1024.0
        return f"{size:.1f} TB"
    
    @property
    def icono_tipo(self):
        """Returns appropriate icon for file type"""
        ext = self.extension
        if ext == '.pdf':
            return 'fas fa-file-pdf text-red-500'
        elif ext in ['.doc', '.docx']:
            return 'fas fa-file-word text-blue-500'
        elif ext in ['.xls', '.xlsx']:
            return 'fas fa-file-excel text-green-500'
        elif ext in ['.jpg', '.jpeg', '.png']:
            return 'fas fa-file-image text-purple-500'
        elif ext == '.txt':
            return 'fas fa-file-alt text-gray-500'
        else:
            return 'fas fa-file text-gray-500'


# =============================================================================
# MODELOS DE CALIFICACIÓN
# =============================================================================

class Calificador(models.Model):
    """
    Modelo para gestionar las agencias de calificación.
    
    Almacena información de las entidades que realizan calificaciones de riesgo
    y crediticias de las contrapartes (ej: Standard & Poor's, Moody's, Fitch).
    
    Campos principales:
    - nombre: Nombre de la agencia calificadora
    - activo: Control de disponibilidad
    - Auditoría completa de creación y modificaciones
    """
    nombre = models.CharField(
        max_length=255,
        verbose_name="Nombre del Calificador",
        help_text="Nombre de la agencia o entidad calificadora"
    )
    
    # Campos de auditoría
    creado_por = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='calificadores_creados',
        verbose_name="Creado por"
    )
    fecha_creacion = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Fecha de creación"
    )
    fecha_actualizacion = models.DateTimeField(
        auto_now=True,
        verbose_name="Última actualización"
    )
    activo = models.BooleanField(
        default=True,
        verbose_name="Activo"
    )
    
    class Meta:
        verbose_name = "Calificador"
        verbose_name_plural = "Calificadores"
        ordering = ['nombre']
    
    def __str__(self):
        return self.nombre


class Outlook(models.Model):
    """
    Modelo para gestionar los tipos de outlook de calificaciones.
    
    Define las perspectivas o tendencias de las calificaciones (ej: Positivo,
    Estable, Negativo, En observación). Se utiliza junto con las calificaciones
    para proporcionar una visión completa del riesgo crediticio.
    
    Campos principales:
    - outlook: Tipo de perspectiva (ej: Positivo, Estable, Negativo)
    - activo: Control de disponibilidad
    - Auditoría completa de creación y modificaciones
    """
    outlook = models.CharField(
        max_length=50,
        verbose_name="Outlook",
        help_text="Tipo de outlook (ej: Positivo, Estable, Negativo)"
    )
    
    # Campos de auditoría
    creado_por = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='outlooks_creados',
        verbose_name="Creado por"
    )
    fecha_creacion = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Fecha de creación"
    )
    fecha_actualizacion = models.DateTimeField(
        auto_now=True,
        verbose_name="Última actualización"
    )
    activo = models.BooleanField(
        default=True,
        verbose_name="Activo"
    )
    
    class Meta:
        verbose_name = "Outlook"
        verbose_name_plural = "Outlooks"
        ordering = ['outlook']
    
    def __str__(self):
        return self.outlook


class Calificacion(models.Model):
    """
    Modelo para gestionar las calificaciones de contrapartes.
    
    Almacena las calificaciones crediticias y de riesgo otorgadas por agencias
    especializadas a las contrapartes. Incluye información sobre el calificador,
    outlook, tipo de calificación y documento de soporte.
    
    Tipos de calificación:
    - Nacional: Calificación en el mercado local
    - Internacional: Calificación en mercados internacionales
    - No aplica: Sin calificación disponible
    
    Características:
    - Vinculación a contraparte, calificador y outlook
    - Fecha de la calificación
    - Documento de soporte opcional
    - Control de activación
    """
    TIPOS_CALIFICACION = [
        ('nacional', 'Nacional'),
        ('internacional', 'Internacional'),
        ('no aplica', 'No aplica'),
    ]
    
    contraparte = models.ForeignKey(
        Contraparte,
        on_delete=models.CASCADE,
        related_name='calificaciones',
        verbose_name="Contraparte"
    )
    calificador = models.ForeignKey(
        Calificador,
        on_delete=models.PROTECT,
        related_name='calificaciones',
        verbose_name="Calificador",
        limit_choices_to={'activo': True}
    )
    outlook = models.ForeignKey(
        Outlook,
        on_delete=models.PROTECT,
        related_name='calificaciones',
        verbose_name="Outlook",
        limit_choices_to={'activo': True}
    )
    calificacion = models.CharField(
        max_length=10,
        verbose_name="Calificación",
        help_text="Calificación otorgada (ej: AAA, AA, A, BBB, etc.)"
    )
    tipo = models.CharField(
        max_length=15,
        choices=TIPOS_CALIFICACION,
        default='no aplica',
        verbose_name="Tipo de Calificación",
        help_text="Indica si la calificación es nacional o internacional"
    )
    fecha = models.DateField(
        verbose_name="Fecha",
        help_text="Fecha de la calificación"
    )
    documento_soporte = models.FileField(
        upload_to='calificaciones/',
        blank=True,
        null=True,
        verbose_name="Documento de Soporte",
        help_text="Documento que respalda la calificación"
    )
    
    # Campos de auditoría
    creado_por = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='calificaciones_creadas',
        verbose_name="Creado por"
    )
    fecha_creacion = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Fecha de creación"
    )
    fecha_actualizacion = models.DateTimeField(
        auto_now=True,
        verbose_name="Última actualización"
    )
    activo = models.BooleanField(
        default=True,
        verbose_name="Activo"
    )
    
    class Meta:
        verbose_name = "Calificación"
        verbose_name_plural = "Calificaciones"
        ordering = ['-fecha']
    
    def __str__(self):
        return f"{self.calificador.nombre} - {self.contraparte.nombre} ({self.calificacion})"


# =============================================================================
# MODELOS FINANCIEROS
# =============================================================================

class Moneda(models.Model):
    """
    Modelo para gestionar las monedas disponibles en el sistema.
    
    Almacena información de las monedas utilizadas en el sistema, incluyendo
    códigos ISO 4217, nombres y símbolos. Se utiliza para conversiones de
    moneda y balance sheets multi-moneda.
    
    Campos principales:
    - codigo: Código ISO 4217 (ej: USD, EUR, COP)
    - nombre: Nombre completo de la moneda
    - simbolo: Símbolo de la moneda (ej: $, €, ¥)
    - activo: Control de disponibilidad
    """
    codigo = models.CharField(
        max_length=3,
        unique=True,
        verbose_name="Código",
        help_text="Código de la moneda (ISO 4217) - ej: USD, EUR, COP"
    )
    nombre = models.CharField(
        max_length=100,
        verbose_name="Nombre",
        help_text="Nombre de la moneda"
    )
    simbolo = models.CharField(
        max_length=10,
        verbose_name="Símbolo",
        help_text="Símbolo de la moneda - ej: $, €, ¥"
    )
    activo = models.BooleanField(
        default=True,
        verbose_name="Activo"
    )
    
    # Campos de auditoría
    creado_por = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='monedas_creadas',
        verbose_name="Creado por"
    )
    fecha_creacion = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    fecha_actualizacion = models.DateTimeField(auto_now=True, verbose_name="Última actualización")
    
    class Meta:
        verbose_name = "Moneda"
        verbose_name_plural = "Monedas"
        ordering = ['codigo']
    
    def __str__(self):
        return f"{self.codigo} - {self.nombre}"


class TipoCambio(models.Model):
    """
    Modelo para almacenar el historial de tipos de cambio.
    
    Mantiene un registro histórico de las tasas de cambio entre diferentes
    monedas y el USD. Se utiliza para conversiones de moneda en balance sheets
    y reportes financieros.
    
    Características:
    - Vinculación a moneda específica
    - Tasa de cambio a USD
    - Fecha del tipo de cambio
    - Restricción única por moneda y fecha
    - Auditoría de creación
    """
    moneda = models.ForeignKey(
        Moneda,
        on_delete=models.CASCADE,
        related_name='tipos_cambio',
        verbose_name="Moneda"
    )
    tasa_usd = models.DecimalField(
        max_digits=15,
        decimal_places=6,
        verbose_name="Tasa a USD",
        help_text="Cuántos USD equivale 1 unidad de esta moneda"
    )
    fecha = models.DateField(
        verbose_name="Fecha",
        help_text="Fecha del tipo de cambio"
    )
    
    # Campos de auditoría
    creado_por = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='tipos_cambio_creados',
        verbose_name="Creado por"
    )
    fecha_creacion = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    
    class Meta:
        verbose_name = "Tipo de Cambio"
        verbose_name_plural = "Tipos de Cambio"
        ordering = ['-fecha']
        unique_together = ['moneda', 'fecha']
    
    def __str__(self):
        return f"{self.moneda.codigo} - {self.tasa_usd} USD ({self.fecha})"


class BalanceSheet(models.Model):
    """
    Modelo para gestionar los balance sheets de contrapartes.
    
    Almacena la información financiera de una contraparte para un año específico,
    incluyendo soporte para múltiples monedas y conversiones automáticas a USD.
    
    Características:
    - Un balance sheet por contraparte y año
    - Soporte para moneda local y USD
    - Vinculación a tipo de cambio para conversiones
    - Propiedades para calcular totales automáticamente
    - Control de activación
    """
    contraparte = models.ForeignKey(
        Contraparte,
        on_delete=models.CASCADE,
        related_name='balance_sheets',
        verbose_name="Contraparte"
    )
    año = models.PositiveIntegerField(
        verbose_name="Año",
        help_text="Año del balance sheet"
    )
    moneda_local = models.ForeignKey(
        Moneda,
        on_delete=models.PROTECT,
        related_name='balance_sheets_moneda_local',
        verbose_name="Moneda Local",
        null=True,
        blank=True,
        help_text="Moneda local del balance sheet (opcional si es en USD)"
    )
    tipo_cambio = models.ForeignKey(
        TipoCambio,
        on_delete=models.PROTECT,
        related_name='balance_sheets',
        verbose_name="Tipo de Cambio",
        null=True,
        blank=True,
        help_text="Tipo de cambio utilizado para convertir a USD"
    )
    solo_usd = models.BooleanField(
        default=True,
        verbose_name="Solo USD",
        help_text="Indica si el balance sheet está únicamente en USD"
    )
    
    # Campos de auditoría
    creado_por = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='balance_sheets_creados',
        verbose_name="Creado por"
    )
    fecha_creacion = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    fecha_actualizacion = models.DateTimeField(auto_now=True, verbose_name="Última actualización")
    activo = models.BooleanField(default=True, verbose_name="Activo")
    
    class Meta:
        verbose_name = "Balance Sheet"
        verbose_name_plural = "Balance Sheets"
        ordering = ['-año']
        unique_together = ['contraparte', 'año']
    
    def __str__(self):
        return f"Balance Sheet {self.año} - {self.contraparte.nombre or self.contraparte.full_company_name}"
    
    @property
    def total_assets_usd(self):
        """Calcula el total de activos en USD"""
        return self.items.filter(categoria='assets', activo=True).aggregate(
            total=models.Sum('monto_usd')
        )['total'] or Decimal('0.00')
    
    @property
    def total_liabilities_usd(self):
        """Calcula el total de pasivos en USD"""
        return self.items.filter(categoria='liabilities', activo=True).aggregate(
            total=models.Sum('monto_usd')
        )['total'] or Decimal('0.00')
    
    @property
    def total_equity_usd(self):
        """Calcula el total de patrimonio en USD"""
        return self.items.filter(categoria='equity', activo=True).aggregate(
            total=models.Sum('monto_usd')
        )['total'] or Decimal('0.00')


class BalanceSheetItem(models.Model):
    """
    Modelo para gestionar los items individuales de un balance sheet.
    
    Almacena cada línea del balance sheet con su descripción, categoría,
    montos en moneda local y USD, y orden de visualización.
    
    Categorías disponibles:
    - Assets: Activos
    - Liabilities: Pasivos
    - Equity: Patrimonio
    
    Características:
    - Vinculación a balance sheet específico
    - Montos en moneda local y USD
    - Orden de visualización personalizable
    - Notas adicionales por item
    - Control de activación
    """
    CATEGORIAS = [
        ('assets', 'Assets'),
        ('liabilities', 'Liabilities'),
        ('equity', 'Equity'),
    ]
    
    balance_sheet = models.ForeignKey(
        BalanceSheet,
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name="Balance Sheet"
    )
    descripcion = models.CharField(
        max_length=255,
        verbose_name="Descripción",
        help_text="Descripción del item del balance"
    )
    nota = models.TextField(
        blank=True,
        null=True,
        verbose_name="Nota",
        help_text="Notas adicionales sobre el item"
    )
    categoria = models.CharField(
        max_length=20,
        choices=CATEGORIAS,
        verbose_name="Categoría"
    )
    monto_usd = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        verbose_name="Monto USD",
        help_text="Monto en dólares estadounidenses"
    )
    monto_local = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name="Monto Moneda Local",
        help_text="Monto en moneda local (opcional)"
    )
    orden = models.PositiveIntegerField(
        default=0,
        verbose_name="Orden",
        help_text="Orden de visualización del item"
    )
    
    # Campos de auditoría
    creado_por = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='balance_sheet_items_creados',
        verbose_name="Creado por"
    )
    fecha_creacion = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    fecha_actualizacion = models.DateTimeField(auto_now=True, verbose_name="Última actualización")
    activo = models.BooleanField(default=True, verbose_name="Activo")
    
    class Meta:
        verbose_name = "Item de Balance Sheet"
        verbose_name_plural = "Items de Balance Sheet"
        ordering = ['categoria', 'orden', 'descripcion']
    
    def __str__(self):
        return f"{self.descripcion} - {self.get_categoria_display()}"
