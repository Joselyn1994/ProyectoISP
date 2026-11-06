
# Importamos path para definir las direcciones.
from django.urls import path

# Importamos las funciones de views.
from . import views


# Nombre de la aplicación.
app_name = 'contratos'


# Direcciones del módulo de contratos.
urlpatterns = [

    # Página principal: listado de contratos.
    path(
        '',
        views.listar_contratos,
        name='listar_contratos'
    ),

    # Registrar un contrato.
    path(
        'registrar/',
        views.registrar_contrato,
        name='registrar_contrato'
    ),

    # Editar un contrato.
    path(
        'editar/<int:contrato_id>/',
        views.editar_contrato,
        name='editar_contrato'
    ),

    # Cambiar el estado del contrato.
    path(
        'cambiar-estado/<int:contrato_id>/',
        views.cambiar_estado_contrato,
        name='cambiar_estado_contrato'
    ),

    # Buscar un cliente por su número de cédula.
    path(
        'buscar-cliente/',
        views.buscar_cliente,
        name='buscar_cliente'
    ),

    # Generar y descargar el contrato en PDF.
    path(
        'pdf/<int:contrato_id>/',
        views.generar_pdf_contrato,
        name='generar_pdf_contrato'
    ),
]



