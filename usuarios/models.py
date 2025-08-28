from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class UserProfile(models.Model):
    """Modelo para extender el perfil de usuario con campos adicionales"""
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
        """Retorna la URL de la foto de perfil o una imagen por defecto"""
        if self.profile_picture:
            return self.profile_picture.url
        return '/static/images/default-avatar.svg'

    def get_display_name(self):
        """Retorna el nombre completo o username si no hay nombre completo"""
        return self.user.get_full_name() or self.user.username


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Crear perfil automáticamente cuando se crea un usuario"""
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """Guardar perfil automáticamente cuando se actualiza un usuario"""
    if hasattr(instance, 'profile'):
        instance.profile.save()
