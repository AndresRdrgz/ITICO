"""
Configuración del Django Admin para Contrapartes
"""
from django.contrib import admin
from django.utils.html import format_html
from .models import TipoContraparte, TipoDocumento, Contraparte, Miembro, Documento, Comentario


@admin.register(TipoContraparte)
class TipoContraparteAdmin(admin.ModelAdmin):
    list_display = [
        'codigo',
        'nombre', 
        'activo_badge',
        'contrapartes_count',
        'creado_por',
        'fecha_creacion'
    ]
    list_filter = [
        'activo',
        'fecha_creacion',
        'creado_por'
    ]
    search_fields = ['codigo', 'nombre', 'descripcion']
    ordering = ['nombre']
    readonly_fields = ['fecha_creacion', 'fecha_actualizacion']
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('codigo', 'nombre', 'descripcion', 'activo')
        }),
        ('Auditoría', {
            'fields': ('creado_por', 'fecha_creacion', 'fecha_actualizacion'),
            'classes': ('collapse',)
        }),
    )
    
    def activo_badge(self, obj):
        """Muestra el estado activo con colores"""
        if obj.activo:
            return format_html(
                '<span style="color: green; font-weight: bold;">✓ Activo</span>'
            )
        else:
            return format_html(
                '<span style="color: red; font-weight: bold;">✗ Inactivo</span>'
            )
    activo_badge.short_description = 'Estado'
    
    def contrapartes_count(self, obj):
        """Muestra el número de contrapartes de este tipo"""
        count = obj.contrapartes.count()
        return format_html(
            '<span style="font-weight: bold;">{} contrapartes</span>',
            count
        )
    contrapartes_count.short_description = 'Contrapartes'
    
    def save_model(self, request, obj, form, change):
        if not change:  # If creating new tipo
            obj.creado_por = request.user
        super().save_model(request, obj, form, change)


@admin.register(TipoDocumento)
class TipoDocumentoAdmin(admin.ModelAdmin):
    list_display = [
        'codigo',
        'nombre', 
        'requiere_expiracion_badge',
        'activo_badge',
        'documentos_count',
        'creado_por',
        'fecha_creacion'
    ]
    list_filter = [
        'activo',
        'requiere_expiracion',
        'fecha_creacion',
        'creado_por'
    ]
    search_fields = ['codigo', 'nombre', 'descripcion']
    ordering = ['nombre']
    readonly_fields = ['fecha_creacion', 'fecha_actualizacion']
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('codigo', 'nombre', 'descripcion', 'requiere_expiracion', 'activo')
        }),
        ('Auditoría', {
            'fields': ('creado_por', 'fecha_creacion', 'fecha_actualizacion'),
            'classes': ('collapse',)
        }),
    )
    
    def requiere_expiracion_badge(self, obj):
        """Muestra si requiere fecha de expiración"""
        if obj.requiere_expiracion:
            return format_html(
                '<span style="color: orange; font-weight: bold;">📅 Sí</span>'
            )
        else:
            return format_html(
                '<span style="color: gray; font-weight: bold;">⏳ No</span>'
            )
    requiere_expiracion_badge.short_description = 'Req. Expiración'
    
    def activo_badge(self, obj):
        """Muestra el estado activo con colores"""
        if obj.activo:
            return format_html(
                '<span style="color: green; font-weight: bold;">✓ Activo</span>'
            )
        else:
            return format_html(
                '<span style="color: red; font-weight: bold;">✗ Inactivo</span>'
            )
    activo_badge.short_description = 'Estado'
    
    def documentos_count(self, obj):
        """Muestra el número de documentos de este tipo"""
        count = obj.documentos.count()
        return format_html(
            '<span style="font-weight: bold;">{} documentos</span>',
            count
        )
    documentos_count.short_description = 'Documentos'
    
    def save_model(self, request, obj, form, change):
        if not change:  # If creating new tipo
            obj.creado_por = request.user
        super().save_model(request, obj, form, change)


