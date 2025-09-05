# Documentación de Views.py - Aplicación Debida Diligencia

## Descripción General

El archivo `views.py` contiene las vistas para la gestión del proceso de debida diligencia, incluyendo vistas CRUD básicas, vistas de proceso de trabajo, funcionalidades especializadas como calendario y reportes, y endpoints API para integración con sistemas externos como RPA (Makito).

## Estructura de Vistas

### 1. Vistas CRUD Básicas

#### DebidaDiligenciaListView
```python
class DebidaDiligenciaListView(LoginRequiredMixin, ListView):
    template_name = 'debida_diligencia/lista.html'
    context_object_name = 'debidas_diligencias'
    
    def get_queryset(self):
        return []  # Temporal
```

**Funcionalidad**:
- **Lista paginada** de debidas diligencias
- **Filtrado** por estado, nivel de riesgo, fecha
- **Búsqueda** por miembro, contraparte, analista
- **Ordenamiento** por fecha de solicitud descendente

**Características Técnicas**:
- **LoginRequiredMixin**: Autenticación requerida
- **ListView**: Vista genérica para listas
- **Template**: `debida_diligencia/lista.html`
- **Context**: `debidas_diligencias` para el template

**Implementación Futura**:
```python
def get_queryset(self):
    queryset = DebidaDiligencia.objects.select_related(
        'miembro__contraparte', 'solicitado_por', 'aprobado_por'
    ).prefetch_related('busquedas', 'analisis_ia')
    
    # Filtros por parámetros GET
    estado = self.request.GET.get('estado')
    if estado:
        queryset = queryset.filter(estado=estado)
    
    nivel_riesgo = self.request.GET.get('nivel_riesgo')
    if nivel_riesgo:
        queryset = queryset.filter(nivel_riesgo=nivel_riesgo)
    
    return queryset
```

#### DebidaDiligenciaDetailView
```python
class DebidaDiligenciaDetailView(LoginRequiredMixin, DetailView):
    template_name = 'debida_diligencia/detalle.html'
```

**Funcionalidad**:
- **Vista detallada** de una debida diligencia específica
- **Información completa** del proceso y resultados
- **Búsquedas relacionadas** con resultados
- **Análisis de IA** generados
- **Historial de cambios** y auditoría

**Características Técnicas**:
- **DetailView**: Vista genérica para detalles
- **Template**: `debida_diligencia/detalle.html`
- **Context**: Objeto `debidadiligencia` automático

**Implementación Futura**:
```python
def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    dd = self.get_object()
    
    context.update({
        'busquedas': dd.busquedas.all().order_by('-fecha_busqueda'),
        'analisis_ia': dd.analisis_ia.all().order_by('-fecha_analisis'),
        'estadisticas': {
            'total_busquedas': dd.busquedas.count(),
            'coincidencias_positivas': dd.busquedas.filter(estado='coincidencia_positiva').count(),
            'duracion_dias': dd.duracion_proceso,
        }
    })
    return context
```

### 2. Vistas de Proceso de Trabajo

#### SolicitarDDView
```python
class SolicitarDDView(LoginRequiredMixin, TemplateView):
    template_name = 'debida_diligencia/solicitar.html'
```

**Funcionalidad**:
- **Formulario de solicitud** de nueva debida diligencia
- **Selección de miembro** para evaluar
- **Configuración de fuentes** de búsqueda
- **Inicio del proceso** automatizado
- **Integración con RPA** (Makito)

**Características Técnicas**:
- **TemplateView**: Vista para formularios complejos
- **Template**: `debida_diligencia/solicitar.html`
- **POST**: Procesamiento de solicitud

**Implementación Futura**:
```python
def post(self, request, miembro_pk):
    miembro = get_object_or_404(Miembro, pk=miembro_pk)
    
    # Crear nueva debida diligencia
    dd = DebidaDiligencia.objects.create(
        miembro=miembro,
        solicitado_por=request.user,
        estado='pendiente'
    )
    
    # Enviar solicitud a RPA (Makito)
    makito_request_id = enviar_solicitud_makito(dd)
    dd.makito_request_id = makito_request_id
    dd.estado = 'en_proceso'
    dd.save()
    
    return redirect('debida_diligencia:detalle', pk=dd.pk)
```

