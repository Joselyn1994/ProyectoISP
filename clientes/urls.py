
# Importamos path para definir las direcciones web.
from django.urls import path

# Importamos las vistas de nuestra aplicación.
from . import views


# Definimos el espacio de nombres de la aplicación.
app_name = 'clientes'


# Definimos las rutas del módulo de clientes.
urlpatterns = [

    # Ruta para consultar y buscar clientes.
    path(
        '',
        views.listar_clientes,
        name='listar_clientes'
    ),

    # Ruta para registrar un nuevo cliente.
    path(
        'registrar/',
        views.registrar_cliente,
        name='registrar_cliente'
    ),

    # Ruta para consultar los cantones de una provincia.
    path(
        'ajax/cantones/',
        views.cargar_cantones,
        name='cargar_cantones'
    ),

    # Ruta para consultar las parroquias de un cantón.
    path(
        'ajax/parroquias/',
        views.cargar_parroquias,
        name='cargar_parroquias'
    ),

]
