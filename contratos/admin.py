
# Importamos el administrador de Django.
from django.contrib import admin

# Importamos el modelo Contrato.
from .models import Contrato


@admin.register(Contrato)
class ContratoAdmin(admin.ModelAdmin):

    # Columnas que aparecerán en el administrador.
    list_display = (
        'codigo',
        'cliente',
        'plan',
        'fecha_inicio',
        'fecha_fin',
        'estado',
    )

    # Filtros para organizar los contratos.
    list_filter = (
        'estado',
        'fecha_inicio',
        'plan',
    )

    # Permitir buscar contratos por código y cliente.
    search_fields = (
        'codigo',
        'cliente__cedula',
        'cliente__nombres',
        'cliente__apellidos',
    )

    # Ordenar por fecha de creación.
    ordering = ('-fecha_creacion',)

