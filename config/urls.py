
# Importamos el panel administrativo de Django.
from django.contrib import admin

# Importamos path e include para configurar las rutas.
from django.urls import path, include


# Definimos las rutas principales del proyecto.
urlpatterns = [

    # Ruta para acceder al administrador de Django.
    path('admin/', admin.site.urls),

    # Conectamos las rutas de la aplicación clientes.
    path('clientes/', include('clientes.urls')),

]
