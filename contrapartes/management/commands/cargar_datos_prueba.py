"""
Comando de gestión para cargar datos de prueba en ITICO
"""
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from contrapartes.models import Contraparte, Miembro
from debida_diligencia.models import DebidaDiligencia, Busqueda
from notificaciones.models import Notificacion, ConfiguracionNotificacion
from datetime import datetime, timedelta
from django.utils import timezone


class Command(BaseCommand):
    help = 'Carga datos de prueba para el sistema ITICO'

    def add_arguments(self, parser):
        parser.add_argument(
            '--reset',
            action='store_true',
            help='Elimina todos los datos existentes antes de cargar nuevos datos'
        )

    def handle(self, *args, **options):
        if options['reset']:
            self.stdout.write('Eliminando datos existentes...')
            Notificacion.objects.all().delete()
            Busqueda.objects.all().delete()
            DebidaDiligencia.objects.all().delete()
            Miembro.objects.all().delete()
            Contraparte.objects.all().delete()
            
        self.stdout.write('Cargando datos de prueba...')
        
        # Crear usuarios de prueba
        admin_user, created = User.objects.get_or_create(
            username='gabriela',
            defaults={
                'first_name': 'Gabriela',
                'last_name': 'Rodríguez',
                'email': 'gabriela@pacifico.com',
                'is_staff': True,
            }
        )
        if created:
            admin_user.set_password('test123')
            admin_user.save()
            self.stdout.write(f'✓ Usuario creado: {admin_user.username}')
        
        # Crear contrapartes de prueba
        contrapartes_data = [
            {
                'nombre': 'Reaseguros Internacionales S.A.',
                'nacionalidad': 'España',
                'tipo': 'empresa',
                'estado': 'activa',
                'descripcion': 'Compañía reaseguradora especializada en seguros de vida y daños.'
            },
            {
                'nombre': 'Global Insurance Corp',
                'nacionalidad': 'Estados Unidos',
                'tipo': 'empresa',
                'estado': 'pendiente',
                'descripcion': 'Empresa multinacional de seguros con presencia en América Latina.'
            },
            {
                'nombre': 'European Re Ltd',
                'nacionalidad': 'Reino Unido',
                'tipo': 'empresa',
                'estado': 'en_revision',
                'descripcion': 'Reaseguradora europea con enfoque en mercados emergentes.'
            },
            {
                'nombre': 'Fundación Seguros Solidarios',
                'nacionalidad': 'Colombia',
                'tipo': 'ong',
                'estado': 'activa',
                'descripcion': 'Fundación sin ánimo de lucro que promueve el acceso a seguros.'
            },
        ]
        
        contrapartes_creadas = []
        for data in contrapartes_data:
            contraparte, created = Contraparte.objects.get_or_create(
                nombre=data['nombre'],
                defaults={
                    **data,
                    'creado_por': admin_user,
                    'fecha_proxima_dd': timezone.now().date() + timedelta(days=300)
                }
            )
            contrapartes_creadas.append(contraparte)
            if created:
                self.stdout.write(f'✓ Contraparte creada: {contraparte.nombre}')
        
        # Crear miembros para cada contraparte
        miembros_data = [
            {
                'nombre': 'Carlos Eduardo Mendoza',
                'documento_identidad': '12345678',
                'tipo_documento': 'cedula',
                'fecha_nacimiento': datetime(1975, 3, 15).date(),
                'nacionalidad': 'España',
                'rol': 'ceo'
            },
            {
                'nombre': 'Maria Isabel García',
                'documento_identidad': '87654321',
                'tipo_documento': 'cedula',
                'fecha_nacimiento': datetime(1980, 7, 22).date(),
                'nacionalidad': 'España',
                'rol': 'accionista'
            },
            {
                'nombre': 'John Michael Smith',
                'documento_identidad': 'P123456789',
                'tipo_documento': 'pasaporte',
                'fecha_nacimiento': datetime(1970, 11, 8).date(),
                'nacionalidad': 'Estados Unidos',
                'rol': 'ceo'
            },
            {
                'nombre': 'Sarah Elizabeth Johnson',
                'documento_identidad': 'P987654321',
                'tipo_documento': 'pasaporte',
                'fecha_nacimiento': datetime(1985, 2, 14).date(),
                'nacionalidad': 'Estados Unidos',
                'rol': 'director'
            },
        ]
        
        for i, contraparte in enumerate(contrapartes_creadas[:2]):  # Solo para las primeras 2
            for j in range(2):  # 2 miembros por contraparte
                miembro_data = miembros_data[i * 2 + j]
                miembro, created = Miembro.objects.get_or_create(
                    contraparte=contraparte,
                    documento_identidad=miembro_data['documento_identidad'],
                    defaults={
                        **miembro_data,
                        'contraparte': contraparte
                    }
                )
                if created:
                    self.stdout.write(f'✓ Miembro creado: {miembro.nombre}')
        
        # Crear algunas debidas diligencias
        miembros = Miembro.objects.all()[:3]
        for miembro in miembros:
            dd, created = DebidaDiligencia.objects.get_or_create(
                miembro=miembro,
                defaults={
                    'solicitado_por': admin_user,
                    'estado': 'en_proceso',
                    'resumen_ia': f'Análisis preliminar para {miembro.nombre}. Búsquedas en proceso.',
                }
            )
            if created:
                self.stdout.write(f'✓ Debida Diligencia creada para: {miembro.nombre}')
                
                # Crear algunas búsquedas
                fuentes = ['ofac', 'onu', 'medios']
                for fuente in fuentes:
                    busqueda, created = Busqueda.objects.get_or_create(
                        debida_diligencia=dd,
                        fuente=fuente,
                        defaults={
                            'estado': 'sin_coincidencias',
                            'resultado': f'Búsqueda realizada en {fuente}. No se encontraron coincidencias.',
                            'coincidencias_encontradas': 0
                        }
                    )
                    if created:
                        self.stdout.write(f'  ✓ Búsqueda creada: {fuente}')
        
        # Crear configuraciones de notificación
        for user in User.objects.all():
            config, created = ConfiguracionNotificacion.objects.get_or_create(
                usuario=user,
                defaults={
                    'email_dd_completada': True,
                    'email_coincidencias': True,
                    'email_dd_proxima': True,
                    'notif_dd_completada': True,
                    'notif_coincidencias': True,
                    'notif_dd_proxima': True,
                    'dias_aviso_dd': 30
                }
            )
            if created:
                self.stdout.write(f'✓ Configuración de notificaciones creada para: {user.username}')
        
        # Crear algunas notificaciones de prueba
        notificaciones_data = [
            {
                'tipo': 'dd_completada',
                'titulo': 'Debida Diligencia Completada',
                'mensaje': f'La debida diligencia de {miembros[0].nombre} ha sido completada exitosamente.',
                'prioridad': 'normal'
            },
            {
                'tipo': 'dd_proxima',
                'titulo': 'Debida Diligencia Próxima a Vencer',
                'mensaje': f'La debida diligencia de {contrapartes_creadas[0].nombre} vence en 15 días.',
                'prioridad': 'alta'
            },
            {
                'tipo': 'sistema',
                'titulo': 'Bienvenido al Sistema ITICO',
                'mensaje': 'El sistema ha sido configurado exitosamente. Puedes comenzar a gestionar contrapartes.',
                'prioridad': 'baja'
            }
        ]
        
        for notif_data in notificaciones_data:
            notif, created = Notificacion.objects.get_or_create(
                usuario=admin_user,
                titulo=notif_data['titulo'],
                defaults=notif_data
            )
            if created:
                self.stdout.write(f'✓ Notificación creada: {notif.titulo}')
        
        self.stdout.write(
            self.style.SUCCESS(
                '\n🎉 Datos de prueba cargados exitosamente!\n'
                '\nUsuarios creados:'
                f'\n  - Usuario: gabriela | Contraseña: test123'
                f'\n  - Usuario: admin | Contraseña: [la que configuraste]'
                '\n\nPuedes iniciar sesión con cualquiera de estos usuarios.'
                '\n\nEjecuta: python manage.py runserver'
                '\nY visita: http://127.0.0.1:8000/'
            )
        )
