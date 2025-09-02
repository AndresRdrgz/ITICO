"""
API views for document management in contrapartes app
Handles AJAX requests for document CRUD operations from detalle.html template
"""

import os
from collections import defaultdict
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage
from django.conf import settings

from .models import Contraparte, Documento, TipoDocumento
from .forms import DocumentoForm


@login_required
@require_http_methods(["GET"])
def load_document_form(request, contraparte_pk):
    """
    Load the document form for creating a new document
    
    Args:
        request: HTTP request object
        contraparte_pk: Primary key of the contraparte
        
    Returns:
        JsonResponse with form HTML or error message
    """
    try:
        contraparte = get_object_or_404(Contraparte, pk=contraparte_pk)
        
        # Create empty form for new document
        form = DocumentoForm()
        
        # Get active document types for the form
        tipos_documento = TipoDocumento.objects.filter(activo=True).order_by('nombre')
        
        # Render the form template
        form_html = render_to_string('contrapartes/documento_form_modal.html', {
            'form': form,
            'contraparte': contraparte,
            'tipos_documento': tipos_documento,
            'documento': None,  # New document
        }, request=request)
        
        return JsonResponse({
            'success': True,
            'form_html': form_html
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': f'Error al cargar el formulario: {str(e)}'
        })


@login_required
@require_http_methods(["POST"])
def save_document_form(request, contraparte_pk):
    """
    Save a new document via AJAX
    
    Args:
        request: HTTP request object with form data and file
        contraparte_pk: Primary key of the contraparte
        
    Returns:
        JsonResponse with success/error message and updated document list HTML
    """
    try:
        contraparte = get_object_or_404(Contraparte, pk=contraparte_pk)
        
        # Create form with submitted data
        form = DocumentoForm(request.POST, request.FILES)

        if form.is_valid():
            # Create the document instance but don't save yet
            documento = form.save(commit=False)
            documento.contraparte = contraparte
            documento.subido_por = request.user
            
            # Save the document
            documento.save()
            
            # Get updated documents grouped by category
            documentos_agrupados = _get_documentos_agrupados(contraparte)
            
            # Render updated documents list
            documentos_html = render_to_string('contrapartes/documentos_list_partial.html', {
                'object': contraparte,
                'documentos_por_categoria': documentos_agrupados,
            }, request=request)
            
            return JsonResponse({
                'success': True,
                'message': 'Documento subido exitosamente',
                'documentos_html': documentos_html,
                'documentos_count': contraparte.documentos.filter(activo=True).count()
            })
        else:
            # Form has errors, return form with errors
            tipos_documento = TipoDocumento.objects.filter(activo=True).order_by('nombre')
            form_html = render_to_string('contrapartes/documento_form_modal.html', {
                'form': form,
                'contraparte': contraparte,
                'tipos_documento': tipos_documento,
                'documento': None,
            }, request=request)
            
            return JsonResponse({
                'success': False,
                'form_html': form_html,
                'errors': form.errors
            })
            
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': f'Error al guardar el documento: {str(e)}'
        })
    
    
@login_required
@require_http_methods(["GET"])
def load_document_edit_form(request, documento_pk):
    """
    Load the document form for editing an existing document
    
    Args:
        request: HTTP request object
        documento_pk: Primary key of the document to edit
        
    Returns:
        JsonResponse with form HTML or error message
    """
    try:
        documento = get_object_or_404(Documento, pk=documento_pk)
        
        # Check if user can edit this document
        if documento.subido_por != request.user and not request.user.is_staff:
            return JsonResponse({
                'success': False,
                'error': 'No tiene permisos para editar este documento'
            })
        
        # Create form with existing document instance
        form = DocumentoForm(instance=documento)
        
        # Get active document types for the form
        tipos_documento = TipoDocumento.objects.filter(activo=True).order_by('nombre')
        
        # Render the form template
        form_html = render_to_string('contrapartes/documento_form_modal.html', {
            'form': form,
            'contraparte': documento.contraparte,
            'tipos_documento': tipos_documento,
            'documento': documento,  # Existing document for editing
        }, request=request)
        
        return JsonResponse({
            'success': True,
            'form_html': form_html
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': f'Error al cargar el formulario: {str(e)}'
        })


@login_required
@require_http_methods(["POST"])
def save_document_edit_form(request, documento_pk):
    """
    Save an edited document via AJAX
    
    Args:
        request: HTTP request object with form data and optional file
        documento_pk: Primary key of the document to edit
        
    Returns:
        JsonResponse with success/error message and updated document list HTML
    """
    try:
        documento = get_object_or_404(Documento, pk=documento_pk)
        
        # Check if user can edit this document
        if documento.subido_por != request.user and not request.user.is_staff:
            return JsonResponse({
                'success': False,
                'error': 'No tiene permisos para editar este documento'
            })
        
        # Create form with submitted data and existing instance
        form = DocumentoForm(request.POST, request.FILES, instance=documento)
        
        if form.is_valid():
            # Save the updated document
            form.save()
            
            # Get updated documents grouped by category
            documentos_agrupados = _get_documentos_agrupados(documento.contraparte)
            
            # Render updated documents list
            documentos_html = render_to_string('contrapartes/documentos_list_partial.html', {
                'object': documento.contraparte,
                'documentos_por_categoria': documentos_agrupados,
            }, request=request)
            
            return JsonResponse({
                'success': True,
                'message': 'Documento actualizado exitosamente',
                'documentos_html': documentos_html,
                'documentos_count': documento.contraparte.documentos.filter(activo=True).count()
            })
        else:
            # Form has errors, return form with errors
            tipos_documento = TipoDocumento.objects.filter(activo=True).order_by('nombre')
            form_html = render_to_string('contrapartes/documento_form_modal.html', {
                'form': form,
                'contraparte': documento.contraparte,
                'tipos_documento': tipos_documento,
                'documento': documento,
            }, request=request)
            
            return JsonResponse({
                'success': False,
                'form_html': form_html,
                'errors': form.errors
            })
            
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': f'Error al actualizar el documento: {str(e)}'
        })


