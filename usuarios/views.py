from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ValidationError
from .models import UserProfile
from .forms import UserForm, UserProfileForm, ChangePasswordForm


@login_required
def profile_edit(request):
    """Vista para editar el perfil del usuario"""
    user = request.user
    
    # Obtener o crear el perfil del usuario
    profile, created = UserProfile.objects.get_or_create(user=user)
    
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=user)
        profile_form = UserProfileForm(request.POST, request.FILES, instance=profile)
        
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Perfil actualizado exitosamente.')
            return redirect('usuarios:profile_edit')
        else:
            messages.error(request, 'Por favor corrige los errores en el formulario.')
    else:
        user_form = UserForm(instance=user)
        profile_form = UserProfileForm(instance=profile)
    
    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'profile': profile,
        'active_tab': 'profile'
    }
    
    return render(request, 'usuarios/profile_edit.html', context)


@login_required
def change_password(request):
    """Vista para cambiar la contraseña"""
    if request.method == 'POST':
        form = ChangePasswordForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Contraseña cambiada exitosamente.')
            return redirect('usuarios:profile_edit')
        else:
            messages.error(request, 'Por favor corrige los errores en el formulario.')
    else:
        form = ChangePasswordForm(request.user)
    
    context = {
        'form': form,
        'active_tab': 'password'
    }
    
    return render(request, 'usuarios/change_password.html', context)


@login_required
def profile_view(request):
    """Vista para ver el perfil del usuario"""
    profile = get_object_or_404(UserProfile, user=request.user)
    
    context = {
        'profile': profile,
        'active_tab': 'view'
    }
    
    return render(request, 'usuarios/profile_view.html', context)


@login_required
@require_http_methods(["POST"])
@csrf_exempt
def upload_profile_picture(request):
    """Vista AJAX para subir foto de perfil"""
    try:
        profile = request.user.profile
        if 'profile_picture' in request.FILES:
            profile.profile_picture = request.FILES['profile_picture']
            profile.save()
            return JsonResponse({
                'success': True,
                'message': 'Foto de perfil actualizada exitosamente.',
                'image_url': profile.get_profile_picture_url()
            })
        else:
            return JsonResponse({
                'success': False,
                'message': 'No se encontró ninguna imagen.'
            })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Error al subir la imagen: {str(e)}'
        })


@login_required
def delete_profile_picture(request):
    """Vista para eliminar la foto de perfil"""
    if request.method == 'POST':
        profile = request.user.profile
        if profile.profile_picture:
            # Eliminar el archivo físico
            profile.profile_picture.delete(save=False)
            profile.profile_picture = None
            profile.save()
            messages.success(request, 'Foto de perfil eliminada exitosamente.')
        else:
            messages.warning(request, 'No tienes una foto de perfil para eliminar.')
    
    return redirect('usuarios:profile_edit')
