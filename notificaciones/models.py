"""
Modelos para el sistema de notificaciones
Portal Interno de Contrapartes – App Pacífico (Cotizador Web)

ESTRUCTURA DE MODELOS:
1. Notificacion: Notificaciones del sistema con diferentes tipos y prioridades
2. ConfiguracionNotificacion: Configuraciones personalizadas por usuario
3. HistorialNotificacion: Auditoría de notificaciones enviadas

FUNCIONALIDADES PRINCIPALES:
- Sistema de notificaciones multi-canal (sistema, email, SMS, webhook)
- Configuración personalizada por usuario
- Diferentes tipos de notificaciones (DD, coincidencias, recordatorios)
- Sistema de prioridades (baja, normal, alta, urgente)
- Historial completo para auditoría
- Enlaces a objetos relacionados (contrapartes, miembros, DD)
"""

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


# =============================================================================
# MODELO PRINCIPAL DE NOTIFICACIONES
# =============================================================================

class Notificacion(models.Model):
    """
    Modelo principal para las notificaciones del sistema.
    
    Gestiona todas las notificaciones enviadas a los usuarios, incluyendo
    diferentes tipos (debida diligencia, coincidencias, recordatorios) y
    prioridades. Permite enlaces a objetos relacionados y URLs de acción.
    
    Tipos de notificaciones:
    - dd_completada: Debida Diligencia completada
    - dd_fallida: Debida Diligencia fallida
    - coincidencia_encontrada: Coincidencia encontrada en búsquedas
    - dd_proxima: Debida Diligencia próxima a vencer
    - dd_vencida: Debida Diligencia vencida
    - revision_requerida: Revisión requerida
    - aprobacion_pendiente: Aprobación pendiente
    - sistema: Notificación del sistema
    - recordatorio: Recordatorio general
    
    Prioridades:
    - baja: Prioridad baja
    - normal: Prioridad normal
    - alta: Prioridad alta
    - urgente: Prioridad urgente
    """
    TIPOS = [
        ('dd_completada', 'Debida Diligencia Completada'),
        ('dd_fallida', 'Debida Diligencia Fallida'),
        ('coincidencia_encontrada', 'Coincidencia Encontrada'),
        ('dd_proxima', 'Debida Diligencia Próxima a Vencer'),
        ('dd_vencida', 'Debida Diligencia Vencida'),
        ('revision_requerida', 'Revisión Requerida'),
        ('aprobacion_pendiente', 'Aprobación Pendiente'),
        ('sistema', 'Notificación del Sistema'),
        ('recordatorio', 'Recordatorio'),
    ]
    
    PRIORIDADES = [
        ('baja', 'Baja'),
        ('normal', 'Normal'),
        ('alta', 'Alta'),
        ('urgente', 'Urgente'),
    ]
    
    usuario = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='notificaciones',
        verbose_name="Usuario"
    )
    tipo = models.CharField(
        max_length=30,
        choices=TIPOS,
        verbose_name="Tipo de notificación"
    )
    titulo = models.CharField(max_length=255, verbose_name="Título")
    mensaje = models.TextField(verbose_name="Mensaje")
    prioridad = models.CharField(
        max_length=20,
        choices=PRIORIDADES,
        default='normal',
        verbose_name="Prioridad"
    )
    leida = models.BooleanField(default=False, verbose_name="¿Leída?")
    fecha_creacion = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    fecha_lectura = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Fecha de lectura"
    )
    
    # Enlaces opcionales a otros objetos
    contraparte_id = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name="ID de Contraparte relacionada"
    )
    miembro_id = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name="ID de Miembro relacionado"
    )
    debida_diligencia_id = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name="ID de Debida Diligencia relacionada"
    )
    
    # URL para redireccionar al hacer clic
    url_accion = models.URLField(
        blank=True,
        null=True,
        verbose_name="URL de acción"
    )
    
    class Meta:
        verbose_name = "Notificación"
        verbose_name_plural = "Notificaciones"
        ordering = ['-fecha_creacion']
        indexes = [
            models.Index(fields=['usuario', 'leida']),
            models.Index(fields=['fecha_creacion']),
            models.Index(fields=['tipo']),
        ]
    
    def __str__(self):
        return f"{self.titulo} - {self.usuario.get_full_name() or self.usuario.username}"
    
    def marcar_como_leida(self):
        """
        Marca la notificación como leída y actualiza la fecha de lectura.
        
        Actualiza los campos 'leida' y 'fecha_lectura' solo si la notificación
        no estaba previamente marcada como leída.
        """
        if not self.leida:
            self.leida = True
            self.fecha_lectura = timezone.now()
            self.save(update_fields=['leida', 'fecha_lectura'])
    
    @property
    def hace_cuanto(self):
        """
        Retorna una cadena amigable indicando hace cuánto se creó la notificación.
        
        Returns:
            str: Descripción amigable del tiempo transcurrido (ej: "hace 2 horas")
        """
        now = timezone.now()
        diff = now - self.fecha_creacion
        
        if diff.days > 0:
            return f"hace {diff.days} día{'s' if diff.days > 1 else ''}"
        elif diff.seconds > 3600:
            hours = diff.seconds // 3600
            return f"hace {hours} hora{'s' if hours > 1 else ''}"
        elif diff.seconds > 60:
            minutes = diff.seconds // 60
            return f"hace {minutes} minuto{'s' if minutes > 1 else ''}"
        else:
            return "hace un momento"


