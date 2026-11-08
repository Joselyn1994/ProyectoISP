
# Importamos el panel administrativo de Django.
from django.contrib import admin

# Importamos el modelo Pago.
from .models import Pago


# Registramos el modelo Pago en el administrador.
@admin.register(Pago)
class PagoAdmin(admin.ModelAdmin):

    # Columnas que aparecerán en el listado.
    list_display = (
        'contrato',
        'mes_referencia',
        'fecha_vencimiento',
        'valor',
        'estado',
        'metodo_pago',
    )

    # Filtros laterales.
    list_filter = (
        'estado',
        'metodo_pago',
        'mes_referencia',
    )

    # Campos para buscar pagos.
    search_fields = (
        'contrato__codigo',
        'contrato__cliente__cedula',
        'contrato__cliente__nombres',
        'contrato__cliente__apellidos',
    )

    # Orden de los registros.
    ordering = ('-mes_referencia',)