@admin.register(Contraparte)
class ContraparteAdmin(admin.ModelAdmin):
    list_display = [
        'nombre', 
        'tipo', 
        'nacionalidad', 
        'estado_badge', 
        'fecha_proxima_dd',
        'creado_por',
        'fecha_creacion'
    ]
    list_filter = [
        'tipo', 
        'estado', 
        'nacionalidad', 
        'fecha_creacion',
        'fecha_proxima_dd'
    ]
    search_fields = ['nombre', 'descripcion', 'notas']
    ordering = ['-fecha_creacion']
    readonly_fields = ['fecha_creacion', 'fecha_actualizacion']
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('nombre', 'tipo', 'nacionalidad', 'estado')
        }),
        ('Debida Diligencia', {
            'fields': ('fecha_proxima_dd',)
        }),
        ('Información Adicional', {
            'fields': ('descripcion', 'notas'),
            'classes': ('collapse',)
        }),
        ('Auditoría', {
            'fields': ('creado_por', 'fecha_creacion', 'fecha_actualizacion'),
            'classes': ('collapse',)
        }),
    )
    
    def estado_badge(self, obj):
        """Muestra el estado con colores"""
        colors = {
            'activa': 'green',
            'inactiva': 'gray',
            'pendiente': 'orange',
            'rechazada': 'red',
            'en_revision': 'blue',
        }
        color = colors.get(obj.estado, 'gray')
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}</span>',
            color,
            obj.get_estado_display()
        )
    estado_badge.short_description = 'Estado'


class MiembroInline(admin.TabularInline):
    model = Miembro
    extra = 1
    fields = ['nombre', 'categoria', 'numero_identificacion', 'tipo_persona', 'nacionalidad', 'activo']
    readonly_fields = ['fecha_creacion']


# Agregar inline de miembros al admin de contrapartes
ContraparteAdmin.inlines = [MiembroInline]


@admin.register(Miembro)
class MiembroAdmin(admin.ModelAdmin):
    list_display = [
        'nombre',
        'contraparte',
        'categoria',
        'numero_identificacion',
        'tipo_persona',
        'nacionalidad',
        'edad_calculada',
        'activo'
    ]
    list_filter = [
        'categoria',
        'tipo_persona',
        'nacionalidad',
        'activo',
        'contraparte__tipo',
        'fecha_creacion'
    ]
    search_fields = [
        'nombre',
        'numero_identificacion',
        'contraparte__nombre'
    ]
    ordering = ['contraparte__nombre', 'nombre']
    readonly_fields = ['fecha_creacion', 'fecha_actualizacion']
    
    fieldsets = (
        ('Información Personal', {
            'fields': ('nombre', 'numero_identificacion', 'tipo_persona', 'fecha_nacimiento', 'nacionalidad')
        }),
        ('Organización', {
            'fields': ('contraparte', 'categoria', 'activo')
        }),
        ('Auditoría', {
            'fields': ('fecha_creacion', 'fecha_actualizacion'),
            'classes': ('collapse',)
        }),
    )
    
    def edad_calculada(self, obj):
        """Muestra la edad calculada"""
        return f"{obj.edad} años"
    edad_calculada.short_description = 'Edad'


