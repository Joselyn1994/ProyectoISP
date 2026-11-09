
# Importamos el panel administrativo de Django.
from django.contrib import admin

# Importamos path e include para configurar las rutas.
from django.urls import path, include

# Importamos la función que mostrará el panel principal.
from django.views.generic import TemplateView

# Definimos las rutas principales del proyecto.
urlpatterns = [

    # Página principal del sistema TELEGUEPI ISP.
    path('', TemplateView.as_view(template_name='core/dashboard.html'), name='dashboard'),

    # Panel administrativo.
    path('admin/', admin.site.urls),

    # Módulo de clientes.
    path('clientes/', include('clientes.urls')),

    # Módulo de planes.
    path('planes/', include('planes.urls')),

    # Módulo de contratos.
    path('contratos/', include('contratos.urls')),

    # Módulo de pagos.
    path('pagos/', include('pagos.urls')),
]