#### RevisarDDView
```python
class RevisarDDView(LoginRequiredMixin, TemplateView):
    template_name = 'debida_diligencia/revisar.html'
```

**Funcionalidad**:
- **Revisión de resultados** de debida diligencia completada
- **Análisis de coincidencias** encontradas
- **Evaluación de nivel de riesgo** por analista
- **Comentarios del analista** sobre resultados
- **Preparación para aprobación** o rechazo

**Características Técnicas**:
- **TemplateView**: Vista para formularios de revisión
- **Template**: `debida_diligencia/revisar.html`
- **POST**: Procesamiento de revisión

**Implementación Futura**:
```python
def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    dd = get_object_or_404(DebidaDiligencia, pk=self.kwargs['pk'])
    
    context.update({
        'debida_diligencia': dd,
        'busquedas_con_coincidencias': dd.busquedas.filter(
            estado='coincidencia_positiva'
        ),
        'resumen_ia': dd.resumen_ia,
        'nivel_riesgo_sugerido': dd.nivel_riesgo,
    })
    return context

def post(self, request, pk):
    dd = get_object_or_404(DebidaDiligencia, pk=pk)
    
    # Actualizar comentarios y nivel de riesgo
    dd.comentarios_analista = request.POST.get('comentarios_analista')
    dd.nivel_riesgo = request.POST.get('nivel_riesgo')
    dd.save()
    
    return redirect('debida_diligencia:detalle', pk=dd.pk)
```

#### AprobarDDView
```python
class AprobarDDView(LoginRequiredMixin, TemplateView):
    template_name = 'debida_diligencia/aprobar.html'
```

**Funcionalidad**:
- **Aprobación final** de debida diligencia
- **Confirmación de decisión** positiva
- **Registro de aprobación** con usuario y fecha
- **Notificaciones** a stakeholders
- **Actualización de estado** del miembro

**Características Técnicas**:
- **TemplateView**: Vista para confirmación de aprobación
- **Template**: `debida_diligencia/aprobar.html`
- **POST**: Procesamiento de aprobación

**Implementación Futura**:
```python
def post(self, request, pk):
    dd = get_object_or_404(DebidaDiligencia, pk=pk)
    
    # Aprobar debida diligencia
    dd.aprobado = True
    dd.aprobado_por = request.user
    dd.fecha_aprobacion = timezone.now()
    dd.save()
    
    # Notificar aprobación
    enviar_notificacion_aprobacion(dd)
    
    return redirect('debida_diligencia:detalle', pk=dd.pk)
```

#### RechazarDDView
```python
class RechazarDDView(LoginRequiredMixin, TemplateView):
    template_name = 'debida_diligencia/rechazar.html'
```

**Funcionalidad**:
- **Rechazo de debida diligencia** por riesgos detectados
- **Justificación del rechazo** con comentarios
- **Registro de decisión** negativa
- **Notificaciones** a stakeholders
- **Acciones correctivas** sugeridas

**Características Técnicas**:
- **TemplateView**: Vista para confirmación de rechazo
- **Template**: `debida_diligencia/rechazar.html`
- **POST**: Procesamiento de rechazo

**Implementación Futura**:
```python
def post(self, request, pk):
    dd = get_object_or_404(DebidaDiligencia, pk=pk)
    
    # Rechazar debida diligencia
    dd.aprobado = False
    dd.aprobado_por = request.user
    dd.fecha_aprobacion = timezone.now()
    dd.comentarios_analista = request.POST.get('justificacion_rechazo')
    dd.save()
    
    # Notificar rechazo
    enviar_notificacion_rechazo(dd)
    
    return redirect('debida_diligencia:detalle', pk=dd.pk)
```

### 3. Vistas de Análisis y Búsquedas

#### BusquedaListView
```python
class BusquedaListView(LoginRequiredMixin, ListView):
    template_name = 'debida_diligencia/busquedas.html'
    context_object_name = 'busquedas'
    
    def get_queryset(self):
        return []
```

**Funcionalidad**:
- **Lista de búsquedas** de una debida diligencia específica
- **Filtrado por fuente** y estado
- **Resultados detallados** de cada búsqueda
- **Documentos adjuntos** y URLs de fuentes
- **Estadísticas de coincidencias**

