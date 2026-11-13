
# Importamos path para definir las direcciones.
from django.urls import path

# Importamos las funciones del archivo views.
from . import views

# Nombre de la aplicación.
app_name = 'pagos'

# Direcciones del módulo de pagos.
urlpatterns = [

    # Página principal: listado de pagos.
    path(
        '',
        views.listar_pagos,
        name='listar_pagos'
    ),

    # Registrar una nueva mensualidad.
    path(
        'registrar/',
        views.registrar_pago,
        name='registrar_pago'
    ),

    # Marcar una mensualidad como pagada.
    path(
        'marcar-pagado/<int:pago_id>/',
        views.marcar_pagado,
        name='marcar_pagado'
    ),
]
