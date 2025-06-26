"""
Configuración de Celery para ITICO
Sistema de gestión de contrapartes con debida diligencia automatizada
"""

from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from django.conf import settings

# Establecer el módulo de configuración por defecto de Django para el programa 'celery'.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'itico.settings')

app = Celery('itico')

# Usar un string aquí significa que el worker no tiene que serializar
# el objeto de configuración para los procesos hijo.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Cargar módulos de tareas de todas las apps Django registradas.
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
