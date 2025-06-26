"""
URLs para la API REST - Temporal simplificado
"""
from django.urls import path
from . import views

app_name = 'api'

urlpatterns = [
    # Endpoints básicos temporales
    path('v1/test/', views.TestAPIView.as_view(), name='test'),
]
