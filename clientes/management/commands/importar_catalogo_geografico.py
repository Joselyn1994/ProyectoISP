
# Importamos Path para trabajar con las rutas de los archivos.
from pathlib import Path

# Importamos las herramientas para crear comandos personalizados.
from django.core.management.base import BaseCommand, CommandError

# Importamos transaction para proteger la información durante la importación.
from django.db import transaction

# Importamos los modelos geográficos.
from clientes.models import Provincia, Canton, Parroquia

# Importamos la herramienta para leer archivos Excel.
from openpyxl import load_workbook


# --------------------------------------------------
# FUNCIÓN PARA NORMALIZAR LOS CÓDIGOS
# --------------------------------------------------

def normalizar_codigo(valor, longitud):

    # Comprobamos que el valor no esté vacío.
    if valor is None:
        return None

    # Convertimos el código a texto y quitamos espacios.
    codigo = str(valor).strip()

    # Evitamos que los números terminen en .0.
    if codigo.endswith('.0'):
        codigo = codigo[:-2]

    # Completamos con ceros a la izquierda.
    return codigo.zfill(longitud)


# --------------------------------------------------
# COMANDO PRINCIPAL DE IMPORTACIÓN
# --------------------------------------------------

class Command(BaseCommand):

    # Describimos la función del comando.
    help = 'Importa el catálogo geográfico oficial del Ecuador.'

    # Método que ejecuta el comando.
    def handle(self, *args, **options):

        # Obtenemos la carpeta principal del proyecto.
        carpeta_proyecto = Path(__file__).resolve().parents[3]

        # Construimos la ruta del archivo Excel.
        ruta_excel = carpeta_proyecto / 'datos' / 'CODIFICACIÓN_2025.xlsx'

        # Comprobamos que el archivo exista.
        if not ruta_excel.exists():
            raise CommandError(
                f'No se encontró el archivo: {ruta_excel}'
            )

        # Abrimos el archivo Excel.
        archivo = load_workbook(ruta_excel, data_only=True)

        try:

            # Definimos las hojas que necesitamos.
            hojas_necesarias = [
                'PROVINCIAS',
                'CANTONES',
                'PARROQUIAS'
            ]

            # Comprobamos que existan todas las hojas.
            for nombre_hoja in hojas_necesarias:

                # Si falta una hoja, detenemos el proceso.
                if nombre_hoja not in archivo.sheetnames:
                    raise CommandError(
                        f'No se encontró la hoja {nombre_hoja}.'
                    )

            # Obtenemos las hojas del archivo.
            hoja_provincias = archivo['PROVINCIAS']
            hoja_cantones = archivo['CANTONES']
            hoja_parroquias = archivo['PARROQUIAS']

            # Mostramos un mensaje de confirmación.
            self.stdout.write(
                self.style.SUCCESS(
                    'Archivo Excel encontrado correctamente.'
                )
            )

            # Mostramos las hojas disponibles.
            self.stdout.write(
                f'Hojas encontradas: {archivo.sheetnames}'
            )

            # Inicializamos los contadores.
            provincias_creadas = 0
            provincias_actualizadas = 0
            cantones_creados = 0
            cantones_actualizados = 0
            parroquias_creadas = 0
            parroquias_actualizadas = 0

            # Creamos diccionarios para localizar las relaciones.
            provincias_por_codigo = {}
            cantones_por_codigo = {}

            # Iniciamos una transacción segura.
            with transaction.atomic():

                # ==========================================
                # IMPORTAR PROVINCIAS
                # ==========================================

                self.stdout.write('\nImportando provincias...')

                # Recorremos las filas desde la tercera.
                for fila in hoja_provincias.iter_rows(
                    min_row=3,
                    values_only=True
                ):

                    # Obtenemos el código de provincia.
                    codigo = normalizar_codigo(fila[1], 2)

                    # Obtenemos el nombre de provincia.
                    nombre = fila[2]

                    # Ignoramos filas incompletas.
                    if not codigo or not nombre:
                        continue

                    # Limpiamos el nombre.
                    nombre = str(nombre).strip().title()

                    # Buscamos la provincia por su nombre.
                    provincia = Provincia.objects.filter(
                        nombre__iexact=nombre
                    ).first()

                    # Si la provincia ya existe, la actualizamos.
                    if provincia:

                        # Comprobamos que el código no esté ocupado.
                        conflicto = Provincia.objects.filter(
                            codigo=codigo
                        ).exclude(pk=provincia.pk).exists()

                        # Detenemos la importación si existe un conflicto.
                        if conflicto:
                            raise CommandError(
                                f'El código {codigo} pertenece a otra provincia.'
                            )

                        # Actualizamos el código oficial.
                        provincia.codigo = codigo
                        provincia.save(update_fields=['codigo'])

                        # Sumamos una provincia actualizada.
                        provincias_actualizadas += 1

                    else:

                        # Comprobamos si el código ya existe.
                        provincia = Provincia.objects.filter(
                            codigo=codigo
                        ).first()

                        # Evitamos asignar un código incorrecto.
                        if provincia:
                            raise CommandError(
                                f'El código {codigo} ya está registrado '
                                f'en {provincia.nombre}.'
                            )

                        # Creamos la provincia.
                        provincia = Provincia.objects.create(
                            nombre=nombre,
                            codigo=codigo
                        )

                        # Sumamos una provincia creada.
                        provincias_creadas += 1

                    # Guardamos la provincia para utilizarla después.
                    provincias_por_codigo[codigo] = provincia

                # ==========================================
                # IMPORTAR CANTONES
                # ==========================================

                self.stdout.write('Importando cantones...')

                # Recorremos las filas de cantones.
                for fila in hoja_cantones.iter_rows(
                    min_row=3,
                    values_only=True
                ):

                    # Obtenemos el código de la provincia.
                    codigo_provincia = normalizar_codigo(
                        fila[1], 2
                    )

                    # Obtenemos el código del cantón.
                    codigo_canton = normalizar_codigo(
                        fila[3], 4
                    )

                    # Obtenemos el nombre del cantón.
                    nombre = fila[4]

                    # Ignoramos registros incompletos.
                    if not codigo_provincia or not codigo_canton or not nombre:
                        continue

                    # Buscamos la provincia correspondiente.
                    provincia = provincias_por_codigo.get(
                        codigo_provincia
                    )

                    # Comprobamos que exista la provincia.
                    if not provincia:
                        raise CommandError(
                            f'No existe la provincia {codigo_provincia}.'
                        )

                    # Limpiamos el nombre del cantón.
                    nombre = str(nombre).strip().title()

                    # Creamos o actualizamos el cantón.
                    canton, creado = Canton.objects.update_or_create(
                        codigo=codigo_canton,
                        defaults={
                            'provincia': provincia,
                            'nombre': nombre
                        }
                    )

                    # Guardamos el cantón para relacionarlo después.
                    cantones_por_codigo[codigo_canton] = canton

                    # Actualizamos los contadores.
                    if creado:
                        cantones_creados += 1
                    else:
                        cantones_actualizados += 1

                # ==========================================
                # IMPORTAR PARROQUIAS
                # ==========================================

                self.stdout.write('Importando parroquias...')

                # Recorremos las filas de parroquias.
                for fila in hoja_parroquias.iter_rows(
                    min_row=3,
                    values_only=True
                ):

                    # Obtenemos el código del cantón.
                    codigo_canton = normalizar_codigo(
                        fila[3], 4
                    )

                    # Obtenemos el código de la parroquia.
                    codigo_parroquia = normalizar_codigo(
                        fila[5], 6
                    )

                    # Obtenemos el nombre de la parroquia.
                    nombre = fila[6]

                    # Ignoramos registros incompletos.
                    if not codigo_canton or not codigo_parroquia or not nombre:
                        continue

                    # Buscamos el cantón correspondiente.
                    canton = cantones_por_codigo.get(
                        codigo_canton
                    )

                    # Comprobamos que exista el cantón.
                    if not canton:
                        raise CommandError(
                            f'No existe el cantón {codigo_canton}.'
                        )

                    # Limpiamos el nombre de la parroquia.
                    nombre = str(nombre).strip().title()

                    # Creamos o actualizamos la parroquia.
                    parroquia, creado = Parroquia.objects.update_or_create(
                        codigo=codigo_parroquia,
                        defaults={
                            'canton': canton,
                            'nombre': nombre
                        }
                    )

                    # Actualizamos los contadores.
                    if creado:
                        parroquias_creadas += 1
                    else:
                        parroquias_actualizadas += 1

            # ==========================================
            # MOSTRAR RESULTADOS
            # ==========================================

            self.stdout.write('\n--- RESULTADO DE LA IMPORTACIÓN ---')

            self.stdout.write(
                f'Provincias creadas: {provincias_creadas}'
            )
            self.stdout.write(
                f'Provincias actualizadas: {provincias_actualizadas}'
            )
            self.stdout.write(
                f'Cantones creados: {cantones_creados}'
            )
            self.stdout.write(
                f'Cantones actualizados: {cantones_actualizados}'
            )
            self.stdout.write(
                f'Parroquias creadas: {parroquias_creadas}'
            )
            self.stdout.write(
                f'Parroquias actualizadas: {parroquias_actualizadas}'
            )

            # Mostramos los totales existentes en PostgreSQL.
            self.stdout.write('\n--- TOTALES EN POSTGRESQL ---')

            self.stdout.write(
                f'Provincias: {Provincia.objects.count()}'
            )
            self.stdout.write(
                f'Cantones: {Canton.objects.count()}'
            )
            self.stdout.write(
                f'Parroquias: {Parroquia.objects.count()}'
            )

            # Confirmamos que terminó correctamente.
            self.stdout.write(
                self.style.SUCCESS(
                    '\n¡Catálogo geográfico importado correctamente!'
                )
            )

        finally:

            # Cerramos el archivo Excel al terminar.
            archivo.close()



