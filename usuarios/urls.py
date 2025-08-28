from django.urls import path
from . import views

app_name = 'usuarios'

urlpatterns = [
    path('perfil/editar/', views.profile_edit, name='profile_edit'),
    path('perfil/ver/', views.profile_view, name='profile_view'),
    path('perfil/cambiar-contrasena/', views.change_password, name='change_password'),
    path('perfil/subir-foto/', views.upload_profile_picture, name='upload_profile_picture'),
    path('perfil/eliminar-foto/', views.delete_profile_picture, name='delete_profile_picture'),
]
