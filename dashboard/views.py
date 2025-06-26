"""
Vistas del dashboard - implementación básica temporal
"""
from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/index.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Datos de ejemplo para el dashboard - estos vendrían de la base de datos
        context.update({
            'total_contrapartes': 45,
            'dd_pendientes': 12,
            'dd_completadas': 28,
            'dd_proximas': 5,
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
