"""
URLs para la aplicación de debida diligencia
"""
from django.urls import path
from . import views

app_name = 'debida_diligencia'

urlpatterns = [
    # Lista de debidas diligencias
    path('', views.DebidaDiligenciaListView.as_view(), name='lista'),
    path('<int:pk>/', views.DebidaDiligenciaDetailView.as_view(), name='detalle'),
    
    # Solicitar nueva debida diligencia
    path('solicitar/<int:miembro_pk>/', views.SolicitarDDView.as_view(), name='solicitar'),
    
    # Gestión de proceso
    path('<int:pk>/revisar/', views.RevisarDDView.as_view(), name='revisar'),
    path('<int:pk>/aprobar/', views.AprobarDDView.as_view(), name='aprobar'),
    path('<int:pk>/rechazar/', views.RechazarDDView.as_view(), name='rechazar'),
    
    # Búsquedas y análisis
    path('<int:pk>/busquedas/', views.BusquedaListView.as_view(), name='busquedas'),
    path('busquedas/<int:pk>/', views.BusquedaDetailView.as_view(), name='busqueda_detalle'),
    path('<int:pk>/analisis-ia/', views.AnalisisIAView.as_view(), name='analisis_ia'),
    
    # Calendario
    path('calendario/', views.CalendarioDDView.as_view(), name='calendario'),
    
    # Reportes
    path('reportes/', views.ReportesDDView.as_view(), name='reportes'),
    
    # API endpoints para integración con RPA
    path('api/webhook/makito/', views.MakitoWebhookView.as_view(), name='makito_webhook'),
    path('api/resultado/<int:dd_pk>/', views.RecibirResultadoView.as_view(), name='recibir_resultado'),
]
