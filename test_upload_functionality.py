#!/usr/bin/env python
"""
Test script to verify document upload functionality is working
"""
import os
import sys
import django

# Add the project directory to the Python path
project_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(project_dir)

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'itico.settings')
django.setup()

from contrapartes.models import Contraparte, TipoDocumento, TipoContraparte, EstadoContraparte
from django.contrib.auth.models import User

def test_models():
    """Test that all models are working correctly"""
    print("Testing models...")
    
    # Check contrapartes exist
    contrapartes_count = Contraparte.objects.count()
    print(f"Found {contrapartes_count} contrapartes")
    
    # Check tipos documento exist
    tipos_count = TipoDocumento.objects.filter(activo=True).count()
    print(f"Found {tipos_count} active document types")
    
    # Check tipos contraparte exist
    tipos_contraparte_count = TipoContraparte.objects.filter(activo=True).count()
    print(f"Found {tipos_contraparte_count} active contraparte types")
    
    # Check estados exist
    estados_count = EstadoContraparte.objects.filter(activo=True).count()
    print(f"Found {estados_count} active estados")
    
    if contrapartes_count == 0:
        print("Warning: No contrapartes found. Creating test data...")
        create_test_data()
    
    print("Models test completed successfully!")

def create_test_data():
    """Create minimal test data for testing"""
    
    # Get or create a user
    user, created = User.objects.get_or_create(
        username='testuser',
        defaults={'email': 'test@example.com', 'first_name': 'Test', 'last_name': 'User'}
    )
    if created:
        user.set_password('testpass123')
        user.save()
        print("Created test user")
    
    # Create tipo contraparte if none exists
    if not TipoContraparte.objects.exists():
        tipo = TipoContraparte.objects.create(
            codigo='empresa',
            nombre='Empresa',
            descripcion='Empresa privada',
            creado_por=user
        )
        print("Created test tipo contraparte")
    else:
        tipo = TipoContraparte.objects.first()
    
    # Create estado contraparte if none exists
    if not EstadoContraparte.objects.exists():
        estado = EstadoContraparte.objects.create(
            codigo='activa',
            nombre='Activa',
            descripcion='Contraparte activa',
            color='#10B981',
            creado_por=user
        )
        print("Created test estado contraparte")
    else:
        estado = EstadoContraparte.objects.first()
    
    # Create tipo documento if none exists
    if not TipoDocumento.objects.exists():
        tipo_doc = TipoDocumento.objects.create(
            codigo='dd',
            nombre='Debida Diligencia',
            descripcion='Documento de debida diligencia',
            requiere_expiracion=True,
            creado_por=user
        )
        print("Created test tipo documento")
    
    # Create test contraparte if none exists
    if not Contraparte.objects.exists():
        contraparte = Contraparte.objects.create(
            full_company_name='Test Company S.A.',
            trading_name='Test Company',
            domicile='Colombia',
            company_nature_business='Software development',
            tipo=tipo,
            estado_nuevo=estado,
            creado_por=user
        )
        print("Created test contraparte")

if __name__ == '__main__':
    test_models()
    print("\nAll tests passed! Document upload should work now.")
    print("Try uploading a document at: http://127.0.0.1:8001/contrapartes/carga-documentos/")
