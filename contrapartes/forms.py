"""
Formularios para la aplicación de contrapartes
"""
from django import forms
from .models import TipoContraparte, EstadoContraparte, TipoDocumento, Contraparte, Miembro, Documento, Comentario, Calificacion, Calificador, Outlook


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


class EstadoContraparteForm(forms.ModelForm):
    """Formulario para crear/editar estados de contraparte"""
    
    class Meta:
        model = EstadoContraparte
        fields = ['codigo', 'nombre', 'descripcion', 'color', 'activo']
        widgets = {
            'codigo': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-purple-500 focus:border-transparent transition-all duration-200',
                'placeholder': 'Ej: activa, pendiente, rechazada'
            }),
            'nombre': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-purple-500 focus:border-transparent transition-all duration-200',
                'placeholder': 'Ej: Activa, Pendiente, Rechazada'
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-purple-500 focus:border-transparent transition-all duration-200',
                'rows': 4,
                'placeholder': 'Descripción detallada del estado de contraparte (opcional)'
            }),
            'color': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-purple-500 focus:border-transparent transition-all duration-200',
                'type': 'color',
                'placeholder': '#6B7280'
            }),
            'activo': forms.CheckboxInput(attrs={
                'class': 'h-4 w-4 text-purple-600 focus:ring-purple-500 border-gray-300 rounded'
            })
        }


class ContraparteForm(forms.ModelForm):
    """Formulario para crear/editar contrapartes"""
    
    class Meta:
        model = Contraparte
        fields = [
            'full_company_name', 'trading_name', 'company_website', 
            'home_regulatory_body', 'is_licensed_by_regulatory_body', 
            'is_publicly_listed', 'publicly_listed_country', 'is_holding_company',
            'external_auditors', 'registered_address', 'business_address',
            'contact_telephone', 'contact_email', 'company_nature_business',
            'domicile', 'company_incorporation_registration', 'date_incorporation',
            'number_of_employees', 'tipo', 'estado_nuevo', 'descripcion'
        ]
        widgets = {
            'full_company_name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200',
                'placeholder': 'Enter the complete legal name of the company'
            }),
            'trading_name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200',
                'placeholder': 'Trading or commercial name (if different)'
            }),
            'company_website': forms.URLInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200',
                'placeholder': 'https://www.company.com'
            }),
            'home_regulatory_body': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200',
                'placeholder': 'Regulatory authority name'
            }),
            'is_licensed_by_regulatory_body': forms.Select(choices=[(None, 'Select...'), (True, 'YES'), (False, 'NO')], attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200'
            }),
            'is_publicly_listed': forms.Select(choices=[(None, 'Select...'), (True, 'YES'), (False, 'NO')], attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200'
            }),
            'publicly_listed_country': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200',
                'placeholder': 'Country where publicly listed'
            }),
            'is_holding_company': forms.Select(choices=[(None, 'Select...'), (True, 'YES'), (False, 'NO')], attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200'
            }),
            'external_auditors': forms.Textarea(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200',
                'rows': 3,
                'placeholder': 'Name and address of external auditors'
            }),
            'registered_address': forms.Textarea(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200',
                'rows': 3,
                'placeholder': 'Complete registered address'
            }),
            'business_address': forms.Textarea(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200',
                'rows': 3,
                'placeholder': 'Primary business address'
            }),
            'contact_telephone': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200',
                'placeholder': '+1 (555) 123-4567'
            }),
            'contact_email': forms.EmailInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200',
                'placeholder': 'contact@company.com'
            }),
            'company_nature_business': forms.Textarea(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200',
                'rows': 4,
                'placeholder': 'Describe the nature and type of business'
            }),
            'domicile': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200',
                'placeholder': 'Legal domicile/jurisdiction'
            }),
            'company_incorporation_registration': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200',
                'placeholder': 'Registration/incorporation number'
            }),
            'date_incorporation': forms.DateInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200',
                'type': 'date'
            }),
            'number_of_employees': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200',
                'placeholder': 'Number of employees',
                'min': '0'
            }),
            'tipo': forms.Select(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200'
            }),
            'estado_nuevo': forms.Select(attrs={
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
        fields = ['tipo_persona', 'nombre', 'numero_identificacion', 'nacionalidad', 'fecha_nacimiento', 'categoria', 'es_pep']
        widgets = {
            'fecha_nacimiento': forms.DateInput(attrs={
                'type': 'date',
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-purple-500 transition-colors duration-200 text-gray-900'
            }),
            'tipo_persona': forms.Select(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-purple-500 transition-colors duration-200 text-gray-900'
            }),
            'categoria': forms.Select(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-purple-500 transition-colors duration-200 text-gray-900'
            }),
            'nombre': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-purple-500 transition-colors duration-200 text-gray-900',
                'placeholder': 'Ingrese el nombre completo'
            }),
            'numero_identificacion': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-purple-500 transition-colors duration-200 text-gray-900',
                'placeholder': 'Ej: 12345678'
            }),
            'nacionalidad': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-purple-500 transition-colors duration-200 text-gray-900',
                'placeholder': 'Ej: Peruana, Colombiana'
            }),
            'es_pep': forms.CheckboxInput(attrs={
                'class': 'h-4 w-4 text-red-600 focus:ring-red-500 border-gray-300 rounded'
            }),
        }


