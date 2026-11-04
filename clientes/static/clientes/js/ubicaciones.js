
// --------------------------------------------------
// UBICACIONES GEOGRÁFICAS DE TELEGUEPI ISP
// --------------------------------------------------

// Esperamos a que el documento HTML esté completamente cargado.
document.addEventListener('DOMContentLoaded', function () {

    // Buscamos el formulario de registro de clientes.
    const formulario = document.getElementById('formulario-cliente');

    // Comprobamos que el formulario exista.
    if (!formulario) {
        return;
    }

    // Obtenemos los campos de ubicación del formulario.
    const provincia = document.getElementById('id_provincia_geo');
    const canton = document.getElementById('id_canton_geo');
    const parroquia = document.getElementById('id_parroquia');

    // Obtenemos las direcciones de consulta configuradas en Django.
    const urlCantones = formulario.dataset.urlCantones;
    const urlParroquias = formulario.dataset.urlParroquias;

    // Comprobamos que existan todos los campos y direcciones.
    if (!provincia || !canton || !parroquia || !urlCantones || !urlParroquias) {
        console.error('No se encontraron los campos o las direcciones de ubicación.');
        return;
    }

    // --------------------------------------------------
    // FUNCIÓN PARA LIMPIAR UNA LISTA
    // --------------------------------------------------

    // Elimina las opciones anteriores y muestra un mensaje inicial.
    function limpiarLista(campo, mensaje) {

        // Eliminamos todas las opciones existentes.
        campo.innerHTML = '';

        // Creamos la opción inicial.
        const opcion = document.createElement('option');

        // Dejamos su valor vacío.
        opcion.value = '';

        // Escribimos el mensaje que verá el usuario.
        opcion.textContent = mensaje;

        // Agregamos la opción al campo.
        campo.appendChild(opcion);
    }

    // --------------------------------------------------
    // CARGAR CANTONES
    // --------------------------------------------------

    // Escuchamos cuando el usuario selecciona una provincia.
    provincia.addEventListener('change', async function () {

        // Guardamos el identificador de la provincia seleccionada.
        const provinciaId = provincia.value;

        // Limpiamos las listas dependientes.
        limpiarLista(canton, 'Cargando cantones...');
        limpiarLista(parroquia, 'Seleccione primero un cantón');

        // Deshabilitamos las listas mientras se realiza la consulta.
        canton.disabled = true;
        parroquia.disabled = true;

        // Si no se seleccionó una provincia, terminamos.
        if (!provinciaId) {
            limpiarLista(canton, 'Seleccione una provincia primero');
            return;
        }

        try {

            // Consultamos Django para obtener los cantones.
            const respuesta = await fetch(
                `${urlCantones}?provincia_id=${encodeURIComponent(provinciaId)}`
            );

            // Comprobamos que la respuesta sea correcta.
            if (!respuesta.ok) {
                throw new Error('No se pudieron consultar los cantones.');
            }

            // Convertimos la respuesta a formato JSON.
            const datos = await respuesta.json();

            // Limpiamos la lista antes de agregar los resultados.
            limpiarLista(canton, 'Seleccione un cantón');

            // Recorremos los cantones recibidos.
            datos.cantones.forEach(function (item) {

                // Creamos una nueva opción.
                const opcion = document.createElement('option');

                // Asignamos el identificador del cantón.
                opcion.value = item.id;

                // Mostramos el nombre del cantón.
                opcion.textContent = item.nombre;

                // Agregamos el cantón a la lista.
                canton.appendChild(opcion);
            });

            // Habilitamos el campo si existen cantones.
            canton.disabled = datos.cantones.length === 0;

            // Si no existen cantones, mostramos un mensaje.
            if (datos.cantones.length === 0) {
                limpiarLista(canton, 'No hay cantones disponibles');
            }

        } catch (error) {

            // Mostramos el error en la consola del navegador.
            console.error(error);

            // Informamos que ocurrió un problema.
            limpiarLista(canton, 'Error al cargar cantones');

        }

    });

    // --------------------------------------------------
    // CARGAR PARROQUIAS
    // --------------------------------------------------

    // Escuchamos cuando el usuario selecciona un cantón.
    canton.addEventListener('change', async function () {

        // Guardamos el identificador del cantón seleccionado.
        const cantonId = canton.value;

        // Limpiamos la lista de parroquias.
        limpiarLista(parroquia, 'Cargando parroquias...');

        // Deshabilitamos el campo mientras se realiza la consulta.
        parroquia.disabled = true;

        // Si no se seleccionó un cantón, terminamos.
        if (!cantonId) {
            limpiarLista(parroquia, 'Seleccione primero un cantón');
            return;
        }

        try {

            // Consultamos Django para obtener las parroquias.
            const respuesta = await fetch(
                `${urlParroquias}?canton_id=${encodeURIComponent(cantonId)}`
            );

            // Comprobamos que la respuesta sea correcta.
            if (!respuesta.ok) {
                throw new Error('No se pudieron consultar las parroquias.');
            }

            // Convertimos la respuesta a formato JSON.
            const datos = await respuesta.json();

            // Limpiamos la lista antes de agregar los resultados.
            limpiarLista(parroquia, 'Seleccione una parroquia');

            // Recorremos las parroquias recibidas.
            datos.parroquias.forEach(function (item) {

                // Creamos una nueva opción.
                const opcion = document.createElement('option');

                // Asignamos el identificador de la parroquia.
                opcion.value = item.id;

                // Mostramos el nombre de la parroquia.
                opcion.textContent = item.nombre;

                // Agregamos la parroquia a la lista.
                parroquia.appendChild(opcion);
            });

            // Habilitamos el campo si existen parroquias.
            parroquia.disabled = datos.parroquias.length === 0;

            // Si no existen parroquias, mostramos un mensaje.
            if (datos.parroquias.length === 0) {
                limpiarLista(parroquia, 'No hay parroquias disponibles');
            }

        } catch (error) {

            // Mostramos el error en la consola del navegador.
            console.error(error);

            // Informamos que ocurrió un problema.
            limpiarLista(parroquia, 'Error al cargar parroquias');

        }

    });

    // --------------------------------------------------
    // ESTADO INICIAL DEL FORMULARIO
    // --------------------------------------------------

    // Deshabilitamos cantón hasta que se seleccione una provincia.
    canton.disabled = true;

    // Deshabilitamos parroquia hasta que se seleccione un cantón.
    parroquia.disabled = true;

});
