"""
Vistas para contrapartes - implementación básica temporal
"""
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.db.models import Q, Count
from django.urls import reverse_lazy, reverse
from django.utils import timezone
from datetime import timedelta
from django.http import JsonResponse
from django.views import View
from django.shortcuts import get_object_or_404, redirect
from django.template.loader import render_to_string
from .models import (
    TipoContraparte, EstadoContraparte, TipoDocumento, Contraparte, Miembro, 
    Documento, Comentario, Calificacion, Calificador, Outlook, BalanceSheet, 
    BalanceSheetItem, Moneda, TipoCambio
)
from .forms import (
    TipoContraparteForm, EstadoContraparteForm, ContraparteForm, MiembroForm, 
    DocumentoForm, ComentarioForm, CalificacionForm, CargaDocumentoForm, 
    BalanceSheetForm, BalanceSheetItemForm, BalanceSheetItemFormSet, MonedaForm, 
    TipoCambioForm
)


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
        activas = Contraparte.objects.filter(estado_nuevo__codigo='activa').count()
        pendientes = Contraparte.objects.filter(estado_nuevo__codigo='pendiente').count()
        
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
        
        # Estados de contraparte para filtros
        context['estados_contraparte'] = EstadoContraparte.objects.filter(activo=True).order_by('nombre')
        
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
        
        # Get tipos de documento with requiere_expiracion info for JavaScript
        tipos_documento = TipoDocumento.objects.filter(activo=True).order_by('nombre')
        
        form_html = render_to_string('contrapartes/documento_form_modal.html', {
            'form': form,
            'contraparte': contraparte,
            'tipos_documento': tipos_documento,
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
            tipos_documento = TipoDocumento.objects.filter(activo=True).order_by('nombre')
            form_html = render_to_string('contrapartes/documento_form_modal.html', {
                'form': form,
                'contraparte': contraparte,
                'tipos_documento': tipos_documento,
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


class DocumentoUpdateAjaxView(LoginRequiredMixin, View):
    """Vista AJAX para editar documentos"""
    
    def get(self, request, pk):
        documento = get_object_or_404(Documento, pk=pk)
        
        # Check if user can edit this document
        if documento.subido_por != request.user and not request.user.is_staff:
            return JsonResponse({
                'success': False,
                'error': 'No tiene permisos para editar este documento'
            })
        
        form = DocumentoForm(instance=documento)
        
        # Get tipos de documento with requiere_expiracion info for JavaScript
        tipos_documento = TipoDocumento.objects.filter(activo=True).order_by('nombre')
        
        form_html = render_to_string('contrapartes/documento_form_modal.html', {
            'form': form,
            'contraparte': documento.contraparte,
            'tipos_documento': tipos_documento,
            'documento': documento,
        }, request=request)
        
        return JsonResponse({
            'success': True,
            'form_html': form_html
        })
    
    def post(self, request, pk):
        documento = get_object_or_404(Documento, pk=pk)
        
        # Check if user can edit this document
        if documento.subido_por != request.user and not request.user.is_staff:
            return JsonResponse({
                'success': False,
                'error': 'No tiene permisos para editar este documento'
            })
        
        form = DocumentoForm(request.POST, request.FILES, instance=documento)
        
        if form.is_valid():
            form.save()
            
            # Render updated documents list
            documentos_html = render_to_string('contrapartes/documentos_list_partial.html', {
                'object': documento.contraparte,
            }, request=request)
            
            return JsonResponse({
                'success': True,
                'message': 'Documento actualizado exitosamente',
                'documentos_html': documentos_html,
                'documentos_count': documento.contraparte.documentos.filter(activo=True).count()
            })
        else:
            # Return form with errors
            tipos_documento = TipoDocumento.objects.filter(activo=True).order_by('nombre')
            form_html = render_to_string('contrapartes/documento_form_modal.html', {
                'form': form,
                'contraparte': documento.contraparte,
                'tipos_documento': tipos_documento,
                'documento': documento,
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


# ====== VISTAS PARA CALIFICACIONES ======

class CalificacionCreateAjaxView(LoginRequiredMixin, View):
    """Vista AJAX para crear calificaciones desde modal"""
    
    def get(self, request, contraparte_pk):
        """Devuelve el formulario en HTML para el modal"""
        contraparte = get_object_or_404(Contraparte, pk=contraparte_pk)
        
        form = CalificacionForm()
        form_html = render_to_string('contrapartes/calificacion_form_modal.html', {
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
        
        form = CalificacionForm(request.POST, request.FILES)
        
        if form.is_valid():
            calificacion = form.save(commit=False)
            calificacion.contraparte = contraparte
            calificacion.creado_por = request.user
            calificacion.save()
            
            # Render updated calificaciones list
            calificaciones_html = render_to_string('contrapartes/calificaciones_list_partial.html', {
                'object': contraparte,
            }, request=request)
            
            return JsonResponse({
                'success': True,
                'message': 'Calificación creada exitosamente',
                'calificaciones_html': calificaciones_html,
                'calificaciones_count': contraparte.calificaciones.filter(activo=True).count()
            })
        else:
            # Return form with errors
            form_html = render_to_string('contrapartes/calificacion_form_modal.html', {
                'form': form,
                'contraparte': contraparte,
            }, request=request)
            
            return JsonResponse({
                'success': False,
                'form_html': form_html,
                'errors': form.errors
            })


class CalificacionUpdateAjaxView(LoginRequiredMixin, View):
    """Vista AJAX para editar calificaciones"""
    
    def get(self, request, pk):
        calificacion = get_object_or_404(Calificacion, pk=pk)
        
        # Check if user can edit this certification
        if calificacion.creado_por != request.user and not request.user.is_staff:
            return JsonResponse({
                'success': False,
                'error': 'No tiene permisos para editar esta calificación'
            })
        
        form = CalificacionForm(instance=calificacion)
        form_html = render_to_string('contrapartes/calificacion_form_modal.html', {
            'form': form,
            'contraparte': calificacion.contraparte,
            'calificacion': calificacion,
        }, request=request)
        
        return JsonResponse({
            'success': True,
            'form_html': form_html
        })
    
    def post(self, request, pk):
        calificacion = get_object_or_404(Calificacion, pk=pk)
        
        # Check if user can edit this certification
        if calificacion.creado_por != request.user and not request.user.is_staff:
            return JsonResponse({
                'success': False,
                'error': 'No tiene permisos para editar esta calificación'
            })
        
        form = CalificacionForm(request.POST, request.FILES, instance=calificacion)
        
        if form.is_valid():
            form.save()
            
            # Render updated calificaciones list
            calificaciones_html = render_to_string('contrapartes/calificaciones_list_partial.html', {
                'object': calificacion.contraparte,
            }, request=request)
            
            return JsonResponse({
                'success': True,
                'message': 'Calificación actualizada exitosamente',
                'calificaciones_html': calificaciones_html
            })
        else:
            return JsonResponse({
                'success': False,
                'errors': form.errors
            })


class CalificacionDeleteAjaxView(LoginRequiredMixin, View):
    """Vista AJAX para eliminar calificaciones"""
    
    def post(self, request, pk):
        calificacion = get_object_or_404(Calificacion, pk=pk)
        
        # Check if user can delete this certification
        if calificacion.creado_por != request.user and not request.user.is_staff:
            return JsonResponse({
                'success': False,
                'error': 'No tiene permisos para eliminar esta calificación'
            })
        
        contraparte = calificacion.contraparte
        
        # Soft delete - mark as inactive
        calificacion.activo = False
        calificacion.save()
        
        # Render updated calificaciones list
        calificaciones_html = render_to_string('contrapartes/calificaciones_list_partial.html', {
            'object': contraparte,
        }, request=request)
        
        return JsonResponse({
            'success': True,
            'message': 'Calificación eliminada exitosamente',
            'calificaciones_html': calificaciones_html,
            'calificaciones_count': contraparte.calificaciones.filter(activo=True).count()
        })


# ====== VISTAS PARA CALIFICADORES ======

class CalificadorListView(LoginRequiredMixin, ListView):
    model = Calificador
    template_name = 'contrapartes/calificador_lista.html'
    context_object_name = 'calificadores'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = Calificador.objects.all()
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(nombre__icontains=search)
            )
        return queryset


class CalificadorCreateView(LoginRequiredMixin, CreateView):
    model = Calificador
    template_name = 'contrapartes/calificador_crear.html'
    fields = ['nombre', 'activo']
    success_url = reverse_lazy('contrapartes:calificador_lista')
    
    def form_valid(self, form):
        form.instance.creado_por = self.request.user
        return super().form_valid(form)


class CalificadorUpdateView(LoginRequiredMixin, UpdateView):
    model = Calificador
    template_name = 'contrapartes/calificador_editar.html'
    fields = ['nombre', 'activo']
    success_url = reverse_lazy('contrapartes:calificador_lista')


class CalificadorDeleteView(LoginRequiredMixin, DeleteView):
    model = Calificador
    template_name = 'contrapartes/calificador_eliminar.html'
    success_url = reverse_lazy('contrapartes:calificador_lista')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['calificaciones_count'] = self.object.calificaciones.count()
        return context


# ====== VISTAS PARA OUTLOOKS ======

class OutlookListView(LoginRequiredMixin, ListView):
    model = Outlook
    template_name = 'contrapartes/outlook_lista.html'
    context_object_name = 'outlooks'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = Outlook.objects.all()
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(outlook__icontains=search)
            )
        return queryset


class OutlookCreateView(LoginRequiredMixin, CreateView):
    model = Outlook
    template_name = 'contrapartes/outlook_crear.html'
    fields = ['outlook', 'activo']
    success_url = reverse_lazy('contrapartes:outlook_lista')
    
    def form_valid(self, form):
        form.instance.creado_por = self.request.user
        return super().form_valid(form)


class OutlookUpdateView(LoginRequiredMixin, UpdateView):
    model = Outlook
    template_name = 'contrapartes/outlook_editar.html'
    fields = ['outlook', 'activo']
    success_url = reverse_lazy('contrapartes:outlook_lista')


class OutlookDeleteView(LoginRequiredMixin, DeleteView):
    model = Outlook
    template_name = 'contrapartes/outlook_eliminar.html'
    success_url = reverse_lazy('contrapartes:outlook_lista')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['calificaciones_count'] = self.object.calificaciones.count()
        return context


# ====== VISTA PARA CARGA DE DOCUMENTOS ======

class CargaDocumentosView(LoginRequiredMixin, CreateView):
    """Vista para cargar documentos con selección de contraparte"""
    model = Documento
    form_class = CargaDocumentoForm
    template_name = 'contrapartes/carga_documentos.html'
    
    def get_success_url(self):
        # Redirect back to the upload page to allow more uploads
        return reverse_lazy('contrapartes:carga_documentos')
    
    def form_valid(self, form):
        try:
            form.instance.subido_por = self.request.user
            response = super().form_valid(form)
            
            # Add success message
            messages.success(
                self.request, 
                f'Documento "{self.object.tipo.nombre}" subido exitosamente para {self.object.contraparte.display_name}'
            )
            
            return response
        except Exception as e:
            # Handle any errors during file upload
            messages.error(
                self.request,
                f'Error al subir el documento: {str(e)}'
            )
            return self.form_invalid(form)
    
    def form_invalid(self, form):
        messages.error(
            self.request,
            'Hubo un error al procesar el formulario. Por favor, revise los datos e intente nuevamente.'
        )
        return super().form_invalid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Add statistics for the dashboard-like view
        context['stats'] = {
            'total_contrapartes': Contraparte.objects.count(),
            'total_documentos': Documento.objects.filter(activo=True).count(),
            'tipos_documento': TipoDocumento.objects.filter(activo=True).count(),
        }
        
        # Get recent uploads for display
        context['recent_uploads'] = Documento.objects.filter(
            activo=True
        ).select_related(
            'contraparte', 'tipo', 'subido_por'
        ).order_by('-fecha_subida')[:10]
        
        return context


# ====== VISTAS PARA BALANCE SHEETS ======

class BalanceSheetListView(LoginRequiredMixin, ListView):
    """Vista para listar los balance sheets de una contraparte"""
    model = BalanceSheet
    template_name = 'contrapartes/balance_sheet_lista.html'
    context_object_name = 'balance_sheets'
    paginate_by = 20
    
    def get_queryset(self):
        self.contraparte = get_object_or_404(Contraparte, pk=self.kwargs['contraparte_pk'])
        return BalanceSheet.objects.filter(
            contraparte=self.contraparte,
            activo=True
        ).order_by('-año')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['contraparte'] = self.contraparte
        return context


class BalanceSheetDetailView(LoginRequiredMixin, DetailView):
    """Vista para ver el detalle de un balance sheet"""
    model = BalanceSheet
    template_name = 'contrapartes/balance_sheet_detalle.html'
    context_object_name = 'balance_sheet'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Group items by category
        items_by_category = {}
        for item in self.object.items.filter(activo=True).order_by('categoria', 'orden', 'descripcion'):
            category = item.get_categoria_display()
            if category not in items_by_category:
                items_by_category[category] = []
            items_by_category[category].append(item)
        
        context['items_by_category'] = items_by_category
        context['contraparte'] = self.object.contraparte
        
        return context


class BalanceSheetCreateView(LoginRequiredMixin, CreateView):
    """Vista para crear un nuevo balance sheet"""
    model = BalanceSheet
    form_class = BalanceSheetForm
    template_name = 'contrapartes/balance_sheet_crear.html'
    
    def dispatch(self, request, *args, **kwargs):
        self.contraparte = get_object_or_404(Contraparte, pk=kwargs['contraparte_pk'])
        return super().dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
        form.instance.contraparte = self.contraparte
        form.instance.creado_por = self.request.user
        messages.success(
            self.request,
            f'Balance Sheet {form.instance.año} creado exitosamente para {self.contraparte.nombre or self.contraparte.full_company_name}'
        )
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse('contrapartes:balance_sheet_editar', kwargs={'pk': self.object.pk})
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['contraparte'] = self.contraparte
        return context


class BalanceSheetUpdateView(LoginRequiredMixin, UpdateView):
    """Vista para editar un balance sheet con sus items"""
    model = BalanceSheet
    form_class = BalanceSheetForm
    template_name = 'contrapartes/balance_sheet_editar.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['contraparte'] = self.object.contraparte
        
        if self.request.POST:
            context['formset'] = BalanceSheetItemFormSet(
                self.request.POST, 
                instance=self.object,
                prefix='form'
            )
        else:
            context['formset'] = BalanceSheetItemFormSet(
                instance=self.object,
                prefix='form'
            )
        
        return context
    
    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['formset']
        
        if formset.is_valid():
            response = super().form_valid(form)
            formset.instance = self.object
            formset.save()
            messages.success(
                self.request,
                f'Balance Sheet {self.object.año} actualizado exitosamente'
            )
            return response
        else:
            return self.form_invalid(form)
    
    def get_success_url(self):
        return reverse('contrapartes:balance_sheet_detalle', kwargs={'pk': self.object.pk})


class BalanceSheetDeleteView(LoginRequiredMixin, DeleteView):
    """Vista para eliminar un balance sheet"""
    model = BalanceSheet
    template_name = 'contrapartes/balance_sheet_eliminar.html'
    
    def get_success_url(self):
        return reverse('contrapartes:balance_sheet_lista', kwargs={'contraparte_pk': self.object.contraparte.pk})
    
    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.activo = False
        self.object.save()
        messages.success(
            request,
            f'Balance Sheet {self.object.año} eliminado exitosamente'
        )
        return redirect(self.get_success_url())


# ====== VISTAS AJAX PARA BALANCE SHEETS ======

class TipoCambioAjaxView(LoginRequiredMixin, View):
    """Vista AJAX para obtener tipos de cambio por moneda"""
    
    def get(self, request):
        moneda_id = request.GET.get('moneda_id')
        tipos_cambio = TipoCambio.objects.filter(moneda_id=moneda_id).order_by('-fecha')[:20]
        
        data = [{
            'id': tc.id,
            'tasa_usd': str(tc.tasa_usd),
            'fecha': tc.fecha.strftime('%Y-%m-%d'),
            'display': f"{tc.fecha.strftime('%Y-%m-%d')} - {tc.tasa_usd} USD"
        } for tc in tipos_cambio]
        
        return JsonResponse({'tipos_cambio': data})


# ====== VISTAS PARA MONEDAS ======

class MonedaListView(LoginRequiredMixin, ListView):
    """Vista para listar monedas"""
    model = Moneda
    template_name = 'contrapartes/moneda_lista.html'
    context_object_name = 'monedas'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = Moneda.objects.all()
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(codigo__icontains=search) | 
                Q(nombre__icontains=search)
            )
        return queryset


class MonedaCreateView(LoginRequiredMixin, CreateView):
    """Vista para crear una nueva moneda"""
    model = Moneda
    form_class = MonedaForm
    template_name = 'contrapartes/moneda_crear.html'
    success_url = reverse_lazy('contrapartes:moneda_lista')
    
    def form_valid(self, form):
        form.instance.creado_por = self.request.user
        messages.success(self.request, 'Moneda creada exitosamente')
        return super().form_valid(form)


class MonedaUpdateView(LoginRequiredMixin, UpdateView):
    """Vista para editar una moneda"""
    model = Moneda
    form_class = MonedaForm
    template_name = 'contrapartes/moneda_editar.html'
    success_url = reverse_lazy('contrapartes:moneda_lista')
    
    def form_valid(self, form):
        messages.success(self.request, 'Moneda actualizada exitosamente')
        return super().form_valid(form)


class MonedaDeleteView(LoginRequiredMixin, DeleteView):
    """Vista para eliminar una moneda"""
    model = Moneda
    template_name = 'contrapartes/moneda_eliminar.html'
    success_url = reverse_lazy('contrapartes:moneda_lista')
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Moneda eliminada exitosamente')
        return super().delete(request, *args, **kwargs)


# ====== VISTAS PARA TIPOS DE CAMBIO ======

class TipoCambioListView(LoginRequiredMixin, ListView):
    """Vista para listar tipos de cambio"""
    model = TipoCambio
    template_name = 'contrapartes/tipo_cambio_lista.html'
    context_object_name = 'tipos_cambio'
    paginate_by = 50
    
    def get_queryset(self):
        queryset = TipoCambio.objects.select_related('moneda').all()
        moneda = self.request.GET.get('moneda')
        if moneda:
            queryset = queryset.filter(moneda__codigo__icontains=moneda)
        return queryset.order_by('-fecha', 'moneda__codigo')


class TipoCambioCreateView(LoginRequiredMixin, CreateView):
    """Vista para crear un nuevo tipo de cambio"""
    model = TipoCambio
    form_class = TipoCambioForm
    template_name = 'contrapartes/tipo_cambio_crear.html'
    success_url = reverse_lazy('contrapartes:tipo_cambio_lista')
    
    def form_valid(self, form):
        form.instance.creado_por = self.request.user
        messages.success(self.request, 'Tipo de cambio creado exitosamente')
        return super().form_valid(form)


class TipoCambioUpdateView(LoginRequiredMixin, UpdateView):
    """Vista para editar un tipo de cambio"""
    model = TipoCambio
    form_class = TipoCambioForm
    template_name = 'contrapartes/tipo_cambio_editar.html'
    success_url = reverse_lazy('contrapartes:tipo_cambio_lista')
    
    def form_valid(self, form):
        messages.success(self.request, 'Tipo de cambio actualizado exitosamente')
        return super().form_valid(form)


class TipoCambioDeleteView(LoginRequiredMixin, DeleteView):
    """Vista para eliminar un tipo de cambio"""
    model = TipoCambio
    template_name = 'contrapartes/tipo_cambio_eliminar.html'
    success_url = reverse_lazy('contrapartes:tipo_cambio_lista')
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Tipo de cambio eliminado exitosamente')
        return super().delete(request, *args, **kwargs)
