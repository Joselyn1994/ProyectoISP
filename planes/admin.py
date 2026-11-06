# Register your models here.

from django.contrib import admin
from .models import PlanInternet


@admin.register(PlanInternet)
class PlanInternetAdmin(admin.ModelAdmin):

    # Columnas que aparecerán en el administrador.
    list_display = (
        'nombre',
        'velocidad',
        'precio_mensual',
        'estado',
        'fecha_creacion',
    )

    # Filtros para organizar los planes.
    list_filter = ('estado',)

    # Permitir buscar planes por nombre y velocidad.
    search_fields = ('nombre', 'velocidad')

    # Ordenar por precio mensual.
    ordering = ('precio_mensual',)

