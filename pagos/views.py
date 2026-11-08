


# Importamos las herramientas necesarias de Django.
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone

# Importamos el modelo Pago.
from .models import Pago

# Importamos el modelo Contrato.
from contratos.models import Contrato


# =====================================================
# LISTAR PAGOS
# =====================================================
def listar_pagos(request):

    # Consultamos todos los pagos y sus contratos.
    pagos = Pago.objects.select_related(
        'contrato',
        'contrato__cliente',
        'contrato__plan'
    ).all()

    # Calculamos las cantidades por estado.
    total_pagos = pagos.count()
    pendientes = pagos.filter(estado='pendiente').count()
    pagados = pagos.filter(estado='pagado').count()

    # Obtenemos la fecha actual.
    hoy = timezone.localdate()

    # Identificamos pagos vencidos.
    vencidos = pagos.filter(
        estado='pendiente',
        fecha_vencimiento__lt=hoy
    ).count()

    # Organizamos los datos para enviarlos a la plantilla.
    contexto = {
        'pagos': pagos,
        'total_pagos': total_pagos,
        'pendientes': pendientes,
        'pagados': pagados,
        'vencidos': vencidos,
        'today': hoy,
    }

    # Mostramos la pantalla principal de pagos.
    return render(
        request,
        'pagos/listar_pagos.html',
        contexto
    )


# =====================================================
# REGISTRAR UNA MENSUALIDAD
# =====================================================
def registrar_pago(request):

    # Consultamos los contratos activos.
    contratos = Contrato.objects.filter(
        estado='activo'
    ).select_related('cliente', 'plan')

    if request.method == 'POST':

        contrato_id = request.POST.get('contrato')
        mes_referencia = request.POST.get('mes_referencia')
        fecha_vencimiento = request.POST.get('fecha_vencimiento')

        # Buscamos el contrato seleccionado.
        contrato = get_object_or_404(
            Contrato,
            id=contrato_id,
            estado='activo'
        )

        # Tomamos el precio mensual del plan.
        valor = contrato.plan.precio_mensual

        # Creamos la mensualidad.
        try:
            Pago.objects.create(
                contrato=contrato,
                mes_referencia=mes_referencia + '-01',
                fecha_vencimiento=fecha_vencimiento,
                valor=valor,
                estado='pendiente'
            )

            messages.success(
                request,
                'La mensualidad se registró correctamente.'
            )

            return redirect('pagos:listar_pagos')

        except Exception:
            messages.error(
                request,
                'No se pudo registrar la mensualidad. '
                'Verifica que no exista ya ese mes para el contrato.'
            )

    return render(
        request,
        'pagos/registrar_pago.html',
        {'contratos': contratos}
    )


# =====================================================
# MARCAR UNA MENSUALIDAD COMO PAGADA
# =====================================================
def marcar_pagado(request, pago_id):

    # Buscamos la mensualidad.
    pago = get_object_or_404(Pago, id=pago_id)

    if request.method == 'POST':

        metodo = request.POST.get('metodo_pago')

        if metodo not in dict(Pago.METODOS_PAGO):
            messages.error(
                request,
                'Selecciona un método de pago válido.'
            )
            return redirect('pagos:listar_pagos')

        pago.estado = 'pagado'
        pago.fecha_pago = timezone.localdate()
        pago.metodo_pago = metodo
        pago.save()

        messages.success(
            request,
            'El pago se registró correctamente.'
        )

    return redirect('pagos:listar_pagos')

