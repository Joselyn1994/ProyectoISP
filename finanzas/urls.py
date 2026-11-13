
# Importamos path para definir las direcciones.
from django.urls import path

# Importamos las vistas de Finanzas.
from . import views

# Nombre de la aplicación.
app_name = 'finanzas'

# Direcciones del módulo Finanzas.
urlpatterns = [
    path(
        '',
        views.panel_finanzas,
        name='panel_finanzas'
    ),
]
