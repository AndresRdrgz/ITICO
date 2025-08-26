"""
Modelos para la gestión de contrapartes
Portal Interno de Contrapartes – App Pacífico
"""

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import datetime, timedelta
import os
from django.core.validators import FileExtensionValidator


def documento_upload_path(instance, filename):
    """Define the upload path for documents"""
    # Clean filename
    name, ext = os.path.splitext(filename)
    # Create path: media/contrapartes/{contraparte_id}/documentos/{filename}
    return f'contrapartes/{instance.contraparte.id}/documentos/{name}{ext}'


class TipoContraparte(models.Model):
    """
    Modelo para los tipos de contraparte
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


class Contraparte(models.Model):
    """
    Modelo principal para las contrapartes
    """
    ESTADOS_CONTRAPARTE = [
        ('activa', 'Activa'),
        ('inactiva', 'Inactiva'),
        ('pendiente', 'Pendiente de Aprobación'),
        ('rechazada', 'Rechazada'),
        ('en_revision', 'En Revisión'),
    ]
    
    nombre = models.CharField(max_length=255, verbose_name="Nombre")
    nacionalidad = models.CharField(max_length=100, verbose_name="Nacionalidad")
    tipo = models.ForeignKey(
        TipoContraparte,
        on_delete=models.PROTECT,
        related_name='contrapartes',
        verbose_name="Tipo",
        limit_choices_to={'activo': True},
        help_text="Tipo de contraparte"
    )
    estado = models.CharField(
        max_length=20, 
        choices=ESTADOS_CONTRAPARTE, 
        default='pendiente',
        verbose_name="Estado"
    )
    fecha_proxima_dd = models.DateField(
        verbose_name="Próxima Debida Diligencia",
        null=True,
        blank=True,
        help_text="Fecha de la próxima renovación de debida diligencia"
    )
    
    # Campos de auditoría
    creado_por = models.ForeignKey(
        User, 
        on_delete=models.PROTECT,
        related_name='contrapartes_creadas',
        verbose_name="Creado por"
    )
    fecha_creacion = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    fecha_actualizacion = models.DateTimeField(auto_now=True, verbose_name="Última actualización")
    
    # Información adicional
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


class Miembro(models.Model):
    """
    Modelo para los miembros asociados a una contraparte
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
    Modelo para los tipos de documento
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
    Modelo para comentarios en contrapartes
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
    Modelo para documentos asociados a contrapartes
    """
    contraparte = models.ForeignKey(
        Contraparte,
        on_delete=models.CASCADE,
        related_name='documentos',
        verbose_name="Contraparte"
    )
    nombre = models.CharField(
        max_length=255,
        verbose_name="Nombre del documento"
    )
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
        return f"{self.nombre} - {self.contraparte.nombre}"
    
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
        return f"{self.nombre} - {self.contraparte.nombre}"
    
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
