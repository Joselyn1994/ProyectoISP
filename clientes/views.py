
# --------------------------------------------------
# IMPORTACIONES
# --------------------------------------------------

# Importamos herramientas de Django para mostrar páginas y redirigir.
from django.shortcuts import render, redirect, get_object_or_404

# Importamos Q para realizar búsquedas en varios campos.
from django.db.models import Q

# Importamos Paginator para dividir los resultados en páginas.
from django.core.paginator import Paginator

# Importamos messages para mostrar notificaciones.
from django.contrib import messages

# Importamos JsonResponse para enviar información a JavaScript.
from django.http import JsonResponse

# Importamos los modelos que utilizaremos en este archivo.
from .models import Cliente, Canton, Parroquia

# Importamos nuestro formulario de clientes.
from .forms import ClienteForm


# --------------------------------------------------
# REGISTRAR CLIENTES
# --------------------------------------------------

# Vista para registrar un nuevo cliente.
def registrar_cliente(request):

    # Comprobamos si el usuario envió el formulario.
    if request.method == "POST":

        # Recibimos los datos enviados por el usuario.
        formulario = ClienteForm(request.POST)

        # Comprobamos que los datos sean válidos.
        if formulario.is_valid():

            # Guardamos el cliente en PostgreSQL.
            formulario.save()

            # Mostramos un mensaje de confirmación.
            messages.success(
                request,
                "Cliente registrado correctamente."
            )

            # Redirigimos al listado de clientes.
            return redirect('clientes:listar_clientes')

        # Si existen errores, mostramos un mensaje.
        messages.error(
            request,
            "No se pudo registrar el cliente. Revise los campos."
        )

    else:

        # Si es una solicitud GET, mostramos un formulario vacío.
        formulario = ClienteForm()

    # Renderizamos la plantilla de registro.
    return render(
        request,
        "clientes/registrar_cliente.html",
        {
            "formulario": formulario,
            "titulo": "Registrar nuevo cliente",
        }
    )


# --------------------------------------------------
# LISTAR Y BUSCAR CLIENTES
# --------------------------------------------------

# Vista para consultar y buscar clientes.
def listar_clientes(request):

    # Consultamos todos los clientes.
    clientes = Cliente.objects.all().order_by('-fecha_registro')

    # Obtenemos el texto que escribió el usuario en el buscador.
    busqueda = request.GET.get('buscar', '').strip()

    # Si existe un texto de búsqueda, filtramos los resultados.
    if busqueda:

        # Buscamos coincidencias en cédula, nombres y apellidos.
        clientes = clientes.filter(
            Q(cedula__icontains=busqueda) |
            Q(nombres__icontains=busqueda) |
            Q(apellidos__icontains=busqueda)
        )

    # Creamos un paginador de 10 clientes por página.
    paginador = Paginator(clientes, 10)

    # Obtenemos el número de página solicitado.
    numero_pagina = request.GET.get('page')

    # Recuperamos los clientes correspondientes a esa página.
    pagina = paginador.get_page(numero_pagina)

    # Renderizamos la plantilla del listado.
    return render(
        request,
        "clientes/listar_clientes.html",
        {
            "pagina": pagina,
            "busqueda": busqueda,
            "total_clientes": clientes.count(),
            "titulo": "Gestión de clientes",
        }
    )


# --------------------------------------------------
# CARGAR CANTONES DE UNA PROVINCIA
# --------------------------------------------------

# Esta función consulta los cantones de la provincia seleccionada.
def cargar_cantones(request):

    # Recibimos el identificador de la provincia desde el navegador.
    provincia_id = request.GET.get('provincia_id')

    # Comprobamos que el identificador recibido sea un número.
    try:
        provincia_id = int(provincia_id)

    except (TypeError, ValueError):

        # Si el identificador no es válido, devolvemos una lista vacía.
        return JsonResponse({'cantones': []})

    # Consultamos únicamente los cantones de esa provincia.
    cantones = Canton.objects.filter(
        provincia_id=provincia_id
    ).order_by('nombre')

    # Organizamos los resultados para enviarlos al navegador.
    datos = [
        {
            'id': canton.id,
            'nombre': canton.nombre
        }
        for canton in cantones
    ]

    # Enviamos los cantones en formato JSON.
    return JsonResponse({'cantones': datos})