# =============================================================================
# CONFIGURACIÓN DE NOTIFICACIONES
# =============================================================================

class ConfiguracionNotificacion(models.Model):
    """
    Configuración personalizada de notificaciones por usuario.
    
    Permite a cada usuario configurar qué tipos de notificaciones desea recibir
    y por qué canales (email, sistema). Incluye configuraciones para diferentes
    tipos de eventos y recordatorios.
    
    Configuraciones disponibles:
    - Email: Configuraciones para notificaciones por correo electrónico
    - Sistema: Configuraciones para notificaciones en el sistema
    - Recordatorios: Configuración de días de aviso para DD
    """
    usuario = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='config_notificaciones',
        verbose_name="Usuario"
    )
    
    # Configuraciones de email
    email_dd_completada = models.BooleanField(
        default=True,
        verbose_name="Email al completarse DD"
    )
    email_coincidencias = models.BooleanField(
        default=True,
        verbose_name="Email por coincidencias encontradas"
    )
    email_dd_proxima = models.BooleanField(
        default=True,
        verbose_name="Email por DD próxima a vencer"
    )
    email_resumen_diario = models.BooleanField(
        default=False,
        verbose_name="Resumen diario por email"
    )
    
    # Configuraciones de notificaciones en sistema
    notif_dd_completada = models.BooleanField(
        default=True,
        verbose_name="Notificación en sistema al completarse DD"
    )
    notif_coincidencias = models.BooleanField(
        default=True,
        verbose_name="Notificación por coincidencias"
    )
    notif_dd_proxima = models.BooleanField(
        default=True,
        verbose_name="Notificación por DD próxima"
    )
    
    # Configuración de recordatorios
    dias_aviso_dd = models.PositiveIntegerField(
        default=30,
        verbose_name="Días de aviso antes de vencimiento DD"
    )
    
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Configuración de Notificaciones"
        verbose_name_plural = "Configuraciones de Notificaciones"
    
    def __str__(self):
        return f"Config. Notif. - {self.usuario.get_full_name() or self.usuario.username}"


# =============================================================================
# HISTORIAL DE NOTIFICACIONES
# =============================================================================

class HistorialNotificacion(models.Model):
    """
    Historial de notificaciones enviadas para auditoría y seguimiento.
    
    Registra cada intento de envío de notificación a través de diferentes
    canales, incluyendo el estado del envío, fechas y mensajes de error.
    Proporciona trazabilidad completa del sistema de notificaciones.
    
    Canales disponibles:
    - sistema: Notificación en el sistema
    - email: Correo electrónico
    - sms: Mensaje de texto
    - webhook: Llamada a webhook externo
    
    Estados:
    - pendiente: Envió pendiente
    - enviada: Enviada exitosamente
    - fallida: Falló el envío
    - entregada: Confirmada la entrega
    """
    CANALES = [
        ('sistema', 'Sistema'),
        ('email', 'Email'),
        ('sms', 'SMS'),
        ('webhook', 'Webhook'),
    ]
    
    ESTADOS = [
        ('pendiente', 'Pendiente'),
        ('enviada', 'Enviada'),
        ('fallida', 'Fallida'),
        ('entregada', 'Entregada'),
    ]
    
    notificacion = models.ForeignKey(
        Notificacion,
        on_delete=models.CASCADE,
        related_name='historial',
        verbose_name="Notificación"
    )
    canal = models.CharField(
        max_length=20,
        choices=CANALES,
        verbose_name="Canal de envío"
    )
    estado = models.CharField(
        max_length=20,
        choices=ESTADOS,
        default='pendiente',
        verbose_name="Estado"
    )
    destinatario = models.CharField(
        max_length=255,
        verbose_name="Destinatario"
    )
    fecha_envio = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de envío")
    fecha_entrega = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Fecha de entrega"
    )
    mensaje_error = models.TextField(
        blank=True,
        null=True,
        verbose_name="Mensaje de error"
    )
    
    class Meta:
        verbose_name = "Historial de Notificación"
        verbose_name_plural = "Historial de Notificaciones"
        ordering = ['-fecha_envio']
    
    def __str__(self):
        return f"{self.canal} - {self.notificacion.titulo} - {self.estado}"