**Características Técnicas**:
- **ListView**: Vista genérica para listas
- **Template**: `debida_diligencia/busquedas.html`
- **Context**: `busquedas` para el template

**Implementación Futura**:
```python
def get_queryset(self):
    dd_pk = self.kwargs.get('pk')
    queryset = Busqueda.objects.filter(
        debida_diligencia_id=dd_pk
    ).order_by('-fecha_busqueda')
    
    # Filtros adicionales
    fuente = self.request.GET.get('fuente')
    if fuente:
        queryset = queryset.filter(fuente=fuente)
    
    estado = self.request.GET.get('estado')
    if estado:
        queryset = queryset.filter(estado=estado)
    
    return queryset
```

#### BusquedaDetailView
```python
class BusquedaDetailView(LoginRequiredMixin, DetailView):
    template_name = 'debida_diligencia/busqueda_detalle.html'
```

**Funcionalidad**:
- **Vista detallada** de una búsqueda específica
- **Resultados completos** de la búsqueda
- **Documento adjunto** si está disponible
- **URL de fuente** para verificación
- **Metadatos** de la búsqueda

**Características Técnicas**:
- **DetailView**: Vista genérica para detalles
- **Template**: `debida_diligencia/busqueda_detalle.html`
- **Context**: Objeto `busqueda` automático

#### AnalisisIAView
```python
class AnalisisIAView(LoginRequiredMixin, TemplateView):
    template_name = 'debida_diligencia/analisis_ia.html'
```

**Funcionalidad**:
- **Visualización de análisis** de IA generados
- **Resultados estructurados** en formato JSON
- **Niveles de confianza** de cada análisis
- **Palabras clave detectadas** automáticamente
- **Comparación de análisis** por tipo

**Características Técnicas**:
- **TemplateView**: Vista para visualización compleja
- **Template**: `debida_diligencia/analisis_ia.html`
- **JSON**: Procesamiento de datos estructurados

**Implementación Futura**:
```python
def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    dd_pk = self.kwargs.get('pk')
    
    analisis = AnalisisIA.objects.filter(
        debida_diligencia_id=dd_pk
    ).order_by('-fecha_analisis')
    
    context.update({
        'analisis': analisis,
        'tipos_analisis': AnalisisIA.TIPOS_ANALISIS,
        'estadisticas': {
            'total_analisis': analisis.count(),
            'confianza_promedio': analisis.aggregate(
                avg_confianza=models.Avg('confianza')
            )['avg_confianza'] or 0,
        }
    })
    return context
```

### 4. Vistas Especializadas

#### CalendarioDDView
```python
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
                'title': f'{documento.tipo.nombre}',
                'date': documento.fecha_expiracion.isoformat(),
                'type': 'document',
                'priority': priority,
                'contraparte': documento.contraparte.nombre,
                'contraparte_id': documento.contraparte.id,
                'description': f'Expiración de documento: {documento.tipo.nombre}',
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
```

**Funcionalidad**:
- **Vista de calendario** con fechas importantes
- **Eventos de debida diligencia** próximos a vencer
- **Expiración de documentos** con alertas
- **Estadísticas** de eventos por prioridad
- **Navegación** a detalles de contrapartes

**Características Técnicas**:
- **TemplateView**: Vista para calendario complejo
- **Template**: `debida_diligencia/calendario.html`
- **Context personalizado**: Eventos y estadísticas
- **Integración**: Con modelos de contrapartes y documentos

**Datos del Contexto**:
- **events**: Lista de eventos para el calendario
- **stats**: Estadísticas de eventos por tipo y prioridad
- **upcoming_dd**: Contrapartes con DD próximas
- **upcoming_docs**: Documentos próximos a expirar

#### ReportesDDView
```python
class ReportesDDView(LoginRequiredMixin, TemplateView):
    template_name = 'debida_diligencia/reportes.html'
```

**Funcionalidad**:
- **Reportes estadísticos** de debidas diligencias
- **Métricas de rendimiento** del proceso
- **Análisis de tendencias** por período
- **Distribución de riesgos** por nivel
- **Exportación** de reportes en múltiples formatos

