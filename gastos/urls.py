from django.urls import path
from . import views

app_name = 'gastos'

urlpatterns = [
    path('', views.listar_gastos, name='listar_gastos'),
    path('registrar/', views.registrar_gasto, name='registrar_gasto'),
    path('eliminar/<int:gasto_id>/', views.eliminar_gasto, name='eliminar_gasto'),
]
