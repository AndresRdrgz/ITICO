"""
Comando de gestión Django para verificar la configuración de la base de datos.
Se usa durante el despliegue para asegurar que PostgreSQL está configurado correctamente.
"""

from django.core.management.base import BaseCommand
from django.db import connections
from django.conf import settings
import os


class Command(BaseCommand):
    help = 'Verifica la configuración y conexión de la base de datos'

    def handle(self, *args, **options):
        # Obtener configuración de la base de datos
        db_config = settings.DATABASES['default']
        db_engine = db_config.get('ENGINE', 'Unknown')
        db_name = db_config.get('NAME', 'Unknown')
        debug_mode = settings.DEBUG
        
        self.stdout.write("=" * 60)
        self.stdout.write(self.style.HTTP_INFO("VERIFICACIÓN DE BASE DE DATOS"))
        self.stdout.write("=" * 60)
        
        # Mostrar modo de operación
        if debug_mode:
            self.stdout.write(self.style.WARNING("Modo: DESARROLLO (DEBUG=True)"))
            self.stdout.write(self.style.SUCCESS("Base de datos esperada: SQLite3"))
        else:
            self.stdout.write(self.style.HTTP_INFO("Modo: PRODUCCIÓN (DEBUG=False)"))
            self.stdout.write(self.style.SUCCESS("Base de datos esperada: PostgreSQL"))
        
        # Mostrar configuración actual
        self.stdout.write(f"Motor de BD: {db_engine}")
        self.stdout.write(f"Nombre de BD: {db_name}")
        
        # Verificar si es el motor correcto
        if debug_mode:
            if 'sqlite3' in db_engine:
                self.stdout.write(self.style.SUCCESS("✓ Configuración correcta: SQLite3 para desarrollo"))
            else:
                self.stdout.write(self.style.ERROR("✗ Error: Se esperaba SQLite3 para desarrollo"))
        else:
            if 'postgresql' in db_engine:
                self.stdout.write(self.style.SUCCESS("✓ Configuración correcta: PostgreSQL para producción"))
            else:
                self.stdout.write(self.style.ERROR("✗ Error: Se esperaba PostgreSQL para producción"))
        
        # Verificar variables de entorno importantes
        self.stdout.write("\nVariables de entorno:")
        database_url = os.environ.get('DATABASE_URL', 'No configurada')
        debug_env = os.environ.get('DEBUG', 'No configurada')
        
        self.stdout.write(f"DEBUG: {debug_env}")
        if not debug_mode:
            if database_url != 'No configurada':
                self.stdout.write(f"DATABASE_URL: {database_url[:50]}..." if len(database_url) > 50 else f"DATABASE_URL: {database_url}")
            else:
                self.stdout.write(self.style.ERROR("DATABASE_URL: No configurada (¡Requerida en producción!)"))
        
        # Probar la conexión
        self.stdout.write("\nProbando conexión a la base de datos...")
        try:
            connection = connections['default']
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
                result = cursor.fetchone()
                if result:
                    self.stdout.write(self.style.SUCCESS("✓ Conexión exitosa a la base de datos"))
                else:
                    self.stdout.write(self.style.ERROR("✗ Error en la conexión"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"✗ Error de conexión: {e}"))
        
        self.stdout.write("=" * 60)

from django.core.management.base import BaseCommand
from django.conf import settings
from django.db import connection
import os


class Command(BaseCommand):
    help = 'Verifica la configuración de la base de datos'

    def handle(self, *args, **options):
        self.stdout.write("=" * 60)
        self.stdout.write("🔍 VERIFICACIÓN DE BASE DE DATOS")
        self.stdout.write("=" * 60)
        
        # Información de configuración
        db_config = settings.DATABASES['default']
        
        self.stdout.write(f"Engine: {db_config.get('ENGINE', 'No definido')}")
        self.stdout.write(f"Name: {db_config.get('NAME', 'No definido')}")
        self.stdout.write(f"User: {db_config.get('USER', 'No definido')}")
        self.stdout.write(f"Host: {db_config.get('HOST', 'No definido')}")
        self.stdout.write(f"Port: {db_config.get('PORT', 'No definido')}")
        
        # Variables de entorno
        self.stdout.write("\n📋 VARIABLES DE ENTORNO:")
        self.stdout.write(f"DATABASE_URL: {'✅ Configurada' if os.environ.get('DATABASE_URL') else '❌ No configurada'}")
        self.stdout.write(f"DEBUG: {os.environ.get('DEBUG', 'No definida')}")
        
        # Intentar conexión
        self.stdout.write("\n🔌 PRUEBA DE CONEXIÓN:")
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT version();")
                version = cursor.fetchone()[0]
                self.stdout.write(self.style.SUCCESS(f"✅ Conexión exitosa: {version}"))
                
                # Verificar si es PostgreSQL
                if 'PostgreSQL' in version:
                    self.stdout.write(self.style.SUCCESS("✅ Usando PostgreSQL correctamente"))
                else:
                    self.stdout.write(self.style.WARNING(f"⚠️ No es PostgreSQL: {version}"))
                    
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"❌ Error de conexión: {e}"))
            
        # Verificar tablas
        self.stdout.write("\n📊 VERIFICACIÓN DE TABLAS:")
        try:
            from django.db import connection
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT table_name 
                    FROM information_schema.tables 
                    WHERE table_schema = 'public' 
                    AND table_name LIKE 'auth_%'
                """)
                tables = cursor.fetchall()
                
                if tables:
                    self.stdout.write(self.style.SUCCESS(f"✅ Encontradas {len(tables)} tablas de autenticación"))
                    for table in tables[:3]:  # Mostrar solo las primeras 3
                        self.stdout.write(f"  - {table[0]}")
                else:
                    self.stdout.write(self.style.WARNING("⚠️ No se encontraron tablas de autenticación"))
                    
        except Exception as e:
            self.stdout.write(self.style.WARNING(f"⚠️ No se pudieron verificar tablas: {e}"))
            
        self.stdout.write("=" * 60)
