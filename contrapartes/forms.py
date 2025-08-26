"""
Formularios para la aplicación de contrapartes
"""
from django import forms
from .models import TipoContraparte, TipoDocumento, Contraparte, Miembro, Documento, Comentario


class TipoContraparteForm(forms.ModelForm):
    """Formulario para crear/editar tipos de contraparte"""
    
    class Meta:
        model = TipoContraparte
        fields = ['codigo', 'nombre', 'descripcion', 'activo']
        widgets = {
            'codigo': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-purple-500 focus:border-transparent transition-all duration-200',
                'placeholder': 'Ej: empresa, ong, persona_natural'
            }),
            'nombre': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-purple-500 focus:border-transparent transition-all duration-200',
                'placeholder': 'Ej: Empresa, ONG, Persona Natural'
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-purple-500 focus:border-transparent transition-all duration-200',
                'rows': 4,
                'placeholder': 'Descripción detallada del tipo de contraparte (opcional)'
            }),
            'activo': forms.CheckboxInput(attrs={
                'class': 'h-4 w-4 text-purple-600 focus:ring-purple-500 border-gray-300 rounded'
            })
        }


class ContraparteForm(forms.ModelForm):
    """Formulario para crear/editar contrapartes"""
    
    class Meta:
        model = Contraparte
        fields = ['nombre', 'nacionalidad', 'tipo', 'estado', 'descripcion']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200',
                'placeholder': 'Ingrese el nombre completo de la contraparte'
            }),
            'nacionalidad': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200',
                'placeholder': 'Ej: Colombia, Estados Unidos'
            }),
            'tipo': forms.Select(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200'
            }),
            'estado': forms.Select(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200'
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200',
                'rows': 4,
                'placeholder': 'Descripción adicional sobre la contraparte (opcional)'
            })
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Solo mostrar tipos activos
        self.fields['tipo'].queryset = TipoContraparte.objects.filter(activo=True)
        # Agregar opción vacía
        self.fields['tipo'].empty_label = "Seleccione un tipo"
        # Hacer campo requerido
        self.fields['tipo'].required = True


class MiembroForm(forms.ModelForm):
    """Formulario para crear/editar miembros"""
    
    class Meta:
        model = Miembro
        fields = ['tipo_persona', 'nombre', 'numero_identificacion', 'nacionalidad', 'fecha_nacimiento', 'categoria']
        widgets = {
            'fecha_nacimiento': forms.DateInput(attrs={
                'type': 'date',
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-purple-500 transition-colors duration-200'
            }),
            'tipo_persona': forms.Select(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-purple-500 transition-colors duration-200'
            }),
            'categoria': forms.Select(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-purple-500 transition-colors duration-200'
            }),
            'nombre': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-purple-500 transition-colors duration-200',
                'placeholder': 'Ingrese el nombre completo'
            }),
            'numero_identificacion': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-purple-500 transition-colors duration-200',
                'placeholder': 'Ej: 12345678'
            }),
            'nacionalidad': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-purple-500 transition-colors duration-200',
                'placeholder': 'Ej: Peruana, Colombiana'
            }),
        }


class DocumentoForm(forms.ModelForm):
    """Formulario para subir documentos"""
    
    class Meta:
        model = Documento
        fields = ['nombre', 'descripcion', 'tipo', 'archivo', 'fecha_emision', 'fecha_expiracion']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-colors duration-200',
                'placeholder': 'Nombre del documento'
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-colors duration-200',
                'rows': 3,
                'placeholder': 'Descripción del documento (opcional)'
            }),
            'tipo': forms.Select(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-colors duration-200'
            }),
            'archivo': forms.FileInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-colors duration-200'
            }),
            'fecha_emision': forms.DateInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-colors duration-200',
                'type': 'date'
            }),
            'fecha_expiracion': forms.DateInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-colors duration-200',
                'type': 'date'
            })
        }


class TipoDocumentoForm(forms.ModelForm):
    """Formulario para crear/editar tipos de documento"""
    
    class Meta:
        model = TipoDocumento
        fields = ['codigo', 'nombre', 'descripcion', 'requiere_expiracion', 'activo']
        widgets = {
            'codigo': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-purple-500 focus:border-transparent transition-all duration-200',
                'placeholder': 'Ej: cedula, pasaporte, certificado'
            }),
            'nombre': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-purple-500 focus:border-transparent transition-all duration-200',
                'placeholder': 'Ej: Cédula de Ciudadanía'
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-purple-500 focus:border-transparent transition-all duration-200',
                'rows': 3,
                'placeholder': 'Descripción del tipo de documento'
            }),
            'requiere_expiracion': forms.CheckboxInput(attrs={
                'class': 'w-5 h-5 text-purple-600 bg-gray-100 border-gray-300 rounded focus:ring-purple-500 focus:ring-2'
            }),
            'activo': forms.CheckboxInput(attrs={
                'class': 'w-5 h-5 text-purple-600 bg-gray-100 border-gray-300 rounded focus:ring-purple-500 focus:ring-2'
            })
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['requiere_expiracion'].help_text = 'Marque si este tipo de documento tiene fecha de expiración'
        self.fields['activo'].help_text = 'Desmarque para deshabilitar este tipo de documento'


class ComentarioForm(forms.ModelForm):
    """Formulario para crear/editar comentarios"""
    
    class Meta:
        model = Comentario
        fields = ['contenido']
        widgets = {
            'contenido': forms.Textarea(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200 resize-none',
                'rows': 3,
                'placeholder': 'Escriba su comentario aquí...'
            })
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['contenido'].label = ''
