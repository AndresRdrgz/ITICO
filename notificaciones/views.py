"""
Vistas para notificaciones - implementación básica temporal
"""
from django.views.generic import ListView, DetailView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.views import View


class NotificacionListView(LoginRequiredMixin, ListView):
    template_name = 'notificaciones/lista.html'
    context_object_name = 'notificaciones'
    
    def get_queryset(self):
        return []


class NotificacionDetailView(LoginRequiredMixin, DetailView):
    template_name = 'notificaciones/detalle.html'


class MarcarLeidaView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        return JsonResponse({'status': 'marked_read'})


class MarcarTodasLeidasView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        return JsonResponse({'status': 'all_marked_read'})


class ConfiguracionNotificacionView(LoginRequiredMixin, TemplateView):
    template_name = 'notificaciones/configuracion.html'


class NotificacionesNoLeidasAPIView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        return JsonResponse({'unread': []})


class ContarNotificacionesAPIView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        return JsonResponse({'count': 0})
