"""
Compatibility file for Render auto-detection.
This redirects to the proper Django WSGI application.
"""

from itico.wsgi import application

# For compatibility with Render's auto-detection
app = application

if __name__ == "__main__":
    # This won't be used in production, but helps with auto-detection
    import os
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'itico.settings')
    from django.core.wsgi import get_wsgi_application
    app = get_wsgi_application()
