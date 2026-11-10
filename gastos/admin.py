from django.contrib import admin
from .models import Gasto


@admin.register(Gasto)
class GastoAdmin(admin.ModelAdmin):

    # Columnas que se mostrarán en la lista de gastos.
    list_display = (
        'descripcion',
        'categoria',
        'monto',
        'fecha_gasto',
        'metodo_pago',
    )

    # Filtros para facilitar la búsqueda.
    list_filter = (
        'categoria',
        'metodo_pago',
        'fecha_gasto',
    )

    # Campos en los que se podrá buscar.
    search_fields = (
        'descripcion',
        'comprobante',
    )

    # Ordenar los gastos por fecha, del más reciente al más antiguo.
    ordering = ('-fecha_gasto',)
