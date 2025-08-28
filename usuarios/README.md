# Usuarios App - Gestión de Perfiles de Usuario

## Descripción

La aplicación `usuarios` proporciona funcionalidad completa para la gestión de perfiles de usuario en el sistema ITICO. Permite a los usuarios editar su información personal, subir fotos de perfil, cambiar contraseñas y ver su información de perfil.

## Características

### ✅ Funcionalidades Implementadas

- **Gestión de Perfiles de Usuario**
  - Modelo `UserProfile` que extiende el modelo `User` de Django
  - Campos adicionales: foto de perfil, teléfono, departamento, cargo, biografía
  - Creación automática de perfiles al registrar usuarios

- **Edición de Perfil**
  - Formulario completo para editar información personal y laboral
  - Subida de fotos de perfil con preview en tiempo real
  - Validación de archivos (tamaño máximo 5MB, formatos: JPG, PNG, GIF)
  - Eliminación de fotos de perfil

- **Cambio de Contraseña**
  - Formulario seguro para cambiar contraseña
  - Validación de contraseña actual
  - Validación en tiempo real de requisitos de contraseña
  - Confirmación de nueva contraseña

- **Visualización de Perfil**
  - Vista completa del perfil del usuario
  - Información personal, laboral y del sistema
  - Estadísticas de usuario
  - Diseño moderno y responsivo

- **Integración con el Sistema**
  - Menú de usuario actualizado con opciones de perfil
  - Navegación intuitiva entre secciones
  - Mensajes de éxito/error
  - Breadcrumbs para navegación

## Estructura del Proyecto

```
usuarios/
├── models.py              # Modelo UserProfile y señales
├── forms.py               # Formularios para edición y cambio de contraseña
├── views.py               # Vistas para todas las funcionalidades
├── urls.py                # Configuración de URLs
├── admin.py               # Configuración del admin de Django
├── tests.py               # Tests unitarios
├── management/
│   └── commands/
│       └── create_user_profiles.py  # Comando para crear perfiles existentes
└── templates/
    └── usuarios/
        ├── profile_edit.html        # Template de edición de perfil
        ├── change_password.html     # Template de cambio de contraseña
        └── profile_view.html        # Template de visualización de perfil
```

## Modelos

### UserProfile

Extiende el modelo `User` de Django con campos adicionales:

- `profile_picture`: ImagenField para foto de perfil
- `phone`: CharField para número de teléfono
- `department`: CharField para departamento
- `position`: CharField para cargo
- `created_at`: DateTimeField automático
- `updated_at`: DateTimeField automático

## URLs Disponibles

- `usuarios:profile_edit` - Editar perfil
- `usuarios:profile_view` - Ver perfil
- `usuarios:change_password` - Cambiar contraseña
- `usuarios:upload_profile_picture` - Subir foto (AJAX)
- `usuarios:delete_profile_picture` - Eliminar foto

## Formularios

### UserProfileForm
Formulario para editar información del perfil:
- Foto de perfil
- Teléfono
- Departamento
- Cargo

### UserForm
Formulario para editar información básica del usuario:
- Nombre
- Apellidos
- Email

### ChangePasswordForm
Formulario para cambiar contraseña:
- Contraseña actual
- Nueva contraseña
- Confirmar nueva contraseña

## Características de Seguridad

- **Autenticación requerida**: Todas las vistas requieren login
- **Validación de archivos**: Solo imágenes permitidas, tamaño máximo 5MB
- **Validación de contraseña**: Verificación de contraseña actual
- **CSRF Protection**: Todos los formularios incluyen protección CSRF
- **Validación de datos**: Validación tanto en frontend como backend

## Características de UX/UI

- **Diseño moderno**: Interfaz basada en Tailwind CSS
- **Responsive**: Funciona en dispositivos móviles y desktop
- **Animaciones suaves**: Transiciones y efectos visuales
- **Feedback visual**: Mensajes de éxito/error claros
- **Preview de imagen**: Vista previa de foto antes de subir
- **Validación en tiempo real**: Feedback inmediato en formularios

## Instalación y Configuración

1. **Agregar la app a INSTALLED_APPS**:
   ```python
   INSTALLED_APPS = [
       # ...
       'usuarios',
   ]
   ```

2. **Incluir las URLs**:
   ```python
   urlpatterns = [
       # ...
       path('usuarios/', include('usuarios.urls')),
   ]
   ```

3. **Ejecutar migraciones**:
   ```bash
   python manage.py makemigrations usuarios
   python manage.py migrate
   ```

4. **Crear perfiles para usuarios existentes**:
   ```bash
   python manage.py create_user_profiles
   ```

## Uso

### Para Usuarios

1. **Acceder al perfil**: Hacer clic en el menú de usuario en la barra lateral
2. **Editar perfil**: Seleccionar "Editar Perfil" para modificar información
3. **Subir foto**: Hacer clic en el ícono de cámara sobre la foto de perfil
4. **Cambiar contraseña**: Seleccionar "Cambiar Contraseña" desde el menú
5. **Ver perfil**: Seleccionar "Mi Perfil" para ver información completa

### Para Administradores

- Los perfiles de usuario se pueden gestionar desde el admin de Django
- El modelo `UserProfile` está integrado en el admin de `User`
- Se pueden ver y editar todos los campos del perfil

## Personalización

### Cambiar campos del perfil

Para agregar o modificar campos del perfil, edita el modelo `UserProfile` en `models.py`:

```python
class UserProfile(models.Model):
    # Agregar nuevos campos aquí
    new_field = models.CharField(max_length=100, blank=True)
```

### Personalizar formularios

Los formularios se pueden personalizar editando `forms.py`:

```python
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['profile_picture', 'phone', 'department', 'position', 'bio', 'new_field']
```

### Personalizar templates

Los templates están en `templates/usuarios/` y se pueden personalizar según las necesidades del proyecto.

## Testing

Ejecutar los tests:

```bash
python manage.py test usuarios
```

Los tests cubren:
- Creación automática de perfiles
- Métodos del modelo UserProfile
- Vistas con y sin autenticación
- Formularios y validaciones

## Dependencias

- Django 4.0+
- Pillow (para manejo de imágenes)
- Tailwind CSS (para estilos)

## Notas de Desarrollo

- La app utiliza señales de Django para crear perfiles automáticamente
- Las imágenes se almacenan en `media/usuarios/profile_pictures/`
- Se incluye un avatar por defecto en SVG
- Todos los formularios incluyen validación tanto en frontend como backend
