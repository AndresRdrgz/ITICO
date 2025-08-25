# ITICO

## 🛡️ Portal Interno de Contrapartes – App Pacífico (Cotizador Web)

### 📝 Descripción General

Este proyecto tiene como objetivo desarrollar un portal web interno para la gestión de contrapartes en una empresa de reaseguros. La plataforma permitirá al Oficial de Cumplimiento crear y administrar perfiles de contrapartes, agregar miembros clave (CEO, accionistas, etc.), ejecutar procesos automatizados de debida diligencia mediante un sistema RPA (Makito) e interpretar los resultados con ayuda de un motor de inteligencia artificial, alertando sobre posibles riesgos reputacionales o financieros.

El sistema incluirá paneles de control, notificaciones, un calendario de seguimientos y análisis automatizados para facilitar la toma de decisiones por parte del analista o comité.

---

## 🎨 Paleta de Colores

La identidad visual del portal utiliza una paleta simple y profesional basada en los siguientes colores principales:

| Color      | Código HEX | Uso principal                |
|------------|:----------:|-----------------------------|
| Azul       | `#154F86`  | Color primario, encabezados, botones, enlaces destacados |
| Blanco     | `#FFFFFF`  | Fondo principal, textos y elementos secundarios           |

**Ejemplo de uso en CSS:**
```css
:root {
    --color-primario: #154F86;
    --color-blanco: #FFFFFF;
}
body {
    background: var(--color-blanco);
    color: var(--color-primario);
}
.btn-primario {
    background: var(--color-primario);
    color: var(--color-blanco);
}
```

Se recomienda mantener la interfaz limpia y consistente, priorizando el azul para elementos interactivos y el blanco para fondos y áreas de contenido.

---

## ⚙️ Requerimientos Funcionales

### Módulo de Contrapartes

- Creación de contrapartes con los siguientes campos:
        - Nombre
        - Nacionalidad
        - Tipo
        - Estado
- Visualización del perfil individual de cada contraparte.
- Gestión de miembros asociados a cada contraparte (CEO, accionistas, etc.).
- Filtro de búsqueda por nombre, tipo o estado.

### Gestión de Miembros

- Cada miembro debe incluir:
        - Nombre completo
        - Número de documento (cédula o pasaporte)
        - Fecha de nacimiento
        - Nacionalidad

### Proceso de Debida Diligencia Automatizada

- Botón **"Solicitar Debida Diligencia"** en el perfil de cada contraparte.
- Al hacer clic, se activa un trigger que envía los datos del miembro al RPA (Makito).
- El RPA realiza búsquedas (listas restrictivas, medios, fuentes públicas).
- Los resultados se cargan al sistema y se vinculan con el miembro correspondiente.
- Cada búsqueda puede tener estado: `completada`, `fallida`, `con coincidencias`, etc.

### Análisis con Inteligencia Artificial

- El sistema debe permitir cargar los documentos generados por Makito (PDF, HTML, etc.).
- Integración de un modelo de IA para analizar los documentos y detectar:
        - Palabras clave o patrones relacionados con fraude, lavado de activos, sanciones, etc.
        - Generación de un **resumen automatizado** para cada miembro.

### Panel del Oficial de Cumplimiento

- Notificaciones cuando las búsquedas estén listas.
- Revisión de hallazgos, marcado de falsos positivos y aprobación o rechazo de contrapartes.
- Comentarios por miembro y/o contraparte.
- Dashboard con filtros por estado:
        - Pendientes
        - En revisión
        - Procesadas
        - Completadas

### Calendario de Próximas Debidas Diligencias

- Cada contraparte tendrá una **fecha de próxima renovación de debida diligencia**.
- Visualización en un calendario global y alertas automatizadas.

---

## 🧱 Modelo de Datos

