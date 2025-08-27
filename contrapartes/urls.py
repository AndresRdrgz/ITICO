"""
URLs para la aplicación de contrapartes
"""
from django.urls import path
from . import views

app_name = 'contrapartes'

urlpatterns = [
    # Gestión de tipos de contraparte
    path('tipos/', views.TipoContraparteListView.as_view(), name='tipo_lista'),
    path('tipos/crear/', views.TipoContraparteCreateView.as_view(), name='tipo_crear'),
    path('tipos/<int:pk>/editar/', views.TipoContraparteUpdateView.as_view(), name='tipo_editar'),
    path('tipos/<int:pk>/eliminar/', views.TipoContraparteDeleteView.as_view(), name='tipo_eliminar'),
    
    # Gestión de estados de contraparte
    path('estados/', views.EstadoContraparteListView.as_view(), name='estado_lista'),
    path('estados/crear/', views.EstadoContraparteCreateView.as_view(), name='estado_crear'),
    path('estados/<int:pk>/editar/', views.EstadoContraparteUpdateView.as_view(), name='estado_editar'),
    path('estados/<int:pk>/eliminar/', views.EstadoContraparteDeleteView.as_view(), name='estado_eliminar'),
    
    # Gestión de tipos de documento
    path('tipos-documento/', views.TipoDocumentoListView.as_view(), name='tipo_documento_lista'),
    path('tipos-documento/crear/', views.TipoDocumentoCreateView.as_view(), name='tipo_documento_crear'),
    path('tipos-documento/<int:pk>/editar/', views.TipoDocumentoUpdateView.as_view(), name='tipo_documento_editar'),
    path('tipos-documento/<int:pk>/eliminar/', views.TipoDocumentoDeleteView.as_view(), name='tipo_documento_eliminar'),
    
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
    
    # Gestión de documentos
    path('<int:contraparte_pk>/documentos/ajax/crear/', views.DocumentoCreateAjaxView.as_view(), name='documento_crear_ajax'),
    path('documentos/<int:pk>/eliminar/', views.DocumentoDeleteView.as_view(), name='documento_eliminar'),
    
    # Gestión de comentarios
    path('<int:contraparte_pk>/comentarios/ajax/crear/', views.ComentarioCreateAjaxView.as_view(), name='comentario_crear_ajax'),
    path('comentarios/<int:pk>/ajax/editar/', views.ComentarioUpdateAjaxView.as_view(), name='comentario_editar_ajax'),
    path('comentarios/<int:pk>/ajax/eliminar/', views.ComentarioDeleteAjaxView.as_view(), name='comentario_eliminar_ajax'),
    
    # Fecha DD
    path('<int:pk>/fecha-dd/ajax/actualizar/', views.ContraparteFechaDDUpdateView.as_view(), name='fecha_dd_actualizar_ajax'),
    
    # Búsqueda y filtros
    path('buscar/', views.ContraparteBuscarView.as_view(), name='buscar'),
    
    # Exportar datos
    path('exportar/', views.ExportarContrapartesView.as_view(), name='exportar'),
]
