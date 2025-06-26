"""
Modelos para la gestión de contrapartes
Portal Interno de Contrapartes – App Pacífico
"""

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import datetime, timedelta


class Contraparte(models.Model):
    """
    Modelo principal para las contrapartes
    """
    TIPOS_CONTRAPARTE = [
        ('empresa', 'Empresa'),
        ('persona_natural', 'Persona Natural'),
        ('entidad_publica', 'Entidad Pública'),
        ('ong', 'ONG'),
        ('otro', 'Otro'),
    ]
    
    ESTADOS_CONTRAPARTE = [
        ('activa', 'Activa'),
        ('inactiva', 'Inactiva'),
        ('pendiente', 'Pendiente de Aprobación'),
        ('rechazada', 'Rechazada'),
        ('en_revision', 'En Revisión'),
    ]
    
    nombre = models.CharField(max_length=255, verbose_name="Nombre")
    nacionalidad = models.CharField(max_length=100, verbose_name="Nacionalidad")
    tipo = models.CharField(
        max_length=20, 
        choices=TIPOS_CONTRAPARTE, 
        default='empresa',
        verbose_name="Tipo"
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
        return f"{self.nombre} ({self.get_tipo_display()})"
    
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