**Características Técnicas**:
- **TemplateView**: Vista para reportes complejos
- **Template**: `debida_diligencia/reportes.html`
- **Context**: Estadísticas y métricas

**Implementación Futura**:
```python
def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    
    # Estadísticas generales
    total_dd = DebidaDiligencia.objects.count()
    dd_completadas = DebidaDiligencia.objects.filter(estado='completada').count()
    dd_aprobadas = DebidaDiligencia.objects.filter(aprobado=True).count()
    
    # Distribución por nivel de riesgo
    riesgo_distribution = DebidaDiligencia.objects.filter(
        nivel_riesgo__isnull=False
    ).values('nivel_riesgo').annotate(
        count=models.Count('id')
    ).order_by('nivel_riesgo')
    
    # Tiempo promedio de procesamiento
    tiempo_promedio = DebidaDiligencia.objects.filter(
        fecha_resultado__isnull=False
    ).aggregate(
        avg_dias=models.Avg(
            models.F('fecha_resultado') - models.F('fecha_solicitud')
        )
    )['avg_dias']
    
    context.update({
        'estadisticas_generales': {
            'total_dd': total_dd,
            'dd_completadas': dd_completadas,
            'dd_aprobadas': dd_aprobadas,
            'tasa_aprobacion': (dd_aprobadas / dd_completadas * 100) if dd_completadas > 0 else 0,
        },
        'distribucion_riesgo': riesgo_distribution,
        'tiempo_promedio_dias': tiempo_promedio.days if tiempo_promedio else 0,
    })
    return context
```

### 5. API Endpoints para Integración

#### MakitoWebhookView
```python
class MakitoWebhookView(View):
    def post(self, request, *args, **kwargs):
        return JsonResponse({'status': 'received'})
```

**Funcionalidad**:
- **Webhook** para recibir notificaciones de Makito
- **Actualización de estado** de debidas diligencias
- **Recepción de resultados** de búsquedas
- **Manejo de errores** y timeouts
- **Validación de datos** recibidos

**Características Técnicas**:
- **View**: Vista base para APIs
- **POST**: Método para recibir webhooks
- **JsonResponse**: Respuesta en formato JSON
- **Autenticación**: Validación de origen del webhook

**Implementación Futura**:
```python
def post(self, request, *args, **kwargs):
    try:
        # Validar autenticación del webhook
        if not validar_webhook_makito(request):
            return JsonResponse({'error': 'Unauthorized'}, status=401)
        
        data = json.loads(request.body)
        makito_request_id = data.get('request_id')
        
        # Buscar debida diligencia
        dd = DebidaDiligencia.objects.get(makito_request_id=makito_request_id)
        
        # Actualizar estado según resultado
        if data.get('status') == 'completed':
            dd.estado = 'completada'
            dd.fecha_resultado = timezone.now()
        elif data.get('status') == 'failed':
            dd.estado = 'fallida'
        
        dd.save()
        
        return JsonResponse({'status': 'success'})
        
    except DebidaDiligencia.DoesNotExist:
        return JsonResponse({'error': 'DD not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
```

#### RecibirResultadoView
```python
class RecibirResultadoView(View):
    def post(self, request, *args, **kwargs):
        return JsonResponse({'status': 'received'})
```

**Funcionalidad**:
- **Recepción de resultados** detallados de búsquedas
- **Creación de registros** de búsqueda
- **Procesamiento de documentos** adjuntos
- **Actualización de análisis** de IA
- **Notificaciones** a usuarios

**Características Técnicas**:
- **View**: Vista base para APIs
- **POST**: Método para recibir resultados
- **JsonResponse**: Respuesta en formato JSON
- **Procesamiento**: De datos complejos

