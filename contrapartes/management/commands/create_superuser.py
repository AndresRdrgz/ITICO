"""
Comando de gestión Django para crear un superusuario automáticamente.
Se usa durante el despliegue en Render para crear el usuario administrador.
"""

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.db import IntegrityError
import os


class Command(BaseCommand):
    help = 'Crea un superusuario automáticamente si no existe'

    def handle(self, *args, **options):
        User = get_user_model()
        
        # Obtener credenciales desde variables de entorno o usar valores por defecto
        username = os.environ.get('DJANGO_SUPERUSER_USERNAME', 'admin')
        email = os.environ.get('DJANGO_SUPERUSER_EMAIL', 'admin@itico.com')
        password = os.environ.get('DJANGO_SUPERUSER_PASSWORD', 'admin123')
        
        try:
            # Verificar si ya existe un superusuario con este username
            if User.objects.filter(username=username).exists():
                self.stdout.write(
                    self.style.WARNING(f'El superusuario "{username}" ya existe.')
                )
                return
            
            # Crear el superusuario
            User.objects.create_superuser(
                username=username,
                email=email,
                password=password
            )
            
            self.stdout.write(
                self.style.SUCCESS(f'Superusuario "{username}" creado exitosamente.')
            )
            self.stdout.write(
                self.style.SUCCESS(f'Email: {email}')
            )
            self.stdout.write(
                self.style.WARNING('Recuerda cambiar la contraseña después del primer login.')
            )
            
        except IntegrityError as e:
            self.stdout.write(
                self.style.ERROR(f'Error al crear superusuario: {e}')
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error inesperado: {e}')
            )
