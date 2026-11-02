# Importamos models, que nos permite crear tablas en la base de datos.
from django.db import models


# Creamos la clase Cliente, que representa a cada abonado de Teleguepi ISP.
class Cliente(models.Model):

    # Definimos los estados que podrá tener un cliente.
    ESTADOS = [
        ('activo', 'Activo'),       # El cliente tiene el servicio activo.
        ('inactivo', 'Inactivo'),   # El cliente ya no tiene el servicio activo.
    ]

    # Guardamos la cédula del cliente.
    # max_length=10 permite almacenar hasta 10 caracteres.
    # unique=True impide registrar dos clientes con la misma cédula.
    # verbose_name establece el nombre que se mostrará en formularios.
    cedula = models.CharField(
        max_length=10,
        unique=True,
        verbose_name='Cédula'
    )

    # Guardamos los nombres del cliente, con un máximo de 100 caracteres.
    nombres = models.CharField(max_length=100)

    # Guardamos los apellidos del cliente, con un máximo de 100 caracteres.
    apellidos = models.CharField(max_length=100)

    # Guardamos el número telefónico del cliente.
    # Utilizamos CharField porque los teléfonos no se usan para operaciones matemáticas.
    telefono = models.CharField(max_length=15)

    # Guardamos el correo electrónico.
    # blank=True permite dejar el campo vacío en los formularios.
    # null=True permite que la base de datos almacene un valor nulo.
    correo = models.EmailField(blank=True, null=True)

    # Guardamos la provincia donde vive el cliente.
    provincia = models.CharField(max_length=100)

    # Guardamos el cantón donde vive el cliente.
    canton = models.CharField(max_length=100)

    # Guardamos el sector, barrio o comunidad del cliente.
    sector = models.CharField(max_length=100)

    # Guardamos la dirección detallada donde está instalado el servicio.
    # TextField permite escribir textos más extensos.
    direccion = models.TextField()

    # Registramos automáticamente la fecha y hora de creación del cliente.
    fecha_registro = models.DateTimeField(auto_now_add=True)

    # Guardamos el estado actual del cliente.
    # choices limita las opciones a las definidas en ESTADOS.
    # default establece "activo" como estado inicial.
    estado = models.CharField(
        max_length=10,
        choices=ESTADOS,
        default='activo'
    )

    # Definimos cómo se mostrará el cliente cuando Django lo represente como texto.
    def __str__(self):
        # Devolvemos los nombres, apellidos y cédula del cliente.
        return f'{self.nombres} {self.apellidos} - {self.cedula}'