**Implementación Futura**:
```python
def post(self, request, *args, **kwargs):
    try:
        dd_pk = self.kwargs.get('dd_pk')
        dd = get_object_or_404(DebidaDiligencia, pk=dd_pk)
        
        data = json.loads(request.body)
        
        # Crear registro de búsqueda
        busqueda = Busqueda.objects.create(
            debida_diligencia=dd,
            fuente=data.get('fuente'),
            estado=data.get('estado', 'exitosa'),
            resultado=data.get('resultado'),
            coincidencias_encontradas=data.get('coincidencias', 0),
            url_fuente=data.get('url_fuente')
        )
        
        # Procesar documento adjunto si existe
        if data.get('documento_url'):
            descargar_documento_adjunto(busqueda, data['documento_url'])
        
        # Generar análisis de IA si hay resultados
        if data.get('resultado'):
            generar_analisis_ia(dd, data['resultado'])
        
        return JsonResponse({'status': 'success', 'busqueda_id': busqueda.id})
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
```

## Patrones de Diseño Utilizados

### 1. Class-Based Views (CBV)
- **Reutilización**: Vistas genéricas para operaciones comunes
- **Herencia**: Mixins para funcionalidad compartida
- **Separación**: De responsabilidades por método

### 2. Template Method Pattern
- **Métodos especializados**: `get_context_data()`, `get_queryset()`
- **Personalización**: Comportamiento específico por vista
- **Consistencia**: Estructura común con variaciones

### 3. API Pattern
- **Endpoints REST**: Para integración externa
- **Webhooks**: Comunicación asíncrona
- **JSON**: Intercambio de datos estructurados

### 4. Observer Pattern
- **Notificaciones**: Automáticas por cambios de estado
- **Webhooks**: Para sistemas externos
- **Eventos**: De proceso para auditoría

## Consideraciones de Seguridad

### 1. Autenticación
- **LoginRequiredMixin**: En todas las vistas
- **Verificación de usuario**: Autenticado
- **Sesiones**: Manejo seguro de sesiones

### 2. Autorización
- **Permisos**: Por usuario y rol
- **Acceso a recursos**: Control granular
- **Validación**: De parámetros de URL

### 3. Validación de Datos
- **Webhooks**: Validación de origen
- **APIs**: Sanitización de entrada
- **Formularios**: Validación en cliente y servidor

### 4. Protección CSRF
- **Tokens**: En formularios
- **Verificación**: En vistas POST
- **Configuración**: Automática

## Consideraciones de Rendimiento

### 1. Optimización de Consultas
- **select_related**: Para ForeignKeys
- **prefetch_related**: Para relaciones inversas
- **Filtros**: Optimizados en querysets

### 2. Caché
- **Resultados**: De consultas frecuentes
- **Templates**: Caché de vistas estáticas
- **APIs**: Caché de respuestas

### 3. Procesamiento Asíncrono
- **Webhooks**: Procesamiento no bloqueante
- **APIs**: Respuestas rápidas
- **Background tasks**: Para operaciones pesadas

### 4. Paginación
- **Listas grandes**: Paginación automática
- **Navegación**: Eficiente
- **Carga**: Bajo demanda

## Manejo de Errores

### 1. Validación
- **Formularios**: Errores de campo específicos
- **APIs**: Códigos de estado HTTP apropiados
- **Webhooks**: Manejo de errores de integración

### 2. Excepciones
- **Base de datos**: Manejo de errores de DB
- **Integración**: Errores de sistemas externos
- **Logging**: Registro de errores críticos

### 3. Respuestas de Error
- **JSON**: Para APIs
- **HTML**: Para vistas web
- **Códigos**: HTTP apropiados

## Testing

### 1. Unit Tests
- **Vistas**: Tests de funcionalidad
- **Context**: Validación de contexto
- **APIs**: Tests de endpoints

### 2. Integration Tests
- **Flujos**: Procesos completos
- **Webhooks**: Integración con Makito
- **APIs**: Comunicación externa

### 3. Performance Tests
- **Consultas**: Optimización de queries
- **APIs**: Tiempo de respuesta
- **Carga**: Escalabilidad

## Mantenimiento

### 1. Documentación
- **Docstrings**: En métodos
- **Comentarios**: Explicaciones de lógica
- **APIs**: Documentación de endpoints

### 2. Logging
- **Operaciones**: Log de acciones importantes
- **Errores**: Registro de errores
- **Auditoría**: Seguimiento de cambios

### 3. Monitoreo
- **APIs**: Monitoreo de endpoints
- **Webhooks**: Estado de integraciones
- **Rendimiento**: Métricas de sistema
