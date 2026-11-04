
# Importamos models para crear las tablas y relaciones de la base de datos.
from django.db import models

# Importamos nuestra función personalizada para validar cédulas ecuatorianas.
from .validaciones import validar_cedula_ecuatoriana


# --------------------------------------------------
# MODELO CLIENTE
# --------------------------------------------------

# Representa a cada abonado de Teleguepi ISP.
class Cliente(models.Model):

    # Definimos los estados que podrá tener un cliente.
    ESTADOS = [
        ('activo', 'Activo'),
        ('inactivo', 'Inactivo'),
    ]

    # Guardamos la cédula y validamos que sea ecuatoriana.
    cedula = models.CharField(
        max_length=10,
        unique=True,
        verbose_name='Cédula',
        validators=[validar_cedula_ecuatoriana]
    )

    # Guardamos los nombres del cliente.
    nombres = models.CharField(max_length=100)

    # Guardamos los apellidos del cliente.
    apellidos = models.CharField(max_length=100)

    # Guardamos el número telefónico.
    telefono = models.CharField(max_length=15)

    # Guardamos el correo electrónico.
    correo = models.EmailField(blank=True, null=True)

    # Conservamos la provincia escrita en el registro anterior.
    # Posteriormente podremos migrar estos datos al catálogo geográfico.
    provincia = models.CharField(max_length=100)

    # Conservamos el cantón escrito en el registro anterior.
    canton = models.CharField(max_length=100)

    # Conservamos el sector escrito anteriormente.
    sector = models.CharField(max_length=100)

    # Guardamos la dirección detallada del cliente.
    direccion = models.TextField()

    # Nueva relación con el catálogo oficial de provincias.
    provincia_geo = models.ForeignKey(
        'Provincia',
        on_delete=models.PROTECT,
        related_name='clientes',
        null=True,
        blank=True,
        verbose_name='Provincia'
    )

    # Nueva relación con el catálogo oficial de cantones.
    canton_geo = models.ForeignKey(
        'Canton',
        on_delete=models.PROTECT,
        related_name='clientes',
        null=True,
        blank=True,
        verbose_name='Cantón'
    )

    # Nueva relación con el catálogo oficial de parroquias.
    parroquia = models.ForeignKey(
        'Parroquia',
        on_delete=models.PROTECT,
        related_name='clientes',
        null=True,
        blank=True,
        verbose_name='Parroquia'
    )

    # Registramos automáticamente la fecha y hora de creación.
    fecha_registro = models.DateTimeField(auto_now_add=True)

    # Guardamos el estado actual del cliente.
    estado = models.CharField(
        max_length=10,
        choices=ESTADOS,
        default='activo'
    )

    # Indicamos cómo se mostrará el cliente.
    def __str__(self):
        return f'{self.nombres} {self.apellidos} - {self.cedula}'


# --------------------------------------------------
# MODELO PROVINCIA
# --------------------------------------------------

# Representa las provincias del Ecuador.
class Provincia(models.Model):

    # Guardamos el nombre de la provincia.
    nombre = models.CharField(max_length=100, unique=True)

    # Guardamos el código geográfico oficial.
    codigo = models.CharField(
        max_length=6,
        unique=True,
        null=True,
        blank=True,
        verbose_name='Código geográfico'
    )

    # Indicamos cómo se mostrará la provincia.
    def __str__(self):
        return self.nombre

    # Definimos el nombre de la tabla en PostgreSQL.
    class Meta:
        verbose_name = 'Provincia'
        verbose_name_plural = 'Provincias'
        ordering = ['nombre']


# --------------------------------------------------
# MODELO CANTÓN
# --------------------------------------------------

# Representa los cantones pertenecientes a una provincia.
class Canton(models.Model):

    # Relacionamos cada cantón con su provincia.
    provincia = models.ForeignKey(
        Provincia,
        on_delete=models.PROTECT,
        related_name='cantones'
    )

    # Guardamos el nombre del cantón.
    nombre = models.CharField(max_length=100)

    # Guardamos el código geográfico oficial.
    codigo = models.CharField(
        max_length=6,
        unique=True,
        null=True,
        blank=True,
        verbose_name='Código geográfico'
    )

    # Evitamos repetir cantones dentro de una misma provincia.
    class Meta:
        unique_together = ('provincia', 'nombre')
        verbose_name = 'Cantón'
        verbose_name_plural = 'Cantones'
        ordering = ['nombre']

    # Indicamos cómo se mostrará el cantón.
    def __str__(self):
        return f'{self.nombre} - {self.provincia.nombre}'


# --------------------------------------------------
# MODELO PARROQUIA
# --------------------------------------------------

# Representa las parroquias pertenecientes a un cantón.
class Parroquia(models.Model):

    # Relacionamos cada parroquia con su cantón.
    canton = models.ForeignKey(
        Canton,
        on_delete=models.PROTECT,
        related_name='parroquias'
    )

    # Guardamos el nombre de la parroquia.
    nombre = models.CharField(max_length=100)

    # Guardamos el código geográfico oficial.
    codigo = models.CharField(
        max_length=6,
        unique=True,
        null=True,
        blank=True,
        verbose_name='Código geográfico'
    )

    # Evitamos repetir parroquias dentro de un mismo cantón.
    class Meta:
        unique_together = ('canton', 'nombre')
        verbose_name = 'Parroquia'
        verbose_name_plural = 'Parroquias'
        ordering = ['nombre']

    # Indicamos cómo se mostrará la parroquia.
    def __str__(self):
        return f'{self.nombre} - {self.canton.nombre}'


# --------------------------------------------------
# MODELO SECTOR
# --------------------------------------------------

# Representa los barrios, ciudadelas o comunidades.
class Sector(models.Model):

    # Relacionamos cada sector con su parroquia.
    parroquia = models.ForeignKey(
        Parroquia,
        on_delete=models.PROTECT,
        related_name='sectores'
    )

    # Guardamos el nombre del sector.
    nombre = models.CharField(max_length=100)

    # Evitamos repetir sectores dentro de una misma parroquia.
    class Meta:
        unique_together = ('parroquia', 'nombre')
        verbose_name = 'Sector'
        verbose_name_plural = 'Sectores'
        ordering = ['nombre']

    # Indicamos cómo se mostrará el sector.
    def __str__(self):
        return f'{self.nombre} - {self.parroquia.nombre}'
