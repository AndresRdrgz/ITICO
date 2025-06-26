"""
URLs para la aplicación de contrapartes
"""
from django.urls import path
from . import views

app_name = 'contrapartes'

urlpatterns = [
    # Lista y gestión de contrapartes
    path('', views.ContraparteListView.as_view(), name='lista'),
    path('crear/', views.ContraparteCreateView.as_view(), name='crear'),
    path('<int:pk>/', views.ContraparteDetailView.as_view(), name='detalle'),
    path('<int:pk>/editar/', views.ContraparteUpdateView.as_view(), name='editar'),
    path('<int:pk>/eliminar/', views.ContraparteDeleteView.as_view(), name='eliminar'),
    
    # Gestión de miembros
    path('<int:contraparte_pk>/miembros/crear/', views.MiembroCreateView.as_view(), name='miembro_crear'),
    path('<int:contraparte_pk>/miembros/ajax/crear/', views.MiembroCreateAjaxView.as_view(), name='miembro_crear_ajax'),
    path('miembros/<int:pk>/', views.MiembroDetailView.as_view(), name='miembro_detalle'),
    path('miembros/<int:pk>/editar/', views.MiembroUpdateView.as_view(), name='miembro_editar'),
    path('miembros/<int:pk>/eliminar/', views.MiembroDeleteView.as_view(), name='miembro_eliminar'),
    
    # Búsqueda y filtros
    path('buscar/', views.ContraparteBuscarView.as_view(), name='buscar'),
    
    # Exportar datos
    path('exportar/', views.ExportarContrapartesView.as_view(), name='exportar'),
]
