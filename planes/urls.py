
from django.urls import path
from . import views

app_name = 'planes'

urlpatterns = [

    # Página principal de planes.
    path('', views.listar_planes, name='listar_planes'),

    # Registrar un nuevo plan.
    path('registrar/', views.registrar_plan, name='registrar_plan'),

    # Editar un plan existente.
    path('editar/<int:plan_id>/', views.editar_plan, name='editar_plan'),

    # Activar o desactivar un plan.
    path(
        'cambiar-estado/<int:plan_id>/',
        views.cambiar_estado_plan,
        name='cambiar_estado_plan'
    ),
]
