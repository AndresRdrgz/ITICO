# Esto asegurará que la app siempre se importe cuando Django se inicie.
from __future__ import absolute_import, unicode_literals

from .celery import app as celery_app

__all__ = ('celery_app',)