# --------------------------------------------------
# CARGAR PARROQUIAS DE UN CANTÓN
# --------------------------------------------------

# Esta función consulta las parroquias del cantón seleccionado.
def cargar_parroquias(request):

    # Recibimos el identificador del cantón desde el navegador.
    canton_id = request.GET.get('canton_id')

    # Comprobamos que el identificador recibido sea un número.
    try:
        canton_id = int(canton_id)

    except (TypeError, ValueError):

        # Si el identificador no es válido, devolvemos una lista vacía.
        return JsonResponse({'parroquias': []})

    # Consultamos únicamente las parroquias de ese cantón.
    parroquias = Parroquia.objects.filter(
        canton_id=canton_id
    ).order_by('nombre')

    # Organizamos los resultados para enviarlos al navegador.
    datos = [
        {
            'id': parroquia.id,
            'nombre': parroquia.nombre
        }
        for parroquia in parroquias
    ]

    # Enviamos las parroquias en formato JSON.
    return JsonResponse({'parroquias': datos})

# --------------------------------------------------
# EDITAR CLIENTES
# --------------------------------------------------

# Vista para modificar la información de un cliente.
def editar_cliente(request, cliente_id):

    # Buscamos el cliente por su ID.
    # Si no existe, Django mostrará un error 404.
    cliente = get_object_or_404(Cliente, id=cliente_id)

    # Comprobamos si el usuario envió el formulario.
    if request.method == "POST":

        # Cargamos los datos enviados y los relacionamos
        # con el cliente que estamos editando.
        formulario = ClienteForm(request.POST, instance=cliente)

        # Validamos los datos.
        if formulario.is_valid():

            # Guardamos los cambios en PostgreSQL.
            formulario.save()

            # Mostramos un mensaje de confirmación.
            messages.success(
                request,
                "Los datos del cliente se actualizaron correctamente."
            )

            # Regresamos al listado de clientes.
            return redirect('clientes:listar_clientes')

        # Si existen errores, mostramos una notificación.
        messages.error(
            request,
            "No se pudieron actualizar los datos. Revise los campos."
        )

    else:

        # Mostramos el formulario con los datos actuales del cliente.
        formulario = ClienteForm(instance=cliente)

    # Utilizamos la misma plantilla del registro.
    return render(
        request,
        "clientes/registrar_cliente.html",
        {
            "formulario": formulario,
            "titulo": "Editar información del cliente",
            "cliente": cliente,
        }
    )


# --------------------------------------------------
# ACTIVAR Y DESACTIVAR CLIENTES
# --------------------------------------------------

# Vista para cambiar el estado de un cliente.
def cambiar_estado_cliente(request, cliente_id):

    # Solo permitimos cambiar el estado mediante POST.
    if request.method == 'POST':

        # Buscamos el cliente por su identificador.
        cliente = get_object_or_404(Cliente, id=cliente_id)

        # Si está activo, lo cambiamos a inactivo.
        if cliente.estado == 'activo':
            cliente.estado = 'inactivo'
            mensaje = 'El cliente fue desactivado correctamente.'

        # Si está inactivo, lo cambiamos a activo.
        else:
            cliente.estado = 'activo'
            mensaje = 'El cliente fue activado correctamente.'

        # Guardamos únicamente el cambio de estado.
        cliente.save(update_fields=['estado'])

        # Mostramos un mensaje de confirmación.
        messages.success(request, mensaje)

    # Regresamos al listado de clientes.
    return redirect('clientes:listar_clientes')

