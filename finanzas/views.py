
# Importamos las herramientas necesarias de Django.
from django.shortcuts import render
from django.db.models import Sum
from django.utils import timezone
from datetime import date

# Importamos los modelos de pagos y gastos.
from pagos.models import Pago
from gastos.models import Gasto


def panel_finanzas(request):
    """
    Muestra el resumen financiero de TELEGUEPI ISP.
    Calcula ingresos, egresos y balance.
    Permite filtrar los movimientos por fechas.
    """

    # Obtenemos la fecha actual.
    hoy = timezone.localdate()

    # Leemos las fechas enviadas desde el formulario.
    fecha_inicio = request.GET.get('fecha_inicio', '')
    fecha_fin = request.GET.get('fecha_fin', '')

    # Consultamos los pagos que realmente fueron pagados.
    ingresos = Pago.objects.filter(
        estado='pagado',
        fecha_pago__isnull=False
    ).select_related(
        'contrato',
        'contrato__cliente'
    )

    # Consultamos todos los gastos registrados.
    egresos = Gasto.objects.all()

    # Aplicamos el filtro de fecha inicial.
    if fecha_inicio:
        try:
            fecha_inicio = date.fromisoformat(fecha_inicio)
            ingresos = ingresos.filter(fecha_pago__gte=fecha_inicio)
            egresos = egresos.filter(fecha_gasto__gte=fecha_inicio)
        except ValueError:
            fecha_inicio = ''

    # Aplicamos el filtro de fecha final.
    if fecha_fin:
        try:
            fecha_fin = date.fromisoformat(fecha_fin)
            ingresos = ingresos.filter(fecha_pago__lte=fecha_fin)
            egresos = egresos.filter(fecha_gasto__lte=fecha_fin)
        except ValueError:
            fecha_fin = ''

    # Calculamos el total de ingresos.
    total_ingresos = ingresos.aggregate(
        total=Sum('valor')
    )['total'] or 0

    # Calculamos el total de egresos.
    total_egresos = egresos.aggregate(
        total=Sum('monto')
    )['total'] or 0

    # Calculamos el balance financiero.
    balance = total_ingresos - total_egresos

    # Preparamos los movimientos de ingresos.
    movimientos_ingresos = []

    for pago in ingresos:
        movimientos_ingresos.append({
            'tipo': 'Ingreso',
            'descripcion': (
                f'Pago de {pago.contrato.cliente}'
            ),
            'fecha': pago.fecha_pago,
            'monto': pago.valor,
        })

    # Preparamos los movimientos de egresos.
    movimientos_egresos = []

    for gasto in egresos:
        movimientos_egresos.append({
            'tipo': 'Egreso',
            'descripcion': gasto.descripcion,
            'fecha': gasto.fecha_gasto,
            'monto': gasto.monto,
        })

    # Unimos y ordenamos los movimientos por fecha.
    movimientos = sorted(
        movimientos_ingresos + movimientos_egresos,
        key=lambda movimiento: movimiento['fecha'],
        reverse=True
    )

    # Información que enviaremos a la plantilla.
    contexto = {
        'total_ingresos': total_ingresos,
        'total_egresos': total_egresos,
        'balance': balance,
        'cantidad_ingresos': ingresos.count(),
        'cantidad_egresos': egresos.count(),
        'movimientos': movimientos,
        'fecha_inicio': fecha_inicio,
        'fecha_fin': fecha_fin,
        'hoy': hoy,
    }

    return render(
        request,
        'finanzas/panel_finanzas.html',
        contexto
    )
