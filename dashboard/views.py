"""
Vistas del dashboard - implementación básica temporal
"""
from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from datetime import timedelta
from django.db.models import Count, Q
from contrapartes.models import Contraparte


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/index.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Obtener datos reales de la base de datos
        today = timezone.now().date()
        next_30_days = today + timedelta(days=30)
        
        # Total de contrapartes activas
        total_contrapartes = Contraparte.objects.count()
        
        # DD pendientes (contrapartes sin fecha de próxima DD o con fecha pasada)
        dd_pendientes = Contraparte.objects.filter(
            Q(fecha_proxima_dd__isnull=True) | Q(fecha_proxima_dd__lt=today)
        ).count()
        
        # DD completadas (contrapartes con fecha de próxima DD en el futuro)
        dd_completadas = Contraparte.objects.filter(
            fecha_proxima_dd__gte=today
        ).count()
        
        # DD próximas a vencer (en los próximos 30 días)
        dd_proximas = Contraparte.objects.filter(
            fecha_proxima_dd__gte=today,
            fecha_proxima_dd__lte=next_30_days
        ).count()
        
        context.update({
            'total_contrapartes': total_contrapartes,
            'dd_pendientes': dd_pendientes,
            'dd_completadas': dd_completadas,
            'dd_proximas': dd_proximas,
        })
        
        return context
    

class EstadisticasWidgetView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/widgets/estadisticas.html'


class DDPendientesWidgetView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/widgets/dd_pendientes.html'


class DDProximasWidgetView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/widgets/dd_proximas.html'


class ActividadRecienteWidgetView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/widgets/actividad.html'


class ReportesView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/reportes.html'


class ExportarReporteView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/exportar.html'
