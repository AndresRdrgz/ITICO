"""
Configuración del Django Admin para Contrapartes
"""
from django.contrib import admin
from django.utils.html import format_html
from .models import Contraparte, Miembro, Documento, Documento


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
        'subido_por'
    ]
    search_fields = ['nombre', 'descripcion', 'contraparte__nombre']
    ordering = ['-fecha_subida']
    readonly_fields = ['fecha_subida', 'fecha_actualizacion', 'tamaño_legible']
    
    fieldsets = (
        ('Información del Documento', {
            'fields': ('contraparte', 'nombre', 'tipo', 'descripcion')
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
    
    def save_model(self, request, obj, form, change):
        if not change:  # If creating new document
            obj.subido_por = request.user
        super().save_model(request, obj, form, change)
