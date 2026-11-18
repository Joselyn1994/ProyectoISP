
# Importamos las herramientas necesarias de Django.
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

# Importamos el modelo y el formulario.
from .models import Contrato
from .forms import ContratoForm

# Herramientas para devolver respuestas JSON y generar archivos PDF.
from django.http import JsonResponse, HttpResponse

# Herramientas de ReportLab para diseñar documentos PDF.
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle

# Importamos el modelo Cliente.
from clientes.models import Cliente

# Importamos el modelo de los planes de Internet.
from planes.models import PlanInternet


# --------------------------------------------------
# LISTAR CONTRATOS
# --------------------------------------------------

def listar_contratos(request):

    # Obtenemos todos los contratos registrados.
    contratos = Contrato.objects.select_related(
        'cliente',
        'plan'
    ).all()

    return render(request, 'contratos/listar_contratos.html', {
        'contratos': contratos,
        'titulo': 'Gestión de contratos',
    })


# --------------------------------------------------
# REGISTRAR CONTRATOS
# --------------------------------------------------

def registrar_contrato(request):

    if request.method == 'POST':

        formulario = ContratoForm(request.POST)

        if formulario.is_valid():

            formulario.save()

            messages.success(
                request,
                'El contrato se registró correctamente.'
            )

            return redirect('contratos:listar_contratos')

    else:

        formulario = ContratoForm()

    return render(request, 'contratos/registrar_contrato.html', {
        'formulario': formulario,
        'titulo': 'Registrar contrato',
    })


# --------------------------------------------------
# EDITAR CONTRATOS
# --------------------------------------------------

def editar_contrato(request, contrato_id):

    contrato = get_object_or_404(
        Contrato,
        id=contrato_id
    )

    if request.method == 'POST':

        formulario = ContratoForm(
            request.POST,
            instance=contrato
        )

        if formulario.is_valid():

            formulario.save()

            messages.success(
                request,
                'El contrato se actualizó correctamente.'
            )

            return redirect('contratos:listar_contratos')

    else:

        formulario = ContratoForm(instance=contrato)

    return render(request, 'contratos/registrar_contrato.html', {
        'formulario': formulario,
        'contrato': contrato,
        'titulo': 'Editar contrato',
    })


# --------------------------------------------------
# CAMBIAR ESTADO DEL CONTRATO
# --------------------------------------------------

def cambiar_estado_contrato(request, contrato_id):

    if request.method == 'POST':

        contrato = get_object_or_404(
            Contrato,
            id=contrato_id
        )

        if contrato.estado == 'activo':

            contrato.estado = 'suspendido'
            mensaje = 'El contrato fue suspendido correctamente.'

        elif contrato.estado == 'suspendido':

            contrato.estado = 'activo'
            mensaje = 'El contrato fue activado correctamente.'

        else:

            messages.error(
                request,
                'No se puede cambiar el estado de un contrato finalizado.'
            )

            return redirect('contratos:listar_contratos')

        contrato.save(update_fields=['estado'])

        messages.success(request, mensaje)

    return redirect('contratos:listar_contratos')

# --------------------------------------------------
# BUSCAR CLIENTE POR CÉDULA
# --------------------------------------------------

def buscar_cliente(request):

    # Obtenemos la cédula enviada desde el formulario.
    cedula = request.GET.get('cedula', '').strip()

    # Buscamos al cliente activo con esa cédula.
    cliente = Cliente.objects.filter(
        cedula=cedula,
        estado='activo'
    ).first()

    # Si no encontramos al cliente.
    if not cliente:

        return JsonResponse({
            'encontrado': False,
            'mensaje': 'No se encontró un cliente activo con esa cédula.'
        })

    # Si encontramos al cliente, devolvemos sus datos.
    return JsonResponse({
        'encontrado': True,
        'id': cliente.id,
        'cedula': cliente.cedula,
        'nombres': cliente.nombres,
        'apellidos': cliente.apellidos,
        'telefono': cliente.telefono,
        'correo': cliente.correo or '',
        'direccion': cliente.direccion,
    })

# --------------------------------------------------
# GENERAR CONTRATO EN PDF
# --------------------------------------------------

