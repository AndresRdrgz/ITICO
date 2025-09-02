#!/usr/bin/env python
"""
Test script to verify document upload functionality
"""
import os
import django
import sys
from io import BytesIO
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import RequestFactory
from django.contrib.auth import get_user_model

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'itico.settings')
sys.path.append('/Users/andresrdrgz_/Documents/GitHub/ITICO')
django.setup()

from contrapartes.models import Contraparte, TipoDocumento
from contrapartes.views import DocumentoCreateAjaxView
from contrapartes.forms import DocumentoForm

def test_document_upload():
    print("Testing document upload functionality...")
    
    # Get or create a user
    User = get_user_model()
    user, created = User.objects.get_or_create(
        username='testuser',
        defaults={
            'email': 'test@example.com',
            'first_name': 'Test',
            'last_name': 'User'
        }
    )
    if created:
        user.set_password('password123')
        user.save()
    print(f"Using user: {user.username}")
    
    # Get a contraparte
    try:
        contraparte = Contraparte.objects.get(pk=6)
        print(f"Found contraparte: {contraparte.nombre}")
    except Contraparte.DoesNotExist:
        print("Contraparte with ID 6 not found!")
        return
    
    # Get a document type
    try:
        tipo_documento = TipoDocumento.objects.filter(activo=True).first()
        print(f"Using document type: {tipo_documento.nombre}")
    except AttributeError:
        print("No active document types found!")
        return
    
    # Create a test file
    test_file_content = b"This is a test document for upload testing."
    test_file = SimpleUploadedFile(
        "test_document.txt",
        test_file_content,
        content_type="text/plain"
    )
    
    # Test the form directly
    print("\n--- Testing DocumentoForm directly ---")
    from datetime import date, timedelta
    form_data = {
        'tipo': tipo_documento.id,
        'categoria': 'general_financial',
        'descripcion': 'Test document upload',
        'fecha_emision': date.today(),
        'fecha_expiracion': date.today() + timedelta(days=365),  # 1 year from now
    }
    form = DocumentoForm(data=form_data, files={'archivo': test_file})
    
    print(f"Form is valid: {form.is_valid()}")
    if not form.is_valid():
        print(f"Form errors: {form.errors}")
        return
    
    # Test the view
    print("\n--- Testing DocumentoCreateAjaxView ---")
    factory = RequestFactory()
    
    # Create a fresh file for the view test
    test_file_2 = SimpleUploadedFile(
        "test_document_2.txt",
        test_file_content,
        content_type="text/plain"
    )
    
    # Create POST request with proper multipart data
    request = factory.post(
        f'/contrapartes/{contraparte.pk}/documentos/ajax/crear/',
        data={
            'tipo': tipo_documento.id,
            'categoria': 'general_financial',
            'descripcion': 'Test document upload via view',
            'fecha_emision': '2025-08-28',
            'fecha_expiracion': '2026-08-28',
        },
        format='multipart'  # This is important for file uploads
    )
    # Add the file separately to FILES
    request.FILES['archivo'] = test_file_2
    request.user = user
    
    # Test the view
    view = DocumentoCreateAjaxView()
    response = view.post(request, contraparte.pk)
    
    print(f"Response status: {response.status_code}")
    print(f"Response content: {response.content.decode()}")
    
    print("\n--- Test completed successfully! ---")

if __name__ == '__main__':
    test_document_upload()
