from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Gasto
from .forms import GastoForm


def listar_gastos(request):
    """
    Muestra todos los gastos registrados.
    """
    gastos = Gasto.objects.all()

    total_gastos = sum(
        (gasto.monto for gasto in gastos),
        start=0
    )

    contexto = {
        'gastos': gastos,
        'total_gastos': total_gastos,
        'cantidad_gastos': gastos.count(),
    }

    return render(request, 'gastos/listar_gastos.html', contexto)


def registrar_gasto(request):
    """
    Permite registrar un nuevo gasto.
    """
    if request.method == 'POST':
        formulario = GastoForm(request.POST)

        if formulario.is_valid():
            formulario.save()
            messages.success(request, 'El gasto se registró correctamente.')
            return redirect('gastos:listar_gastos')
    else:
        formulario = GastoForm()

    return render(
        request,
        'gastos/registrar_gasto.html',
        {'formulario': formulario}
    )


def eliminar_gasto(request, gasto_id):
    """
    Elimina un gasto después de confirmar la acción.
    """
    gasto = get_object_or_404(Gasto, id=gasto_id)

    if request.method == 'POST':
        gasto.delete()
        messages.success(request, 'El gasto se eliminó correctamente.')
        return redirect('gastos:listar_gastos')

    return redirect('gastos:listar_gastos')
