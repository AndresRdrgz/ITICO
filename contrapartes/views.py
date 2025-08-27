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
from .models import TipoContraparte, EstadoContraparte, TipoDocumento, Contraparte, Miembro, Documento, Comentario
from .forms import TipoContraparteForm, EstadoContraparteForm, ContraparteForm, MiembroForm, DocumentoForm, ComentarioForm


# ====== VISTAS PARA TIPO CONTRAPARTE ======
class TipoContraparteListView(LoginRequiredMixin, ListView):
    model = TipoContraparte
    template_name = 'contrapartes/tipo_lista.html'
    context_object_name = 'tipos'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = TipoContraparte.objects.all()
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(codigo__icontains=search) | 
                Q(nombre__icontains=search) |
                Q(descripcion__icontains=search)
            )
        return queryset


class TipoContraparteCreateView(LoginRequiredMixin, CreateView):
    model = TipoContraparte
    form_class = TipoContraparteForm
    template_name = 'contrapartes/tipo_crear.html'
    success_url = reverse_lazy('contrapartes:tipo_lista')
    
    def form_valid(self, form):
        form.instance.creado_por = self.request.user
        return super().form_valid(form)


class TipoContraparteUpdateView(LoginRequiredMixin, UpdateView):
    model = TipoContraparte
    form_class = TipoContraparteForm
    template_name = 'contrapartes/tipo_editar.html'
    success_url = reverse_lazy('contrapartes:tipo_lista')


class TipoContraparteDeleteView(LoginRequiredMixin, DeleteView):
    model = TipoContraparte
    template_name = 'contrapartes/tipo_eliminar.html'
    success_url = reverse_lazy('contrapartes:tipo_lista')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['contrapartes_count'] = self.object.contrapartes.count()
        return context


# ====== VISTAS PARA ESTADO CONTRAPARTE ======
class EstadoContraparteListView(LoginRequiredMixin, ListView):
    model = EstadoContraparte
    template_name = 'contrapartes/estado_lista.html'
    context_object_name = 'estados'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = EstadoContraparte.objects.all()
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(codigo__icontains=search) | 
                Q(nombre__icontains=search) |
                Q(descripcion__icontains=search)
            )
        return queryset


class EstadoContraparteCreateView(LoginRequiredMixin, CreateView):
    model = EstadoContraparte
    form_class = EstadoContraparteForm
    template_name = 'contrapartes/estado_crear.html'
    success_url = reverse_lazy('contrapartes:estado_lista')
    
    def form_valid(self, form):
        form.instance.creado_por = self.request.user
        return super().form_valid(form)


class EstadoContraparteUpdateView(LoginRequiredMixin, UpdateView):
    model = EstadoContraparte
    form_class = EstadoContraparteForm
    template_name = 'contrapartes/estado_editar.html'
    success_url = reverse_lazy('contrapartes:estado_lista')


class EstadoContraparteDeleteView(LoginRequiredMixin, DeleteView):
    model = EstadoContraparte
    template_name = 'contrapartes/estado_eliminar.html'
    success_url = reverse_lazy('contrapartes:estado_lista')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['contrapartes_count'] = self.object.contrapartes.count()
        return context


# ====== VISTAS PARA TIPO DOCUMENTO ======
class TipoDocumentoListView(LoginRequiredMixin, ListView):
    model = TipoDocumento
    template_name = 'contrapartes/tipo_documento_lista.html'
    context_object_name = 'tipos'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = TipoDocumento.objects.all()
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(codigo__icontains=search) | 
                Q(nombre__icontains=search) |
                Q(descripcion__icontains=search)
            )
        return queryset


class TipoDocumentoCreateView(LoginRequiredMixin, CreateView):
    model = TipoDocumento
    template_name = 'contrapartes/tipo_documento_crear.html'
    fields = ['codigo', 'nombre', 'descripcion', 'requiere_expiracion', 'activo']
    success_url = reverse_lazy('contrapartes:tipo_documento_lista')
    
    def form_valid(self, form):
        form.instance.creado_por = self.request.user
        return super().form_valid(form)


class TipoDocumentoUpdateView(LoginRequiredMixin, UpdateView):
    model = TipoDocumento
    template_name = 'contrapartes/tipo_documento_editar.html'
    fields = ['codigo', 'nombre', 'descripcion', 'requiere_expiracion', 'activo']
    success_url = reverse_lazy('contrapartes:tipo_documento_lista')


class TipoDocumentoDeleteView(LoginRequiredMixin, DeleteView):
    model = TipoDocumento
    template_name = 'contrapartes/tipo_documento_eliminar.html'
    success_url = reverse_lazy('contrapartes:tipo_documento_lista')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['documentos_count'] = self.object.documentos.count()
        return context