class DocumentoForm(forms.ModelForm):
    """Formulario para subir documentos"""
    
    class Meta:
        model = Documento
        fields = ['descripcion', 'tipo', 'archivo', 'fecha_emision', 'fecha_expiracion']
        widgets = {
            'descripcion': forms.Textarea(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-colors duration-200 text-gray-900',
                'rows': 3,
                'placeholder': 'Descripción del documento (opcional)'
            }),
            'tipo': forms.Select(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-colors duration-200 text-gray-900',
                'id': 'documento-tipo-select'
            }),
            'archivo': forms.FileInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-colors duration-200 text-gray-900'
            }),
            'fecha_emision': forms.DateInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-colors duration-200 text-gray-900',
                'type': 'date'
            }),
            'fecha_expiracion': forms.DateInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-colors duration-200 text-gray-900',
                'type': 'date'
            })
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make date fields not required by default
        self.fields['fecha_emision'].required = False
        self.fields['fecha_expiracion'].required = False
    
    def clean(self):
        cleaned_data = super().clean()
        tipo = cleaned_data.get('tipo')
        fecha_emision = cleaned_data.get('fecha_emision')
        fecha_expiracion = cleaned_data.get('fecha_expiracion')
        
        if tipo and tipo.requiere_expiracion:
            # If tipo requires dates, make them required
            if not fecha_emision:
                self.add_error('fecha_emision', 'La fecha de emisión es requerida para este tipo de documento.')
            
            if not fecha_expiracion:
                self.add_error('fecha_expiracion', 'La fecha de expiración es requerida para este tipo de documento.')
            
            # Validate that fecha_emision is before fecha_expiracion
            if fecha_emision and fecha_expiracion and fecha_emision >= fecha_expiracion:
                self.add_error('fecha_expiracion', 'La fecha de expiración debe ser posterior a la fecha de emisión.')
        
        return cleaned_data


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
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200 resize-none text-gray-900',
                'rows': 3,
                'placeholder': 'Escriba su comentario aquí...'
            })
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['contenido'].label = ''


class CalificacionForm(forms.ModelForm):
    """Formulario para crear/editar calificaciones"""
    
    class Meta:
        model = Calificacion
        fields = [
            'calificador', 'outlook', 'calificacion', 'fecha', 'documento_soporte'
        ]
        widgets = {
            'calificador': forms.Select(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-colors duration-200 text-gray-900'
            }),
            'outlook': forms.Select(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-colors duration-200 text-gray-900'
            }),
            'calificacion': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-colors duration-200 text-gray-900',
                'placeholder': 'Ej: AAA, AA, A, BBB, BB, B, CCC, CC, C, D, NR'
            }),
            'fecha': forms.DateTimeInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-colors duration-200 text-gray-900',
                'type': 'datetime-local'
            }),
            'documento_soporte': forms.FileInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-colors duration-200 text-gray-900'
            })
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Personalizar labels
        self.fields['calificador'].label = 'Calificador *'
        self.fields['outlook'].label = 'Outlook *'
        self.fields['calificacion'].label = 'Calificación *'
        self.fields['fecha'].label = 'Fecha *'
        self.fields['documento_soporte'].label = 'Documento de Soporte'
