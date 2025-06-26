"""
URLs para el dashboard
"""
from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    # Dashboard principal
    path('', views.DashboardView.as_view(), name='index'),
    
    # Widgets del dashboard
    path('widget/estadisticas/', views.EstadisticasWidgetView.as_view(), name='widget_estadisticas'),
    path('widget/dd-pendientes/', views.DDPendientesWidgetView.as_view(), name='widget_dd_pendientes'),
    path('widget/dd-proximas/', views.DDProximasWidgetView.as_view(), name='widget_dd_proximas'),
    path('widget/actividad-reciente/', views.ActividadRecienteWidgetView.as_view(), name='widget_actividad'),
    
    # Reportes
    path('reportes/', views.ReportesView.as_view(), name='reportes'),
    path('reportes/exportar/', views.ExportarReporteView.as_view(), name='exportar_reporte'),
]