```plaintext
Contraparte
- id
- nombre
- nacionalidad
- tipo
- estado
- fecha_proxima_dd

Miembro
- id
- contraparte (FK)
- nombre
- documento_identidad
- fecha_nacimiento
- nacionalidad

DebidaDiligencia
- id
- miembro (FK)
- fecha_solicitud
- fecha_resultado
- resumen_ia
- estado (pendiente, en proceso, completada)
- comentarios_analista

Busqueda
- id
- debida_diligencia (FK)
- fuente
- resultado
- estado (exitosa, con error, coincidencia positiva)
- documento_adjunto (PDF/HTML)

Notificacion
- id
- usuario (FK)
- mensaje
- leida (boolean)
```

---

## 🧪 Requerimientos Técnicos

### Backend

- Framework: **Django 5+**
- Lenguaje: **Python 3.11+**
- Librerías sugeridas:
        - `Django REST Framework` para APIs
        - `Celery + Redis` para tareas asincrónicas (disparo al RPA y seguimiento)
        - `pdfminer.six` o `PyMuPDF` para extracción de texto de PDFs
        - `spaCy` o `transformers` para análisis de texto e IA

### Integraciones

- API HTTP para enviar solicitudes al RPA (Makito).
- Recepción de resultados de Makito vía endpoint o carga manual.
- Motor de análisis IA embebido en Django o como servicio externo vía REST API.

### Frontend

- Librerías: `HTMX`, `TailwindCSS` o `ReactJS` para interfaz dinámica.
- Dashboards y visualizaciones con `Chart.js` o `Plotly`.
- Calendario: Integración con `FullCalendar` o similar.

### Seguridad y Autenticación

- Autenticación basada en roles (`is_analyst`, `is_admin`)
- Registro de auditoría (acciones del oficial de cumplimiento)
- Protección de endpoints sensibles (CSRF, JWT para API externa si aplica)

---

## � Instalación y Despliegue

### Desarrollo Local

1. **Clona el repositorio:**
   ```bash
   git clone https://github.com/AndresRdrgz/ITICO.git
   cd ITICO
   ```

2. **Configura el entorno de desarrollo:**
   ```bash
   chmod +x setup_dev.sh
   ./setup_dev.sh
   ```

3. **Configura las variables de entorno:**
   ```bash
   cp .env.example .env
   # Edita el archivo .env con tus configuraciones
   ```

4. **Crea un superusuario:**
   ```bash
   python manage.py createsuperuser
   ```

5. **Ejecuta el servidor:**
   ```bash
   python manage.py runserver
   ```

### Despliegue en Producción (Render)

Este proyecto está configurado para desplegarse fácilmente en [Render](https://render.com) usando el archivo `render.yaml`.

1. **Conecta tu repositorio a Render**
2. **Crea un nuevo Blueprint** y selecciona este repositorio
3. **Configura las variables de entorno necesarias** (ver `DEPLOY.md` para detalles)
4. **Despliega automáticamente**

Para instrucciones detalladas de despliegue, consulta [`DEPLOY.md`](DEPLOY.md).

### Servicios Incluidos

- **Web App**: Aplicación Django principal
- **Worker**: Procesador de tareas Celery
- **Beat**: Programador de tareas periódicas
- **Redis**: Cola de mensajes
- **PostgreSQL**: Base de datos

---

## �📩 Flujo del Proceso

1. Gabriela crea la contraparte y sus miembros.
2. Solicita la debida diligencia.
3. El sistema envía los datos al RPA (Makito).
4. Makito realiza búsquedas y carga los resultados.
5. La IA analiza los documentos y genera un resumen.
6. Gabriela recibe una notificación.
7. Revisa resultados, deja comentarios y toma una decisión.
8. Si es necesario, eleva el caso al comité.
9. El comité aprueba o rechaza la contraparte.

---

## 📌 Próximos Pasos

- [ ] Configurar entorno Django (Andrés Rodríguez)
- [ ] Integrar portal al servidor web (Darío Osorio)
- [ ] Diseñar primer prototipo del módulo de contrapartes
- [ ] Investigar e integrar motor IA para análisis de texto
- [ ] Implementar lógica de notificaciones
- [ ] Construir calendario de seguimientos