# ====== VISTAS PARA CONTRAPARTES ======


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
        
        # Tipos de contraparte para filtros
        context['tipos_contraparte'] = TipoContraparte.objects.filter(activo=True).order_by('nombre')
        
        return context


class ContraparteDetailView(LoginRequiredMixin, DetailView):
    model = Contraparte
    template_name = 'contrapartes/detalle.html'


class ContraparteCreateView(LoginRequiredMixin, CreateView):
    model = Contraparte
    form_class = ContraparteForm
    template_name = 'contrapartes/crear.html'
    success_url = reverse_lazy('contrapartes:lista')
    
    def form_valid(self, form):
        form.instance.creado_por = self.request.user
        return super().form_valid(form)


class ContraparteUpdateView(LoginRequiredMixin, UpdateView):
    model = Contraparte
    form_class = ContraparteForm
    template_name = 'contrapartes/editar.html'
    success_url = reverse_lazy('contrapartes:lista')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add form to context so we can access form.tipo.field.queryset in template
        if 'form' not in context:
            context['form'] = self.get_form()
        return context


class ContraparteDeleteView(LoginRequiredMixin, DeleteView):
    model = Contraparte
    template_name = 'contrapartes/eliminar.html'
    success_url = reverse_lazy('contrapartes:lista')


class MiembroCreateView(LoginRequiredMixin, CreateView):
    model = Miembro
    form_class = MiembroForm
    template_name = 'contrapartes/miembro_crear.html'
    
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
    form_class = MiembroForm
    template_name = 'contrapartes/miembro_editar.html'
    
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


