
# Importamos las herramientas necesarias de Django.
from django.shortcuts import render
from django.db.models import Sum
from django.db.models.functions import TruncMonth
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
    Prepara los datos de la gráfica de los últimos 12 meses.
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

            ingresos = ingresos.filter(
                fecha_pago__gte=fecha_inicio
            )

            egresos = egresos.filter(
                fecha_gasto__gte=fecha_inicio
            )

        except ValueError:
            fecha_inicio = ''

    # Aplicamos el filtro de fecha final.
    if fecha_fin:
        try:
            fecha_fin = date.fromisoformat(fecha_fin)

            ingresos = ingresos.filter(
                fecha_pago__lte=fecha_fin
            )

            egresos = egresos.filter(
                fecha_gasto__lte=fecha_fin
            )

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
            'descripcion': f'Pago de {pago.contrato.cliente}',
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

    # -------------------------------------------------
    # DATOS PARA LA GRÁFICA DE LOS ÚLTIMOS 12 MESES
    # -------------------------------------------------

    # Nombres de los meses en español.
    nombres_meses = [
        'Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun',
        'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic'
    ]

    # Construimos los últimos 12 meses, incluyendo el actual.
    meses = []

    anio = hoy.year
    mes = hoy.month

    for _ in range(12):
        meses.append(date(anio, mes, 1))

        mes -= 1

        if mes == 0:
            mes = 12
            anio -= 1

    meses.reverse()

    # Fecha inicial del período de la gráfica.
    primer_mes = meses[0]

    # Consultamos los ingresos de los últimos 12 meses.
    ingresos_grafica = (
        Pago.objects.filter(
            estado='pagado',
            fecha_pago__isnull=False,
            fecha_pago__gte=primer_mes,
            fecha_pago__lte=hoy
        )
        .annotate(mes=TruncMonth('fecha_pago'))
        .values('mes')
        .annotate(total=Sum('valor'))
    )

    # Consultamos los egresos de los últimos 12 meses.
    egresos_grafica = (
        Gasto.objects.filter(
            fecha_gasto__gte=primer_mes,
            fecha_gasto__lte=hoy
        )
        .annotate(mes=TruncMonth('fecha_gasto'))
        .values('mes')
        .annotate(total=Sum('monto'))
    )

    # Organizamos los ingresos por mes.
    ingresos_por_mes = {}

    for registro in ingresos_grafica:
        fecha_mes = registro['mes']

        # Convertimos el resultado a fecha si Django devuelve datetime.
        if hasattr(fecha_mes, 'date'):
            fecha_mes = fecha_mes.date()

        ingresos_por_mes[fecha_mes] = float(
            registro['total'] or 0
        )

    # Organizamos los egresos por mes.
    egresos_por_mes = {}

    for registro in egresos_grafica:
        fecha_mes = registro['mes']

        # Convertimos el resultado a fecha si Django devuelve datetime.
        if hasattr(fecha_mes, 'date'):
            fecha_mes = fecha_mes.date()

        egresos_por_mes[fecha_mes] = float(
            registro['total'] or 0
        )

    # Preparamos las etiquetas y valores de la gráfica.
    etiquetas_grafica = []
    valores_ingresos = []
    valores_egresos = []

    for mes_actual in meses:

        # Etiqueta del mes y año.
        etiquetas_grafica.append(
            f"{nombres_meses[mes_actual.month - 1]} {mes_actual.year}"
        )

        # Total de ingresos del mes.
        valores_ingresos.append(
            ingresos_por_mes.get(mes_actual, 0)
        )

        # Total de egresos del mes.
        valores_egresos.append(
            egresos_por_mes.get(mes_actual, 0)
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

        # Datos reales para la gráfica mensual.
        'etiquetas_grafica': etiquetas_grafica,
        'valores_ingresos': valores_ingresos,
        'valores_egresos': valores_egresos,
    }

    # Mostramos el panel financiero.
    return render(
        request,
        'finanzas/panel_finanzas.html',
        contexto
    )
