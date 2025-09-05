"""
Modelos para la gestión de usuarios
Portal Interno de Contrapartes – App Pacífico (Cotizador Web)

ESTRUCTURA DE MODELOS:
1. UserProfile: Extensión del modelo User de Django con campos adicionales
2. Signals: Creación automática de perfiles al crear usuarios

FUNCIONALIDADES PRINCIPALES:
- Extensión del sistema de usuarios de Django
- Perfiles con información adicional (foto, teléfono, departamento, cargo)
- Creación automática de perfiles mediante signals
- Métodos de utilidad para obtener información del perfil
"""

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


# =============================================================================
# MODELO DE PERFIL DE USUARIO
# =============================================================================

class UserProfile(models.Model):
    """
    Modelo para extender el perfil de usuario con campos adicionales.
    
    Extiende el modelo User de Django agregando información específica del
    negocio como foto de perfil, teléfono, departamento y cargo. Se crea
    automáticamente cuando se registra un nuevo usuario.
    
    Características:
    - Relación OneToOne con el modelo User de Django
    - Campos opcionales para información adicional
    - Métodos de utilidad para obtener URLs y nombres de visualización
    - Auditoría de fechas de creación y actualización
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    profile_picture = models.ImageField(
        upload_to='usuarios/profile_pictures/',
        blank=True,
        null=True,
        verbose_name='Foto de perfil'
    )
    phone = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        verbose_name='Teléfono'
    )
    department = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name='Departamento'
    )
    position = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name='Cargo'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Última actualización')

    class Meta:
        verbose_name = 'Perfil de Usuario'
        verbose_name_plural = 'Perfiles de Usuario'
        ordering = ['-updated_at']

    def __str__(self):
        return f"Perfil de {self.user.get_full_name() or self.user.username}"

    def get_profile_picture_url(self):
        """
        Retorna la URL de la foto de perfil o una imagen por defecto.
        
        Returns:
            str: URL de la foto de perfil o URL de imagen por defecto
        """
        if self.profile_picture:
            return self.profile_picture.url
        return '/static/images/default-avatar.svg'

    def get_display_name(self):
        """
        Retorna el nombre completo o username si no hay nombre completo.
        
        Returns:
            str: Nombre completo del usuario o username como fallback
        """
        return self.user.get_full_name() or self.user.username


# =============================================================================
# SIGNALS PARA CREACIÓN AUTOMÁTICA DE PERFILES
# =============================================================================

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """
    Crear perfil automáticamente cuando se crea un usuario.
    
    Signal que se ejecuta después de crear un nuevo usuario para crear
    automáticamente su perfil asociado con valores por defecto.
    """
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """
    Guardar perfil automáticamente cuando se actualiza un usuario.
    
    Signal que se ejecuta después de actualizar un usuario para asegurar
    que su perfil también se mantenga sincronizado.
    """
    if hasattr(instance, 'profile'):
        instance.profile.save()
