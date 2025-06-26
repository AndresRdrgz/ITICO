"""
Modelos para el proceso de debida diligencia
Portal Interno de Contrapartes – App Pacífico
"""

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from contrapartes.models import Miembro


class DebidaDiligencia(models.Model):
    """
    Modelo principal para el proceso de debida diligencia
    """
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
    
    miembro = models.ForeignKey(
        Miembro,
        on_delete=models.CASCADE,
        related_name='debidas_diligencias',
        verbose_name="Miembro"
    )
    fecha_solicitud = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de solicitud")
    fecha_resultado = models.DateTimeField(
        null=True, 
        blank=True,
        verbose_name="Fecha de resultado"
    )
    estado = models.CharField(
        max_length=20,
        choices=ESTADOS,
        default='pendiente',
        verbose_name="Estado"
    )
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
    fecha_aprobacion = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Fecha de aprobación"
    )
    
    # Campos técnicos para integración con RPA
    makito_request_id = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="ID de solicitud en Makito"
    )
    
    # Campos de auditoría
    solicitado_por = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='dd_solicitadas',
        verbose_name="Solicitado por"
    )
    fecha_actualizacion = models.DateTimeField(auto_now=True, verbose_name="Última actualización")
    
    class Meta:
        verbose_name = "Debida Diligencia"
        verbose_name_plural = "Debidas Diligencias"
        ordering = ['-fecha_solicitud']
    
    def __str__(self):
        return f"DD {self.id} - {self.miembro.nombre} ({self.get_estado_display()})"
    
    def save(self, *args, **kwargs):
        # Actualizar fecha de resultado cuando cambia el estado
        if self.estado == 'completada' and not self.fecha_resultado:
            self.fecha_resultado = timezone.now()
        super().save(*args, **kwargs)
    
    @property
    def duracion_proceso(self):
        """Retorna la duración del proceso en días"""
        if self.fecha_resultado:
            delta = self.fecha_resultado - self.fecha_solicitud
            return delta.days
        return None
    
    @property
    def tiene_coincidencias(self):
        """Retorna True si hay búsquedas con coincidencias positivas"""
        return self.busquedas.filter(estado='coincidencia_positiva').exists()


class Busqueda(models.Model):
    """
    Modelo para las búsquedas individuales realizadas por el RPA
    """
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
    
    debida_diligencia = models.ForeignKey(
        DebidaDiligencia,
        on_delete=models.CASCADE,
        related_name='busquedas',
        verbose_name="Debida Diligencia"
    )
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
    fecha_busqueda = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de búsqueda")
    
    # Metadatos de la búsqueda
    url_fuente = models.URLField(
        blank=True,
        null=True,
        verbose_name="URL de la fuente"
    )
    coincidencias_encontradas = models.PositiveIntegerField(
        default=0,
        verbose_name="Número de coincidencias encontradas"
    )
    
    class Meta:
        verbose_name = "Búsqueda"
        verbose_name_plural = "Búsquedas"
        ordering = ['-fecha_busqueda']
    
    def __str__(self):
        return f"{self.get_fuente_display()} - {self.debida_diligencia.miembro.nombre}"
    
    @property
    def es_positiva(self):
        """Retorna True si la búsqueda encontró coincidencias"""
        return self.estado == 'coincidencia_positiva' or self.coincidencias_encontradas > 0


class AnalisisIA(models.Model):
    """
    Modelo para almacenar análisis detallados de IA
    """
    TIPOS_ANALISIS = [
        ('texto', 'Análisis de Texto'),
        ('documento', 'Análisis de Documento'),
        ('resumen', 'Resumen Automatizado'),
        ('clasificacion', 'Clasificación de Riesgo'),
    ]
    
    debida_diligencia = models.ForeignKey(
        DebidaDiligencia,
        on_delete=models.CASCADE,
        related_name='analisis_ia',
        verbose_name="Debida Diligencia"
    )
    tipo_analisis = models.CharField(
        max_length=20,
        choices=TIPOS_ANALISIS,
        verbose_name="Tipo de análisis"
    )
    texto_analizado = models.TextField(verbose_name="Texto analizado")
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
    fecha_analisis = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de análisis")
    
    class Meta:
        verbose_name = "Análisis de IA"
        verbose_name_plural = "Análisis de IA"
        ordering = ['-fecha_analisis']
    
    def __str__(self):
        return f"{self.get_tipo_analisis_display()} - {self.debida_diligencia.miembro.nombre}"
