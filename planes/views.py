
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

from .models import PlanInternet
from .forms import PlanInternetForm


# --------------------------------------------------
# LISTAR PLANES DE INTERNET
# --------------------------------------------------

def listar_planes(request):

    planes = PlanInternet.objects.all()

    return render(request, 'planes/listar_planes.html', {
        'planes': planes,
        'titulo': 'Gestión de planes de Internet',
    })


# --------------------------------------------------
# REGISTRAR PLANES
# --------------------------------------------------

def registrar_plan(request):

    if request.method == 'POST':
        formulario = PlanInternetForm(request.POST)

        if formulario.is_valid():
            formulario.save()
            messages.success(
                request,
                'El plan de Internet se registró correctamente.'
            )
            return redirect('planes:listar_planes')

    else:
        formulario = PlanInternetForm()

    return render(request, 'planes/registrar_plan.html', {
        'formulario': formulario,
        'titulo': 'Registrar plan de Internet',
    })


# --------------------------------------------------
# EDITAR PLANES
# --------------------------------------------------

def editar_plan(request, plan_id):

    plan = get_object_or_404(PlanInternet, id=plan_id)

    if request.method == 'POST':
        formulario = PlanInternetForm(
            request.POST,
            instance=plan
        )

        if formulario.is_valid():
            formulario.save()
            messages.success(
                request,
                'El plan se actualizó correctamente.'
            )
            return redirect('planes:listar_planes')

    else:
        formulario = PlanInternetForm(instance=plan)

    return render(request, 'planes/registrar_plan.html', {
        'formulario': formulario,
        'plan': plan,
        'titulo': 'Editar plan de Internet',
    })


# --------------------------------------------------
# ACTIVAR Y DESACTIVAR PLANES
# --------------------------------------------------

def cambiar_estado_plan(request, plan_id):

    if request.method == 'POST':

        plan = get_object_or_404(PlanInternet, id=plan_id)

        if plan.estado == 'activo':
            plan.estado = 'inactivo'
            mensaje = 'El plan fue desactivado correctamente.'

        else:
            plan.estado = 'activo'
            mensaje = 'El plan fue activado correctamente.'

        plan.save(update_fields=['estado'])

        messages.success(request, mensaje)

    return redirect('planes:listar_planes')

