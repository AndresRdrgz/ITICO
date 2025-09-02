# API Documentos Implementation Summary

## Overview
Created a new `apiDocumentos.py` file in the contrapartes app with function-based views to handle document operations in the detalle.html template. This provides a cleaner, more maintainable API for document management with proper AJAX support.

## Files Created/Modified

### 1. `/contrapartes/apiDocumentos.py` (NEW)
Function-based views for document operations:

#### Functions:
- **`load_document_form(request, contraparte_pk)`** - GET
  - Loads empty form for creating new documents
  - Returns form HTML via JSON

- **`save_document_form(request, contraparte_pk)`** - POST
  - Saves new documents with file upload
  - Validates form data and files
  - Returns success/error status and updated document list

- **`load_document_edit_form(request, documento_pk)`** - GET
  - Loads form with existing document data for editing
  - Checks user permissions
  - Returns pre-populated form HTML

- **`save_document_edit_form(request, documento_pk)`** - POST
  - Updates existing documents
  - Handles file replacement if new file uploaded
  - Validates form and permissions

- **`delete_document(request, documento_pk)`** - POST
  - Soft deletes documents (marks as inactive)
  - Checks user permissions
  - Returns updated document list

- **`upload_progress(request, contraparte_pk)`** - POST
  - Validates uploaded files (size, type)
  - Provides upload feedback
  - Returns file validation status

- **`get_document_types(request)`** - GET
  - Returns all active document types for dynamic forms
  - Useful for form updates

- **`_get_documentos_agrupados(contraparte)`** - Helper function
  - Groups documents by category for display
  - Used by multiple functions to maintain consistency

### 2. `/contrapartes/urls.py` (MODIFIED)
Added new URL patterns for the API:

```python
# API para documentos (new function-based views)
path('<int:contraparte_pk>/documentos/ajax/crear/', apiDocumentos.load_document_form, name='documento_crear_ajax'),
path('<int:contraparte_pk>/documentos/ajax/guardar/', apiDocumentos.save_document_form, name='documento_guardar_ajax'),
path('documentos/<int:documento_pk>/ajax/cargar/', apiDocumentos.load_document_edit_form, name='documento_cargar_editar_ajax'),
path('documentos/<int:documento_pk>/ajax/actualizar/', apiDocumentos.save_document_edit_form, name='documento_actualizar_ajax'),
path('documentos/<int:documento_pk>/ajax/eliminar/', apiDocumentos.delete_document, name='documento_eliminar_ajax'),
path('<int:contraparte_pk>/documentos/ajax/validar-archivo/', apiDocumentos.upload_progress, name='documento_validar_archivo'),
path('documentos/ajax/tipos/', apiDocumentos.get_document_types, name='documento_tipos_ajax'),
```

### 3. `/templates/contrapartes/detalle.html` (MODIFIED)
Added and updated JavaScript functions:

#### New Functions:
- **`loadDocumentForm()`** - Loads new document form via AJAX
- **`saveDocumentForm()`** - Handles both create and edit operations

#### Modified Functions:
- **`editarDocumento(documentoId)`** - Updated to use new API endpoint
- **`eliminarDocumento(documentoId)`** - Updated to use new API endpoint
- **Document button event listeners** - Reset modal state for new documents

## Key Features

### 1. Permission Handling
- Users can only edit/delete documents they uploaded
- Staff users can edit/delete any document
- Proper permission checks in all functions

### 2. Form Validation
- Server-side validation using Django forms
- File type and size validation
- Required field validation based on document type

### 3. File Upload Management
- Handles file uploads with proper path structure
- Validates file extensions and sizes
- Maintains original file organization

### 4. AJAX Integration
- All operations return JSON responses
- Proper error handling and user feedback
- Dynamic form updates without page reload

### 5. User Experience
- Loading indicators during operations
- Success/error notifications
- Form state management (create vs edit mode)
- Proper modal reset between operations

## API Endpoints

| Method | URL | Function | Purpose |
|--------|-----|----------|---------|
| GET | `/<contraparte_pk>/documentos/ajax/crear/` | `load_document_form` | Load new document form |
| POST | `/<contraparte_pk>/documentos/ajax/guardar/` | `save_document_form` | Save new document |
| GET | `/documentos/<documento_pk>/ajax/cargar/` | `load_document_edit_form` | Load edit form |
| POST | `/documentos/<documento_pk>/ajax/actualizar/` | `save_document_edit_form` | Update document |
| POST | `/documentos/<documento_pk>/ajax/eliminar/` | `delete_document` | Delete document |
| POST | `/<contraparte_pk>/documentos/ajax/validar-archivo/` | `upload_progress` | Validate file |
| GET | `/documentos/ajax/tipos/` | `get_document_types` | Get document types |

## Integration with Existing System

### Compatible Templates:
- Uses existing `documento_form_modal.html`
- Uses existing `documentos_list_partial.html`
- Maintains existing modal structure

### Compatible Models:
- Works with existing `Documento` model
- Uses existing `TipoDocumento` model
- Maintains existing `DocumentoForm`

### Legacy Support:
- Keeps existing class-based views for backward compatibility
- New function-based views work alongside existing ones
- No breaking changes to existing functionality

## Testing Recommendations

1. **Form Loading**: Test both new document and edit document form loading
2. **File Upload**: Test various file types and sizes
3. **Permissions**: Test with different user roles
4. **Error Handling**: Test form validation and server errors
5. **User Experience**: Test modal behavior and notifications

## Benefits of This Implementation

1. **Cleaner Code**: Function-based views are simpler and more focused
2. **Better Error Handling**: Comprehensive error messages and validation
3. **Improved UX**: Better feedback and form state management
4. **Maintainability**: Clearer separation of concerns
5. **Extensibility**: Easy to add new document operations
6. **Performance**: Efficient AJAX operations without page reloads

## Notes

- All functions include proper CSRF protection
- File uploads are handled securely with validation
- Database operations use soft deletes for better data integrity
- The API maintains consistency with existing code patterns
- All functions include comprehensive error handling and logging
