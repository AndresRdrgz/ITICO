from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import UserProfile


class UserProfileInline(admin.StackedInline):
    """Inline para mostrar el perfil de usuario en el admin de User"""
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Perfil de Usuario'
    fk_name = 'user'


class UserAdmin(BaseUserAdmin):
    """Admin personalizado para el modelo User con perfil integrado"""
    inlines = (UserProfileInline,)
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'get_department')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    search_fields = ('username', 'first_name', 'last_name', 'email')
    ordering = ('username',)

    def get_department(self, obj):
        """Obtener el departamento del perfil del usuario"""
        if hasattr(obj, 'profile'):
            return obj.profile.department or '-'
        return '-'
    get_department.short_description = 'Departamento'

    def get_inline_instances(self, request, obj=None):
        """Mostrar inlines solo al editar"""
        if not obj:
            return list()
        return super().get_inline_instances(request, obj)


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    """Admin para el modelo UserProfile"""
    list_display = ('user', 'get_full_name', 'department', 'position', 'phone', 'created_at')
    list_filter = ('department', 'created_at')
    search_fields = ('user__username', 'user__first_name', 'user__last_name', 'user__email', 'department', 'position')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Información del Usuario', {
            'fields': ('user',)
        }),
        ('Información Personal', {
            'fields': ('profile_picture', 'phone')
        }),
        ('Información Laboral', {
            'fields': ('department', 'position')
        }),
        ('Información del Sistema', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def get_full_name(self, obj):
        """Obtener el nombre completo del usuario"""
        return obj.get_display_name()
    get_full_name.short_description = 'Nombre Completo'

    def get_queryset(self, request):
        """Optimizar consultas con select_related"""
        return super().get_queryset(request).select_related('user')


# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
