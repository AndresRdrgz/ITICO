"""
Vistas para contrapartes - implementación básica temporal
"""
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q, Count
from django.urls import reverse_lazy
from django.utils import timezone
from datetime import timedelta
from django.http import JsonResponse
from django.views import View
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from .models import Contraparte, Miembro


class ContraparteListView(LoginRequiredMixin, ListView):
    model = Contraparte
    template_name = 'contrapartes/lista.html'
    context_object_name = 'object_list'
    paginate_by = 20
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Estadísticas para los cards
        total = Contraparte.objects.count()
        activas = Contraparte.objects.filter(estado='activa').count()
        pendientes = Contraparte.objects.filter(estado='pendiente').count()
        
        # DD próximas a vencer (30 días)
        fecha_limite = timezone.now().date() + timedelta(days=30)
        dd_proximas = Contraparte.objects.filter(
            fecha_proxima_dd__lte=fecha_limite,
            fecha_proxima_dd__gte=timezone.now().date()
        ).count()
        
        context['stats'] = {
            'total': total,
            'activas': activas,
            'pendientes': pendientes,
            'dd_proximas': dd_proximas,
        }
        
        return context


class ContraparteDetailView(LoginRequiredMixin, DetailView):
    model = Contraparte
    template_name = 'contrapartes/detalle.html'


class ContraparteCreateView(LoginRequiredMixin, CreateView):
    model = Contraparte
    template_name = 'contrapartes/crear.html'
    fields = ['nombre', 'nacionalidad', 'tipo', 'estado', 'descripcion']
    success_url = reverse_lazy('contrapartes:lista')
    
    def form_valid(self, form):
        form.instance.creado_por = self.request.user
        return super().form_valid(form)


class ContraparteUpdateView(LoginRequiredMixin, UpdateView):
    model = Contraparte
    template_name = 'contrapartes/editar.html'
    fields = ['nombre', 'nacionalidad', 'tipo', 'estado', 'descripcion']
    success_url = reverse_lazy('contrapartes:lista')


class ContraparteDeleteView(LoginRequiredMixin, DeleteView):
    model = Contraparte
    template_name = 'contrapartes/eliminar.html'
    success_url = reverse_lazy('contrapartes:lista')


class MiembroCreateView(LoginRequiredMixin, CreateView):
    model = Miembro
    template_name = 'contrapartes/miembro_crear.html'
    fields = ['tipo_persona', 'nombre', 'numero_identificacion', 'nacionalidad', 'fecha_nacimiento', 'categoria']
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        contraparte_pk = self.kwargs.get('contraparte_pk')
        context['contraparte'] = Contraparte.objects.get(pk=contraparte_pk)
        context['contraparte_pk'] = contraparte_pk
        return context
    
    def form_valid(self, form):
        contraparte_pk = self.kwargs.get('contraparte_pk')
        form.instance.contraparte = Contraparte.objects.get(pk=contraparte_pk)
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('contrapartes:detalle', kwargs={'pk': self.kwargs.get('contraparte_pk')})


class MiembroDetailView(LoginRequiredMixin, DetailView):
    model = Miembro
    template_name = 'contrapartes/miembro_detalle.html'


class MiembroUpdateView(LoginRequiredMixin, UpdateView):
    model = Miembro
    template_name = 'contrapartes/miembro_editar.html'
    fields = ['tipo_persona', 'nombre', 'numero_identificacion', 'nacionalidad', 'fecha_nacimiento', 'categoria']
    
    def get_success_url(self):
        return reverse_lazy('contrapartes:detalle', kwargs={'pk': self.object.contraparte.pk})


class MiembroDeleteView(LoginRequiredMixin, DeleteView):
    model = Miembro
    template_name = 'contrapartes/miembro_eliminar.html'
    
    def get_success_url(self):
        return reverse_lazy('contrapartes:detalle', kwargs={'pk': self.object.contraparte.pk})


class MiembroCreateAjaxView(LoginRequiredMixin, View):
    """Vista AJAX para crear miembros desde modal"""
    
    def get(self, request, contraparte_pk):
        """Devuelve el formulario en HTML para el modal"""
        contraparte = get_object_or_404(Contraparte, pk=contraparte_pk)
        
        # Crear formulario vacío
        from django import forms
        
        class MiembroForm(forms.ModelForm):
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
        
        form = MiembroForm()
        form_html = render_to_string('contrapartes/miembro_form_modal.html', {
            'form': form,
            'contraparte': contraparte,
        }, request=request)
        
        return JsonResponse({
            'success': True,
            'form_html': form_html
        })
    
    def post(self, request, contraparte_pk):
        """Procesa el formulario enviado por AJAX"""
        contraparte = get_object_or_404(Contraparte, pk=contraparte_pk)
        
        from django import forms
        
        class MiembroForm(forms.ModelForm):
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
        
        form = MiembroForm(request.POST)
        
        if form.is_valid():
            miembro = form.save(commit=False)
            miembro.contraparte = contraparte
            miembro.save()
            
            # Render updated member list
            miembros_html = render_to_string('contrapartes/miembros_list_partial.html', {
                'object': contraparte,
            }, request=request)
            
            return JsonResponse({
                'success': True,
                'message': 'Miembro creado exitosamente',
                'miembros_html': miembros_html,
                'miembros_count': contraparte.miembros.count()
            })
        else:
            # Return form with errors
            form_html = render_to_string('contrapartes/miembro_form_modal.html', {
                'form': form,
                'contraparte': contraparte,
            }, request=request)
            
            return JsonResponse({
                'success': False,
                'form_html': form_html,
                'errors': form.errors
            })


class ContraparteBuscarView(LoginRequiredMixin, TemplateView):
    template_name = 'contrapartes/buscar.html'


class ExportarContrapartesView(LoginRequiredMixin, TemplateView):
    template_name = 'contrapartes/exportar.html'
