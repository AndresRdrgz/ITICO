"""
URLs para la aplicación de notificaciones
"""
from django.urls import path
from . import views

app_name = 'notificaciones'

urlpatterns = [
    # Lista de notificaciones
    path('', views.NotificacionListView.as_view(), name='lista'),
    path('<int:pk>/', views.NotificacionDetailView.as_view(), name='detalle'),
    
    # Marcar como leída
    path('<int:pk>/leer/', views.MarcarLeidaView.as_view(), name='marcar_leida'),
    path('leer-todas/', views.MarcarTodasLeidasView.as_view(), name='marcar_todas_leidas'),
    
    # Configuración
    path('configuracion/', views.ConfiguracionNotificacionView.as_view(), name='configuracion'),
    
    # API para notificaciones en tiempo real
    path('api/no-leidas/', views.NotificacionesNoLeidasAPIView.as_view(), name='api_no_leidas'),
    path('api/contar/', views.ContarNotificacionesAPIView.as_view(), name='api_contar'),
]
