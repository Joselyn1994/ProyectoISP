# =====================================================
# IMPORTACIONES
# =====================================================

from django.shortcuts import render
from django.db.models import Sum
from django.utils import timezone

# Modelos de los modulos del sistema
from clientes.models import Cliente
from planes.models import PlanInternet
from contratos.models import Contrato
from pagos.models import Pago
from gastos.models import Gasto


# =====================================================
# PANEL PRINCIPAL
# =====================================================

def dashboard(request):

    hoy = timezone.localdate()

    # -----------------------------------------
    # CLIENTES
    # -----------------------------------------

    total_clientes = Cliente.objects.count()

    clientes_activos = Cliente.objects.filter(
        estado='activo'
    ).count()

    clientes_inactivos = Cliente.objects.filter(
        estado='inactivo'
    ).count()

    # -----------------------------------------
    # PLANES DE INTERNET
    # -----------------------------------------

    total_planes = PlanInternet.objects.count()

    planes_disponibles = PlanInternet.objects.filter(
        estado='activo'
    ).count()

    planes_inactivos = PlanInternet.objects.filter(
        estado='inactivo'
    ).count()

    # -----------------------------------------
    # CONTRATOS
    # -----------------------------------------

    total_contratos = Contrato.objects.count()

    contratos_activos = Contrato.objects.filter(
        estado='activo'
    ).count()

    contratos_suspendidos = Contrato.objects.filter(
        estado='suspendido'
    ).count()

    contratos_finalizados = Contrato.objects.filter(
        estado='finalizado'
    ).count()

    # -----------------------------------------
    # PAGOS
    # -----------------------------------------

    total_pagos = Pago.objects.count()

    pagos_pendientes = Pago.objects.filter(
        estado='pendiente'
    ).count()

    pagos_vencidos = Pago.objects.filter(
        estado='pendiente',
        fecha_vencimiento__lt=hoy
    ).count()

    pagos_pagados_mes = Pago.objects.filter(
        estado='pagado',
        fecha_pago__year=hoy.year,
        fecha_pago__month=hoy.month
    ).count()

    # -----------------------------------------
    # INGRESOS DEL MES
    # -----------------------------------------

    ingresos_mes = Pago.objects.filter(
        estado='pagado',
        fecha_pago__year=hoy.year,
        fecha_pago__month=hoy.month
    ).aggregate(
        total=Sum('valor')
    )['total'] or 0

    # -----------------------------------------
    # GASTOS DEL MES
    # -----------------------------------------

    gastos_mes = Gasto.objects.filter(
        fecha_gasto__year=hoy.year,
        fecha_gasto__month=hoy.month
    ).aggregate(
        total=Sum('monto')
    )['total'] or 0

    gastos_registrados = Gasto.objects.count()

    # -----------------------------------------
    # BALANCE DEL MES
    # -----------------------------------------

    balance_mes = ingresos_mes - gastos_mes

    # -----------------------------------------
    # DATOS PARA EL GRAFICO ANUAL
    # -----------------------------------------

    nombres_meses = [
        'Enero', 'Febrero', 'Marzo', 'Abril',
        'Mayo', 'Junio', 'Julio', 'Agosto',
        'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'
    ]

    ingresos_mensuales = []

    for numero_mes in range(1, 13):

        total = Pago.objects.filter(
            estado='pagado',
            fecha_pago__year=hoy.year,
            fecha_pago__month=numero_mes
        ).aggregate(
            total=Sum('valor')
        )['total'] or 0

        ingresos_mensuales.append(float(total))

    # -----------------------------------------
    # INFORMACION PARA EL DASHBOARD
    # -----------------------------------------

    contexto = {
        # Clientes
        'total_clientes': total_clientes,
        'clientes_activos': clientes_activos,
        'clientes_inactivos': clientes_inactivos,

        # Planes
        'total_planes': total_planes,
        'planes_disponibles': planes_disponibles,
        'planes_inactivos': planes_inactivos,

        # Contratos
        'total_contratos': total_contratos,
        'contratos_activos': contratos_activos,
        'contratos_suspendidos': contratos_suspendidos,
        'contratos_finalizados': contratos_finalizados,

        # Pagos
        'total_pagos': total_pagos,
        'pagos_pendientes': pagos_pendientes,
        'pagos_vencidos': pagos_vencidos,
        'pagos_pagados_mes': pagos_pagados_mes,

        # Finanzas
        'ingresos_mes': ingresos_mes,
        'gastos_mes': gastos_mes,
        'balance_mes': balance_mes,
        'gastos_registrados': gastos_registrados,

        # Grafico
        'nombres_meses': nombres_meses,
        'ingresos_mensuales': ingresos_mensuales,
        'anio_actual': hoy.year,
    }

    return render(
        request,
        'core/dashboard.html',
        contexto
    )