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


class ReportesDDView(LoginRequiredMixin, TemplateView):
    template_name = 'debida_diligencia/reportes.html'


class MakitoWebhookView(View):
    def post(self, request, *args, **kwargs):
        return JsonResponse({'status': 'received'})


class RecibirResultadoView(View):
    def post(self, request, *args, **kwargs):
        return JsonResponse({'status': 'received'})
