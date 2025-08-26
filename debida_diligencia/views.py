"""
Vistas para debida diligencia - implementación básica temporal
"""
from django.views.generic import ListView, DetailView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.views import View


class DebidaDiligenciaListView(LoginRequiredMixin, ListView):
    template_name = 'debida_diligencia/lista.html'
    context_object_name = 'debidas_diligencias'
    
    def get_queryset(self):
        return []  # Temporal


class DebidaDiligenciaDetailView(LoginRequiredMixin, DetailView):
    template_name = 'debida_diligencia/detalle.html'


class SolicitarDDView(LoginRequiredMixin, TemplateView):
    template_name = 'debida_diligencia/solicitar.html'


class RevisarDDView(LoginRequiredMixin, TemplateView):
    template_name = 'debida_diligencia/revisar.html'


class AprobarDDView(LoginRequiredMixin, TemplateView):
    template_name = 'debida_diligencia/aprobar.html'


class RechazarDDView(LoginRequiredMixin, TemplateView):
    template_name = 'debida_diligencia/rechazar.html'


class BusquedaListView(LoginRequiredMixin, ListView):
    template_name = 'debida_diligencia/busquedas.html'
    context_object_name = 'busquedas'
    
    def get_queryset(self):
        return []


class BusquedaDetailView(LoginRequiredMixin, DetailView):
    template_name = 'debida_diligencia/busqueda_detalle.html'


class AnalisisIAView(LoginRequiredMixin, TemplateView):
    template_name = 'debida_diligencia/analisis_ia.html'


class CalendarioDDView(LoginRequiredMixin, TemplateView):
    template_name = 'debida_diligencia/calendario.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Import here to avoid circular imports
        from contrapartes.models import Contraparte, Documento
        from datetime import datetime, timedelta
        
        # Get all contrapartes with upcoming DD dates
        today = datetime.now().date()
        next_90_days = today + timedelta(days=90)
        
        upcoming_dd = Contraparte.objects.filter(
            fecha_proxima_dd__gte=today,
            fecha_proxima_dd__lte=next_90_days
        ).select_related('tipo', 'creado_por').order_by('fecha_proxima_dd')
        
        # Get documents with upcoming expiration dates
        upcoming_docs = Documento.objects.filter(
            fecha_expiracion__gte=today,
            fecha_expiracion__lte=next_90_days,
            activo=True
        ).select_related('contraparte', 'tipo', 'subido_por').order_by('fecha_expiracion')
        
        # Prepare events data for the calendar
        events = []
        
        # Add DD events
        for contraparte in upcoming_dd:
            days_until = (contraparte.fecha_proxima_dd - today).days
            priority = 'critical' if days_until <= 7 else 'high' if days_until <= 30 else 'medium'
            
            events.append({
                'id': f'dd_{contraparte.id}',
                'title': f'DD {contraparte.nombre}',
                'date': contraparte.fecha_proxima_dd.isoformat(),
                'type': 'dd',
                'priority': priority,
                'contraparte': contraparte.nombre,
                'contraparte_id': contraparte.id,
                'description': f'Renovación de debida diligencia para {contraparte.nombre}',
                'url': f'/contrapartes/{contraparte.id}/',
                'days_until': days_until
            })
        
        # Add document expiration events
        for documento in upcoming_docs:
            days_until = (documento.fecha_expiracion - today).days
            priority = 'critical' if days_until <= 7 else 'high' if days_until <= 30 else 'medium'
            
            events.append({
                'id': f'doc_{documento.id}',
                'title': f'{documento.nombre}',
                'date': documento.fecha_expiracion.isoformat(),
                'type': 'document',
                'priority': priority,
                'contraparte': documento.contraparte.nombre,
                'contraparte_id': documento.contraparte.id,
                'description': f'Expiración de documento: {documento.nombre}',
                'url': f'/contrapartes/{documento.contraparte.id}/',
                'days_until': days_until,
                'document_type': documento.tipo.nombre if documento.tipo else 'Sin tipo'
            })
        
        # Statistics
        stats = {
            'total_events': len(events),
            'critical_events': len([e for e in events if e['priority'] == 'critical']),
            'dd_events': len([e for e in events if e['type'] == 'dd']),
            'document_events': len([e for e in events if e['type'] == 'document']),
            'this_month': len([e for e in events if datetime.fromisoformat(e['date']).month == today.month]),
            'next_30_days': len([e for e in events if e['days_until'] <= 30]),
            'overdue': 0  # You can implement overdue logic here
        }
        
        context.update({
            'events': events,
            'stats': stats,
            'upcoming_dd': upcoming_dd,
            'upcoming_docs': upcoming_docs,
        })
        
        return context


class ReportesDDView(LoginRequiredMixin, TemplateView):
    template_name = 'debida_diligencia/reportes.html'


class MakitoWebhookView(View):
    def post(self, request, *args, **kwargs):
        return JsonResponse({'status': 'received'})


class RecibirResultadoView(View):
    def post(self, request, *args, **kwargs):
        return JsonResponse({'status': 'received'})
