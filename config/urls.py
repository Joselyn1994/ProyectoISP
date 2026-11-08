
# Importamos el panel administrativo de Django.
from django.contrib import admin

# Importamos path e include para configurar las rutas.
from django.urls import path, include


# Definimos las rutas principales del proyecto.
urlpatterns = [

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