@admin.register(Documento)
class DocumentoAdmin(admin.ModelAdmin):
    list_display = [
        'nombre',
        'contraparte', 
        'tipo',
        'fecha_emision',
        'fecha_expiracion',
        'estado_expiracion',
        'archivo',
        'tamaño_legible',
        'subido_por',
        'fecha_subida',
        'activo'
    ]
    list_filter = [
        'tipo',
        'activo',
        'fecha_subida',
        'fecha_emision',
        'fecha_expiracion',
        'subido_por'
    ]
    search_fields = ['nombre', 'descripcion', 'contraparte__nombre']
    ordering = ['-fecha_subida']
    readonly_fields = ['fecha_subida', 'fecha_actualizacion', 'tamaño_legible']
    
    fieldsets = (
        ('Información del Documento', {
            'fields': ('contraparte', 'nombre', 'tipo', 'descripcion')
        }),
        ('Fechas', {
            'fields': ('fecha_emision', 'fecha_expiracion')
        }),
        ('Archivo', {
            'fields': ('archivo', 'tamaño_legible')
        }),
        ('Estado', {
            'fields': ('activo',)
        }),
        ('Auditoría', {
            'fields': ('subido_por', 'fecha_subida', 'fecha_actualizacion'),
            'classes': ('collapse',)
        }),
    )
    
    def estado_expiracion(self, obj):
        """Muestra el estado de expiración del documento"""
        if not obj.fecha_expiracion:
            return format_html(
                '<span style="color: gray;">Sin expiración</span>'
            )
        
        if obj.esta_vencido:
            return format_html(
                '<span style="color: red; font-weight: bold;">🔴 Vencido</span>'
            )
        elif obj.expira_pronto:
            dias = obj.dias_hasta_expiracion
            return format_html(
                '<span style="color: orange; font-weight: bold;">🟡 Expira en {} días</span>',
                dias
            )
        else:
            dias = obj.dias_hasta_expiracion
            return format_html(
                '<span style="color: green;">🟢 Válido ({} días)</span>',
                dias
            )
    estado_expiracion.short_description = 'Estado'
    
    def save_model(self, request, obj, form, change):
        if not change:  # If creating new document
            obj.subido_por = request.user
        super().save_model(request, obj, form, change)


@admin.register(Comentario)
class ComentarioAdmin(admin.ModelAdmin):
    list_display = [
        'contraparte',
        'usuario',
        'contenido_resumido',
        'editado_badge',
        'activo_badge',
        'fecha_creacion'
    ]
    list_filter = [
        'editado',
        'activo',
        'fecha_creacion',
        'usuario'
    ]
    search_fields = [
        'contraparte__nombre',
        'usuario__username',
        'usuario__first_name',
        'usuario__last_name',
        'contenido'
    ]
    ordering = ['-fecha_creacion']
    readonly_fields = ['fecha_creacion', 'fecha_actualizacion']
    
    fieldsets = (
        ('Información del Comentario', {
            'fields': ('contraparte', 'usuario', 'contenido')
        }),
        ('Estado', {
            'fields': ('editado', 'activo')
        }),
        ('Auditoría', {
            'fields': ('fecha_creacion', 'fecha_actualizacion'),
            'classes': ('collapse',)
        })
    )
    
    def contenido_resumido(self, obj):
        """Muestra una versión resumida del contenido"""
        if len(obj.contenido) > 100:
            return obj.contenido[:97] + '...'
        return obj.contenido
    contenido_resumido.short_description = 'Contenido'
    
    def editado_badge(self, obj):
        """Muestra badge si el comentario fue editado"""
        if obj.editado:
            return format_html(
                '<span style="background-color: orange; color: white; padding: 2px 6px; border-radius: 3px; font-size: 11px;">EDITADO</span>'
            )
        return format_html(
            '<span style="background-color: gray; color: white; padding: 2px 6px; border-radius: 3px; font-size: 11px;">ORIGINAL</span>'
        )
    editado_badge.short_description = 'Estado'
    
    def activo_badge(self, obj):
        """Muestra badge de estado activo/inactivo"""
        if obj.activo:
            return format_html(
                '<span style="background-color: green; color: white; padding: 2px 6px; border-radius: 3px; font-size: 11px;">ACTIVO</span>'
            )
        return format_html(
            '<span style="background-color: red; color: white; padding: 2px 6px; border-radius: 3px; font-size: 11px;">ELIMINADO</span>'
        )
    activo_badge.short_description = 'Estado'
    
    def save_model(self, request, obj, form, change):
        if not change:  # If creating new comment
            obj.usuario = request.user
        super().save_model(request, obj, form, change)
