
# Importamos el panel administrativo de Django.
from django.contrib import admin

# Importamos path e include para configurar las rutas.
from django.urls import path, include


from . import views

# Definimos las rutas principales del proyecto.
urlpatterns = [

# Página principal del sistema TELEGUEPI ISP.
# Página principal: ejecuta la vista dashboard,que consulta los datos reales de la base de datos
# y los envÃ­a a la plantilla del panel principal.
path('', views.dashboard, name='dashboard'),

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

     # Módulo de gastos.
    path('gastos/', include('gastos.urls')),

    # Módulo de finanzas.
    path('finanzas/', include('finanzas.urls')),

    # Módulo de reportes.
    path('reportes/', include('reportes.urls')),
]