@login_required
@require_http_methods(["POST"])
def delete_document(request, documento_pk):
    """
    Delete a document via AJAX (soft delete by marking as inactive)
    
    Args:
        request: HTTP request object
        documento_pk: Primary key of the document to delete
        
    Returns:
        JsonResponse with success/error message and updated document list HTML
    """
    try:
        documento = get_object_or_404(Documento, pk=documento_pk)
        contraparte = documento.contraparte
        
        # Check if user can delete this document
        if documento.subido_por != request.user and not request.user.is_staff:
            return JsonResponse({
                'success': False,
                'error': 'No tiene permisos para eliminar este documento'
            })
        
        # Soft delete - mark as inactive
        documento.activo = False
        documento.save()
        
        # Get updated documents grouped by category
        documentos_agrupados = _get_documentos_agrupados(contraparte)
        
        # Render updated documents list
        documentos_html = render_to_string('contrapartes/documentos_list_partial.html', {
            'object': contraparte,
            'documentos_por_categoria': documentos_agrupados,
        }, request=request)
        
        return JsonResponse({
            'success': True,
            'message': 'Documento eliminado exitosamente',
            'documentos_html': documentos_html,
            'documentos_count': contraparte.documentos.filter(activo=True).count()
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': f'Error al eliminar el documento: {str(e)}'
        })


@login_required
@require_http_methods(["POST"])
def upload_progress(request, contraparte_pk):
    """
    Handle file upload progress and validation
    This can be used for real-time upload feedback
    
    Args:
        request: HTTP request object
        contraparte_pk: Primary key of the contraparte
        
    Returns:
        JsonResponse with upload status
    """
    try:
        contraparte = get_object_or_404(Contraparte, pk=contraparte_pk)
        
        if 'archivo' not in request.FILES:
            return JsonResponse({
                'success': False,
                'error': 'No se encontró ningún archivo'
            })
        
        archivo = request.FILES['archivo']
        
        # Basic file validation
        max_size = getattr(settings, 'MAX_UPLOAD_SIZE', 10 * 1024 * 1024)  # 10MB default
        allowed_extensions = ['pdf', 'doc', 'docx', 'xls', 'xlsx', 'txt', 'jpg', 'jpeg', 'png']
        
        # Check file size
        if archivo.size > max_size:
            return JsonResponse({
                'success': False,
                'error': f'El archivo es demasiado grande. Tamaño máximo: {max_size // (1024*1024)}MB'
            })
        
        # Check file extension
        file_extension = archivo.name.split('.')[-1].lower()
        if file_extension not in allowed_extensions:
            return JsonResponse({
                'success': False,
                'error': f'Tipo de archivo no permitido. Tipos permitidos: {", ".join(allowed_extensions)}'
            })
        
        return JsonResponse({
            'success': True,
            'message': 'Archivo válido',
            'file_name': archivo.name,
            'file_size': archivo.size,
            'file_type': file_extension
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': f'Error al validar el archivo: {str(e)}'
        })


def _get_documentos_agrupados(contraparte):
    """
    Helper function to group documents by category
    
    Args:
        contraparte: Contraparte instance
        
    Returns:
        dict: Documents grouped by category with display names
    """
    documentos_por_categoria = defaultdict(list)
    
    # Get active documents ordered by category and upload date
    for doc in contraparte.documentos.filter(activo=True).order_by('categoria', '-fecha_subida'):
        documentos_por_categoria[doc.categoria].append(doc)
    
    # Convert to regular dict and add category display names
    documentos_agrupados = {}
    for categoria_code, documentos in documentos_por_categoria.items():
        categoria_display = dict(Documento.CATEGORIA_CHOICES).get(categoria_code, categoria_code)
        documentos_agrupados[categoria_display] = {
            'codigo': categoria_code,
            'documentos': documentos
        }
    
    return documentos_agrupados


@login_required
@require_http_methods(["GET"])
def get_document_types(request):
    """
    Get all active document types (useful for dynamic form updates)
    
    Returns:
        JsonResponse with list of document types
    """
    try:
        tipos = TipoDocumento.objects.filter(activo=True).order_by('nombre')
        tipos_data = []
        
        for tipo in tipos:
            tipos_data.append({
                'id': tipo.id,
                'nombre': tipo.nombre,
                'codigo': tipo.codigo,
                'requiere_expiracion': tipo.requiere_expiracion,
                'descripcion': tipo.descripcion or ''
            })
        
        return JsonResponse({
            'success': True,
            'tipos': tipos_data
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': f'Error al obtener tipos de documento: {str(e)}'
        })
