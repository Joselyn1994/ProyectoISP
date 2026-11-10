# Importamos los modelos de Django.
from django.db import models


class Gasto(models.Model):

    # Categorías disponibles para clasificar los gastos.
    CATEGORIAS = [
        ('sueldos', 'Sueldos'),
        ('servicios', 'Servicios básicos'),
        ('mantenimiento', 'Mantenimiento'),
        ('equipos', 'Equipos y materiales'),
        ('transporte', 'Transporte'),
        ('otros', 'Otros'),
    ]

    # Métodos utilizados para pagar los gastos.
    METODOS_PAGO = [
        ('efectivo', 'Efectivo'),
        ('transferencia', 'Transferencia'),
        ('deposito', 'Depósito'),
        ('otro', 'Otro'),
    ]

    # Categoría a la que pertenece el gasto.
    categoria = models.CharField(
        max_length=20,
        choices=CATEGORIAS,
        verbose_name='Categoría'
    )

    # Descripción del gasto.
    descripcion = models.CharField(
        max_length=200,
        verbose_name='Descripción'
    )

    # Valor económico del gasto.
    monto = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Monto'
    )

    # Fecha en que se realizó el gasto.
    fecha_gasto = models.DateField(
        verbose_name='Fecha del gasto'
    )

    # Método utilizado para realizar el pago.
    metodo_pago = models.CharField(
        max_length=20,
        choices=METODOS_PAGO,
        verbose_name='Método de pago'
    )

    # Número o referencia del comprobante.
    comprobante = models.CharField(
        max_length=100,
        blank=True,
        verbose_name='Comprobante'
    )

    # Información adicional del gasto.
    observaciones = models.TextField(
        blank=True,
        verbose_name='Observaciones'
    )

    # Fecha de creación del registro.
    fecha_creacion = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f'{self.descripcion} - ${self.monto}'

    class Meta:
        verbose_name = 'Gasto'
        verbose_name_plural = 'Gastos'
        ordering = ['-fecha_gasto']