def generar_pdf_contrato(request, contrato_id):

    # Buscamos el contrato y obtenemos también sus datos relacionados.
    contrato = get_object_or_404(
        Contrato.objects.select_related('cliente', 'plan'),
        id=contrato_id
    )

    # Creamos la respuesta que devolverá un archivo PDF.
    respuesta = HttpResponse(content_type='application/pdf')

    # Indicamos el nombre con el que se descargará el archivo.
    respuesta['Content-Disposition'] = (
        f'attachment; filename="contrato_{contrato.codigo}.pdf"'
    )

    # Configuramos el documento en tamaño A4.
    documento = SimpleDocTemplate(
        respuesta,
        pagesize=A4,
        rightMargin=20 * mm,
        leftMargin=20 * mm,
        topMargin=20 * mm,
        bottomMargin=20 * mm
    )

    # Cargamos los estilos básicos de ReportLab.
    estilos = getSampleStyleSheet()

    # Estilo para el nombre de la empresa.
    estilo_titulo = ParagraphStyle(
        'TituloEmpresa',
        parent=estilos['Title'],
        fontSize=20,
        textColor=colors.HexColor('#173B63'),
        alignment=TA_CENTER,
        spaceAfter=8
    )

    # Estilo para el subtítulo.
    estilo_subtitulo = ParagraphStyle(
        'Subtitulo',
        parent=estilos['Normal'],
        fontSize=11,
        alignment=TA_CENTER,
        textColor=colors.HexColor('#555555'),
        spaceAfter=18
    )

    # Estilo para los textos del documento.
    estilo_texto = estilos['BodyText']

    # Lista donde organizaremos el contenido del PDF.
    contenido = []

    # Encabezado del documento.
    contenido.append(
        Paragraph('TELEGUEPI ISP', estilo_titulo)
    )

    contenido.append(
        Paragraph(
            'CONTRATO DE PRESTACIÓN DE SERVICIOS DE INTERNET',
            estilo_subtitulo
        )
    )

    # Código del contrato.
    contenido.append(
        Paragraph(
            f'<b>Código del contrato:</b> {contrato.codigo}',
            estilo_texto
        )
    )

    contenido.append(Spacer(1, 12))

    # Datos del cliente.
    datos_cliente = [
        ['DATOS DEL CLIENTE', ''],
        ['Cédula:', contrato.cliente.cedula],
        [
            'Nombres y apellidos:',
            f'{contrato.cliente.nombres} {contrato.cliente.apellidos}'
        ],
        ['Teléfono:', contrato.cliente.telefono],
        ['Correo:', contrato.cliente.correo or 'No registrado'],
        ['Dirección:', contrato.cliente.direccion],
    ]

    tabla_cliente = Table(
        datos_cliente,
        colWidths=[55 * mm, 105 * mm]
    )

    tabla_cliente.setStyle(TableStyle([
        ('SPAN', (0, 0), (1, 0)),
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#173B63')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTNAME', (0, 1), (0, -1), 'Helvetica-Bold'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#CCCCCC')),
        ('PADDING', (0, 0), (-1, -1), 8),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))

    contenido.append(tabla_cliente)
    contenido.append(Spacer(1, 18))

    # Datos del plan contratado.
    datos_plan = [
        ['DETALLES DEL PLAN DE INTERNET', ''],
        ['Nombre del plan:', contrato.plan.nombre],
        ['Velocidad:', f'{contrato.plan.velocidad} Mbps'],
        ['Precio mensual:', f'$ {contrato.plan.precio_mensual}'],
    ]

    tabla_plan = Table(
        datos_plan,
        colWidths=[55 * mm, 105 * mm]
    )

    tabla_plan.setStyle(TableStyle([
        ('SPAN', (0, 0), (1, 0)),
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#173B63')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTNAME', (0, 1), (0, -1), 'Helvetica-Bold'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#CCCCCC')),
        ('PADDING', (0, 0), (-1, -1), 8),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))

    contenido.append(tabla_plan)
    contenido.append(Spacer(1, 18))

    # Fechas y estado del contrato.
    fecha_fin = (
        contrato.fecha_fin.strftime('%d/%m/%Y')
        if contrato.fecha_fin else 'Indefinida'
    )

    datos_contrato = [
        ['INFORMACIÓN DEL CONTRATO', ''],
        ['Fecha de inicio:', contrato.fecha_inicio.strftime('%d/%m/%Y')],
        ['Fecha de finalización:', fecha_fin],
        ['Estado:', contrato.get_estado_display()],
        ['Observaciones:', contrato.observaciones or 'Sin observaciones'],
    ]

    tabla_contrato = Table(
        datos_contrato,
        colWidths=[55 * mm, 105 * mm]
    )

    tabla_contrato.setStyle(TableStyle([
        ('SPAN', (0, 0), (1, 0)),
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#173B63')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTNAME', (0, 1), (0, -1), 'Helvetica-Bold'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#CCCCCC')),
        ('PADDING', (0, 0), (-1, -1), 8),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))

    contenido.append(tabla_contrato)
    contenido.append(Spacer(1, 40))

    # Espacios para las firmas.
    firmas = [
        ['____________________________', '____________________________'],
        ['Firma del cliente', 'Firma del proveedor'],
    ]

    tabla_firmas = Table(
        firmas,
        colWidths=[80 * mm, 80 * mm]
    )

    tabla_firmas.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 1), (-1, 1), 'Helvetica-Bold'),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
    ]))

    contenido.append(tabla_firmas)

    # Construimos el documento PDF.
    documento.build(contenido)

    # Entregamos el archivo al navegador.
    return respuesta

# --------------------------------------------------
# OBTENER LOS DATOS DEL PLAN SELECCIONADO
# --------------------------------------------------

def obtener_datos_plan(request):

    # Obtenemos el identificador del plan enviado por el navegador.
    plan_id = request.GET.get('plan_id')

    # Buscamos el plan solamente si está activo.
    plan = PlanInternet.objects.filter(
        id=plan_id,
        estado='activo'
    ).first()

    # Si el plan no existe o está inactivo, informamos que no se encontró.
    if not plan:
        return JsonResponse({
            'encontrado': False
        })

    # Devolvemos los datos del plan en formato JSON.
    return JsonResponse({
        'encontrado': True,
        'nombre': plan.nombre,
        'velocidad': plan.velocidad,
        'precio_mensual': str(plan.precio_mensual)
    })