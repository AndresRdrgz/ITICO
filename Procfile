release: python manage.py migrate
web: gunicorn itico.wsgi:application
worker: celery -A itico worker --loglevel=info
beat: celery -A itico beat --loglevel=info --scheduler django_celery_beat.schedulers:DatabaseScheduler