class DocumentoCreateAjaxView(LoginRequiredMixin, View):
    """Vista AJAX para subir documentos desde modal"""
    
    def get(self, request, contraparte_pk):
        """Devuelve el formulario en HTML para el modal"""
        contraparte = get_object_or_404(Contraparte, pk=contraparte_pk)
        
        form = DocumentoForm()
        form_html = render_to_string('contrapartes/documento_form_modal.html', {
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
        
        form = DocumentoForm(request.POST, request.FILES)
        
        if form.is_valid():
            documento = form.save(commit=False)
            documento.contraparte = contraparte
            documento.subido_por = request.user
            documento.save()
            
            # Render updated documents list
            documentos_html = render_to_string('contrapartes/documentos_list_partial.html', {
                'object': contraparte,
            }, request=request)
            
            return JsonResponse({
                'success': True,
                'message': 'Documento subido exitosamente',
                'documentos_html': documentos_html,
                'documentos_count': contraparte.documentos.filter(activo=True).count()
            })
        else:
            # Return form with errors
            form_html = render_to_string('contrapartes/documento_form_modal.html', {
                'form': form,
                'contraparte': contraparte,
            }, request=request)
            
            return JsonResponse({
                'success': False,
                'form_html': form_html,
                'errors': form.errors
            })


class DocumentoDeleteView(LoginRequiredMixin, View):
    """Vista AJAX para eliminar documentos"""
    
    def post(self, request, pk):
        documento = get_object_or_404(Documento, pk=pk)
        contraparte = documento.contraparte
        
        # Soft delete - mark as inactive
        documento.activo = False
        documento.save()
        
        # Render updated documents list
        documentos_html = render_to_string('contrapartes/documentos_list_partial.html', {
            'object': contraparte,
        }, request=request)
        
        return JsonResponse({
            'success': True,
            'message': 'Documento eliminado exitosamente',
            'documentos_html': documentos_html,
            'documentos_count': contraparte.documentos.filter(activo=True).count()
        })


class ContraparteBuscarView(LoginRequiredMixin, TemplateView):
    template_name = 'contrapartes/buscar.html'


class ExportarContrapartesView(LoginRequiredMixin, TemplateView):
    template_name = 'contrapartes/exportar.html'


class ComentarioCreateAjaxView(LoginRequiredMixin, View):
    """Vista AJAX para crear comentarios"""
    
    def post(self, request, contraparte_pk):
        contraparte = get_object_or_404(Contraparte, pk=contraparte_pk)
        
        form = ComentarioForm(request.POST)
        
        if form.is_valid():
            comentario = form.save(commit=False)
            comentario.contraparte = contraparte
            comentario.usuario = request.user
            comentario.save()
            
            # Render updated comments list
            comentarios_html = render_to_string('contrapartes/comentarios_list_partial.html', {
                'object': contraparte,
            }, request=request)
            
            return JsonResponse({
                'success': True,
                'message': 'Comentario agregado exitosamente',
                'comentarios_html': comentarios_html,
                'comentarios_count': contraparte.comentarios.filter(activo=True).count()
            })
        else:
            return JsonResponse({
                'success': False,
                'errors': form.errors
            })


class ComentarioUpdateAjaxView(LoginRequiredMixin, View):
    """Vista AJAX para editar comentarios"""
    
    def get(self, request, pk):
        comentario = get_object_or_404(Comentario, pk=pk)
        
        # Check if user can edit this comment
        if comentario.usuario != request.user and not request.user.is_staff:
            return JsonResponse({
                'success': False,
                'error': 'No tiene permisos para editar este comentario'
            })
        
        return JsonResponse({
            'success': True,
            'contenido': comentario.contenido
        })
    
    def post(self, request, pk):
        comentario = get_object_or_404(Comentario, pk=pk)
        
        # Check if user can edit this comment
        if comentario.usuario != request.user and not request.user.is_staff:
            return JsonResponse({
                'success': False,
                'error': 'No tiene permisos para editar este comentario'
            })
        
        form = ComentarioForm(request.POST, instance=comentario)
        
        if form.is_valid():
            form.save()
            
            # Render updated comments list
            comentarios_html = render_to_string('contrapartes/comentarios_list_partial.html', {
                'object': comentario.contraparte,
            }, request=request)
            
            return JsonResponse({
                'success': True,
                'message': 'Comentario actualizado exitosamente',
                'comentarios_html': comentarios_html
            })
        else:
            return JsonResponse({
                'success': False,
                'errors': form.errors
            })


class ComentarioDeleteAjaxView(LoginRequiredMixin, View):
    """Vista AJAX para eliminar comentarios"""
    
    def post(self, request, pk):
        comentario = get_object_or_404(Comentario, pk=pk)
        contraparte = comentario.contraparte
        
        # Soft delete - mark as inactive
        comentario.activo = False
        comentario.save()
        
        # Render updated comments list
        comentarios_html = render_to_string('contrapartes/comentarios_list_partial.html', {
            'object': contraparte,
        }, request=request)
        
        return JsonResponse({
            'success': True,
            'message': 'Comentario eliminado exitosamente',
            'comentarios_html': comentarios_html,
            'comentarios_count': contraparte.comentarios.filter(activo=True).count()
        })


class ContraparteFechaDDUpdateView(LoginRequiredMixin, View):
    """Vista AJAX para actualizar la fecha de debida diligencia"""
    
    def post(self, request, pk):
        from datetime import datetime
        
        contraparte = get_object_or_404(Contraparte, pk=pk)
        
        # Get the new date from request
        nueva_fecha = request.POST.get('fecha_proxima_dd')
        
        if not nueva_fecha:
            return JsonResponse({
                'success': False,
                'message': 'Fecha requerida'
            }, status=400)
        
        try:
            # Parse the date (format: YYYY-MM-DD)
            fecha_obj = datetime.strptime(nueva_fecha, '%Y-%m-%d').date()
            
            # Update the contraparte
            contraparte.fecha_proxima_dd = fecha_obj
            contraparte.save(update_fields=['fecha_proxima_dd', 'fecha_actualizacion'])
            
            # Calculate days until DD
            from datetime import date
            today = date.today()
            dias_hasta_dd = (fecha_obj - today).days
            
            # Determine status
            if dias_hasta_dd < 0:
                status_text = "Vencida"
                status_class = "danger"
                dias_text = f"Vencida hace {abs(dias_hasta_dd)} días"
            elif dias_hasta_dd == 0:
                status_text = "Vence hoy"
                status_class = "danger"
                dias_text = "Vence hoy"
            elif dias_hasta_dd <= 30:
                status_text = "Próxima a vencer"
                status_class = "warning"
                dias_text = f"Faltan {dias_hasta_dd} días"
            else:
                status_text = "Al día"
                status_class = "success"
                dias_text = f"Faltan {dias_hasta_dd} días"
            
            return JsonResponse({
                'success': True,
                'message': 'Fecha de debida diligencia actualizada exitosamente',
                'fecha_formatted': fecha_obj.strftime('%d/%m/%Y'),
                'dias_hasta_dd': dias_hasta_dd,
                'status_text': status_text,
                'status_class': status_class,
                'dias_text': dias_text
            })
            
        except ValueError:
            return JsonResponse({
                'success': False,
                'message': 'Formato de fecha inválido'
            }, status=400)
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': f'Error al actualizar fecha: {str(e)}'
            }, status=500)
        comentario = get_object_or_404(Comentario, pk=pk)
        
        # Check if user can delete this comment
        if comentario.usuario != request.user and not request.user.is_staff:
            return JsonResponse({
                'success': False,
                'error': 'No tiene permisos para eliminar este comentario'
            })
        
        contraparte = comentario.contraparte
        
        # Soft delete - mark as inactive
        comentario.activo = False
        comentario.save()
        
        # Render updated comments list
        comentarios_html = render_to_string('contrapartes/comentarios_list_partial.html', {
            'object': contraparte,
        }, request=request)
        
        return JsonResponse({
            'success': True,
            'message': 'Comentario eliminado exitosamente',
            'comentarios_html': comentarios_html,
            'comentarios_count': contraparte.comentarios.filter(activo=True).count()
        })
