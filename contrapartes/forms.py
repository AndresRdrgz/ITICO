"""
Formularios para la aplicación de contrapartes
"""
from django import forms
from .models import (
    TipoContraparte, EstadoContraparte, TipoDocumento, Contraparte, Miembro, 
    Documento, Comentario, Calificacion, Calificador, Outlook, BalanceSheet, 
    BalanceSheetItem, Moneda, TipoCambio
)
from decimal import Decimal


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
        fields = ['tipo_persona', 'nombre', 'numero_identificacion', 'nacionalidad', 'fecha_nacimiento', 'categoria', 'es_pep', 'posicion_pep']
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
            'posicion_pep': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-red-500 focus:border-red-500 transition-colors duration-200 text-gray-900',
                'placeholder': 'Ej: Senador, Ministro, Alcalde, etc.'
            }),
        }
    
    def clean(self):
        cleaned_data = super().clean()
        es_pep = cleaned_data.get('es_pep')
        posicion_pep = cleaned_data.get('posicion_pep')
        
        if es_pep and not posicion_pep:
            self.add_error('posicion_pep', 'La posición como PEP es requerida cuando se marca como PEP.')
        
        return cleaned_data


class DocumentoForm(forms.ModelForm):
    """Formulario para subir documentos"""
    
    class Meta:
        model = Documento
        fields = ['descripcion', 'tipo', 'categoria', 'archivo', 'fecha_emision', 'fecha_expiracion']
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
            'categoria': forms.Select(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-colors duration-200 text-gray-900'
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
        # Make categoria field required
        self.fields['categoria'].required = True
    
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


class CargaDocumentoForm(forms.ModelForm):
    """Formulario para cargar documentos con selección de contraparte"""
    
    contraparte = forms.ModelChoiceField(
        queryset=Contraparte.objects.all(),
        widget=forms.Select(attrs={
            'class': 'w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200',
            'id': 'contraparte-select'
        }),
        empty_label="Seleccione una contraparte...",
        help_text="Seleccione la contraparte a la que pertenece el documento"
    )
    
    class Meta:
        model = Documento
        fields = ['contraparte', 'descripcion', 'tipo', 'categoria', 'archivo', 'fecha_emision', 'fecha_expiracion']
        widgets = {
            'descripcion': forms.Textarea(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200',
                'rows': 3,
                'placeholder': 'Descripción del documento (opcional)'
            }),
            'tipo': forms.Select(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200',
                'id': 'documento-tipo-select'
            }),
            'categoria': forms.Select(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200'
            }),
            'archivo': forms.FileInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200 file:mr-4 file:py-2 file:px-4 file:rounded-lg file:border-0 file:text-sm file:font-medium file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100',
                'accept': '.pdf,.doc,.docx,.xls,.xlsx,.txt,.jpg,.jpeg,.png'
            }),
            'fecha_emision': forms.DateInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200',
                'type': 'date'
            }),
            'fecha_expiracion': forms.DateInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200',
                'type': 'date'
            })
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make date fields not required by default
        self.fields['fecha_emision'].required = False
        self.fields['fecha_expiracion'].required = False
        # Make categoria field required
        self.fields['categoria'].required = True
        
        # Order contrapartes by name
        self.fields['contraparte'].queryset = Contraparte.objects.all().order_by('full_company_name', 'nombre')
    
    def clean(self):
        cleaned_data = super().clean()
        tipo = cleaned_data.get('tipo')
        fecha_emision = cleaned_data.get('fecha_emision')
        fecha_expiracion = cleaned_data.get('fecha_expiracion')
        archivo = cleaned_data.get('archivo')
        
        # Validate file size
        if archivo:
            # Maximum file size: 50MB
            max_size = 50 * 1024 * 1024  # 50MB in bytes
            if archivo.size > max_size:
                self.add_error('archivo', f'El archivo es demasiado grande. El tamaño máximo permitido es {max_size // (1024*1024)}MB.')
        
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
            'calificador', 'outlook', 'calificacion', 'tipo', 'fecha', 'documento_soporte'
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
            'tipo': forms.Select(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-colors duration-200 text-gray-900'
            }),
            'fecha': forms.DateInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-colors duration-200 text-gray-900',
                'type': 'date'
            }),
            'documento_soporte': forms.FileInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-colors duration-200 text-gray-900'
            })
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Personalizar labels
        self.fields['calificador'].label = 'Calificador *'


class MonedaForm(forms.ModelForm):
    """Formulario para crear/editar monedas"""
    
    class Meta:
        model = Moneda
        fields = ['codigo', 'nombre', 'simbolo', 'activo']
        widgets = {
            'codigo': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200',
                'placeholder': 'Ej: USD, EUR, COP',
                'maxlength': '3'
            }),
            'nombre': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200',
                'placeholder': 'Ej: Dólar estadounidense'
            }),
            'simbolo': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200',
                'placeholder': 'Ej: $, €, ¥'
            }),
            'activo': forms.CheckboxInput(attrs={
                'class': 'h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded'
            })
        }


