
# --------------------------------------------------
# IMPORTACIONES
# --------------------------------------------------

# Importamos path para definir las direcciones web.
from django.urls import path

# Importamos las vistas de nuestra aplicación.
from . import views


# --------------------------------------------------
# CONFIGURACIÓN DE LA APLICACIÓN
# --------------------------------------------------

# Definimos el espacio de nombres de la aplicación.
app_name = 'clientes'


# --------------------------------------------------
# RUTAS DEL MÓDULO DE CLIENTES
# --------------------------------------------------

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

    # Ruta para editar la información de un cliente.
    # Recibe el identificador del cliente en la dirección web.
    path(
        'editar/<int:cliente_id>/',
        views.editar_cliente,
        name='editar_cliente'
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

        # Ruta para activar o desactivar un cliente.
    path(
        'cambiar-estado/<int:cliente_id>/',
        views.cambiar_estado_cliente,
        name='cambiar_estado_cliente'
    ),

        # Ruta para activar o desactivar un cliente.
    path(
        'cambiar-estado/<int:cliente_id>/',
        views.cambiar_estado_cliente,
        name='cambiar_estado_cliente'
    ),

]
