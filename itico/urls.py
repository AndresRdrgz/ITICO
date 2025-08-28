"""
URL configuration for itico project.
Portal Interno de Contrapartes – App Pacífico

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.shortcuts import redirect
from django.http import HttpResponseRedirect

def redirect_to_dashboard(request):
    """Redirecciona la raíz al dashboard"""
    return redirect('dashboard:index')

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),
    
    # Autenticación
    path('login/', auth_views.LoginView.as_view(template_name='auth/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    
    # Redireccionar raíz al dashboard
    path('', redirect_to_dashboard, name='home'),
    
    # Apps principales
    path('dashboard/', include('dashboard.urls')),
    path('contrapartes/', include('contrapartes.urls')),
    path('debida-diligencia/', include('debida_diligencia.urls')),
    path('notificaciones/', include('notificaciones.urls')),
    path('usuarios/', include('usuarios.urls')),
    
    # API
    path('api/', include('api.urls')),
]

# Servir archivos media en desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    
    # Debug toolbar
    if 'debug_toolbar' in settings.INSTALLED_APPS:
        import debug_toolbar
        urlpatterns = [
            path('__debug__/', include(debug_toolbar.urls)),
        ] + urlpatterns

# Configurar títulos del admin
admin.site.site_header = "ITICO - Portal de Contrapartes"
admin.site.site_title = "ITICO Admin"
admin.site.index_title = "Administración del Portal"
