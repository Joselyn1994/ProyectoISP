
from datetime import date

from django.db.models import Sum
from django.shortcuts import render
from django.utils import timezone

from clientes.models import Cliente
from contratos.models import Contrato
from pagos.models import Pago
from gastos.models import Gasto


def panel_reportes(request):
    hoy = timezone.localdate()

    # Recibimos las fechas seleccionadas en el formulario.
    fecha_inicio = request.GET.get('fecha_inicio', '')
    fecha_fin = request.GET.get('fecha_fin', '')

    # Validamos las fechas ingresadas.
    try:
        inicio = date.fromisoformat(fecha_inicio) if fecha_inicio else None
    except ValueError:
        inicio = None
        fecha_inicio = ''

    try:
        fin = date.fromisoformat(fecha_fin) if fecha_fin else None
    except ValueError:
        fin = None
        fecha_fin = ''

    # Consultamos los clientes.
    clientes = Cliente.objects.all().order_by('-fecha_registro')

    if inicio:
        clientes = clientes.filter(fecha_registro__date__gte=inicio)
    if fin:
        clientes = clientes.filter(fecha_registro__date__lte=fin)

    # Consultamos los contratos.
    contratos = Contrato.objects.select_related(
        'cliente', 'plan'
    ).order_by('-fecha_inicio')

    if inicio:
        contratos = contratos.filter(fecha_inicio__gte=inicio)
    if fin:
        contratos = contratos.filter(fecha_inicio__lte=fin)

    # Consultamos los pagos según su mes de referencia.
    pagos = Pago.objects.select_related(
        'contrato', 'contrato__cliente'
    ).order_by('-mes_referencia')

    if inicio:
        pagos = pagos.filter(mes_referencia__gte=inicio)
    if fin:
        pagos = pagos.filter(mes_referencia__lte=fin)

    # Consultamos los gastos.
    gastos = Gasto.objects.all().order_by('-fecha_gasto')

    if inicio:
        gastos = gastos.filter(fecha_gasto__gte=inicio)
    if fin:
        gastos = gastos.filter(fecha_gasto__lte=fin)

    # Calculamos los totales de clientes.
    total_clientes = clientes.count()
    clientes_activos = clientes.filter(estado='activo').count()
    clientes_inactivos = clientes.filter(estado='inactivo').count()

    # Calculamos los totales de contratos.
    total_contratos = contratos.count()
    contratos_activos = contratos.filter(estado='activo').count()
    contratos_suspendidos = contratos.filter(estado='suspendido').count()
    contratos_finalizados = contratos.filter(estado='finalizado').count()

    # Calculamos los valores de pagos.
    total_pagos = pagos.count()
    pagos_realizados = pagos.filter(estado='pagado')
    pagos_pendientes = pagos.filter(estado='pendiente')

    ingresos = pagos_realizados.aggregate(
        total=Sum('valor')
    )['total'] or 0

    valor_pendiente = pagos_pendientes.aggregate(
        total=Sum('valor')
    )['total'] or 0

    pagos_vencidos = pagos_pendientes.filter(
        fecha_vencimiento__lt=hoy
    ).count()

    # Calculamos los valores de gastos.
    total_gastos = gastos.count()

    egresos = gastos.aggregate(
        total=Sum('monto')
    )['total'] or 0

    # Calculamos el balance del periodo seleccionado.
    balance = ingresos - egresos

    contexto = {
        'fecha_inicio': fecha_inicio,
        'fecha_fin': fecha_fin,

        'total_clientes': total_clientes,
        'clientes_activos': clientes_activos,
        'clientes_inactivos': clientes_inactivos,

        'total_contratos': total_contratos,
        'contratos_activos': contratos_activos,
        'contratos_suspendidos': contratos_suspendidos,
        'contratos_finalizados': contratos_finalizados,

        'total_pagos': total_pagos,
        'pagos_realizados': pagos_realizados.count(),
        'cantidad_pendientes': pagos_pendientes.count(),
        'pagos_vencidos': pagos_vencidos,
        'ingresos': ingresos,
        'valor_pendiente': valor_pendiente,

        'total_gastos': total_gastos,
        'egresos': egresos,
        'balance': balance,

        # Mostramos los últimos diez registros de cada sección.
        'ultimos_clientes': clientes[:10],
        'ultimos_contratos': contratos[:10],
        'ultimos_pagos': pagos[:10],
        'ultimos_gastos': gastos[:10],
    }

    return render(request, 'reportes/panel_reportes.html', contexto)