class TipoCambioForm(forms.ModelForm):
    """Formulario para crear/editar tipos de cambio"""
    
    class Meta:
        model = TipoCambio
        fields = ['moneda', 'tasa_usd', 'fecha']
        widgets = {
            'moneda': forms.Select(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200'
            }),
            'tasa_usd': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200',
                'step': '0.000001',
                'placeholder': 'Ej: 0.00025 (cuántos USD equivale 1 unidad de la moneda)'
            }),
            'fecha': forms.DateInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200',
                'type': 'date'
            })
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['moneda'].queryset = Moneda.objects.filter(activo=True)


class BalanceSheetForm(forms.ModelForm):
    """Formulario para crear/editar balance sheets"""
    
    class Meta:
        model = BalanceSheet
        fields = ['año', 'solo_usd', 'moneda_local', 'tipo_cambio']
        widgets = {
            'año': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200',
                'min': '1900',
                'max': '2100',
                'placeholder': 'Ej: 2024'
            }),
            'solo_usd': forms.CheckboxInput(attrs={
                'class': 'h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded',
                'id': 'id_solo_usd'
            }),
            'moneda_local': forms.Select(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200',
                'id': 'id_moneda_local'
            }),
            'tipo_cambio': forms.Select(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200',
                'id': 'id_tipo_cambio'
            })
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['moneda_local'].queryset = Moneda.objects.filter(activo=True)
        self.fields['tipo_cambio'].queryset = TipoCambio.objects.none()
        
        # If we have a moneda_local selected, filter tipo_cambio by that currency
        if 'moneda_local' in self.data:
            try:
                moneda_id = int(self.data.get('moneda_local'))
                self.fields['tipo_cambio'].queryset = TipoCambio.objects.filter(moneda_id=moneda_id).order_by('-fecha')
            except (ValueError, TypeError):
                pass
        elif self.instance.pk and self.instance.moneda_local:
            self.fields['tipo_cambio'].queryset = TipoCambio.objects.filter(moneda=self.instance.moneda_local).order_by('-fecha')
    
    def clean(self):
        cleaned_data = super().clean()
        solo_usd = cleaned_data.get('solo_usd')
        moneda_local = cleaned_data.get('moneda_local')
        tipo_cambio = cleaned_data.get('tipo_cambio')
        
        if not solo_usd:
            if not moneda_local:
                raise forms.ValidationError("Si no es solo USD, debe seleccionar una moneda local.")
            if not tipo_cambio:
                raise forms.ValidationError("Si no es solo USD, debe seleccionar un tipo de cambio.")
        
        return cleaned_data


class BalanceSheetItemForm(forms.ModelForm):
    """Formulario para crear/editar items de balance sheet"""
    
    class Meta:
        model = BalanceSheetItem
        fields = ['descripcion', 'nota', 'categoria', 'monto_usd', 'monto_local', 'orden']
        widgets = {
            'descripcion': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-colors duration-200',
                'placeholder': 'Descripción del item'
            }),
            'nota': forms.Textarea(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-colors duration-200',
                'rows': 2,
                'placeholder': 'Notas adicionales (opcional)'
            }),
            'categoria': forms.Select(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-colors duration-200'
            }),
            'monto_usd': forms.NumberInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-colors duration-200',
                'step': '0.01',
                'placeholder': '0.00'
            }),
            'monto_local': forms.NumberInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-colors duration-200',
                'step': '0.01',
                'placeholder': '0.00 (opcional)'
            }),
            'orden': forms.NumberInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-colors duration-200',
                'placeholder': '0'
            })
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # If balance sheet is only USD, disable local currency field
        # Check if instance has a balance_sheet (for existing items) or if parent form has solo_usd (for new items)
        try:
            if self.instance and hasattr(self.instance, 'balance_sheet') and self.instance.balance_sheet and self.instance.balance_sheet.solo_usd:
                self.fields['monto_local'].widget.attrs['disabled'] = True
                self.fields['monto_local'].required = False
        except:
            # For new forms, we can't check the parent balance sheet here
            # This will be handled by JavaScript based on the solo_usd checkbox state
            pass
    
    def clean(self):
        cleaned_data = super().clean()
        monto_usd = cleaned_data.get('monto_usd')
        
        if monto_usd is None or monto_usd < 0:
            raise forms.ValidationError("El monto en USD debe ser mayor o igual a 0.")
        
        return cleaned_data


# Formset for Balance Sheet Items
BalanceSheetItemFormSet = forms.inlineformset_factory(
    BalanceSheet,
    BalanceSheetItem,
    form=BalanceSheetItemForm,
    extra=1,
    can_delete=True,
    fields=['descripcion', 'nota', 'categoria', 'monto_usd', 'monto_local', 'orden']
)
