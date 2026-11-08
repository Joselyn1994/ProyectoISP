
# Importamos los modelos de Django.
from django.db import models

# Importamos el modelo de contratos.
from contratos.models import Contrato


class Pago(models.Model):

    # Estados disponibles para cada mensualidad.
    ESTADOS = [
        ('pendiente', 'Pendiente'),
        ('pagado', 'Pagado'),
    ]

    # Métodos disponibles para realizar un pago.
    METODOS_PAGO = [
        ('efectivo', 'Efectivo'),
        ('transferencia', 'Transferencia'),
        ('deposito', 'Depósito'),
        ('otro', 'Otro'),
    ]

    # Contrato al que pertenece esta mensualidad.
    contrato = models.ForeignKey(
        Contrato,
        on_delete=models.PROTECT,
        related_name='pagos',
        verbose_name='Contrato'
    )

    # Mes al que corresponde el pago.
    mes_referencia = models.DateField(
        verbose_name='Mes de referencia'
    )

    # Fecha límite para realizar el pago.
    fecha_vencimiento = models.DateField(
        verbose_name='Fecha de vencimiento'
    )

    # Fecha en que el cliente realizó el pago.
    fecha_pago = models.DateField(
        null=True,
        blank=True,
        verbose_name='Fecha de pago'
    )

    # Valor cobrado en esta mensualidad.
    valor = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        verbose_name='Valor del pago'
    )

    # Método utilizado por el cliente.
    metodo_pago = models.CharField(
        max_length=20,
        choices=METODOS_PAGO,
        blank=True,
        default='',
        verbose_name='Método de pago'
    )

    # Estado actual de la mensualidad.
    estado = models.CharField(
        max_length=15,
        choices=ESTADOS,
        default='pendiente',
        verbose_name='Estado'
    )

    # Observaciones adicionales.
    observaciones = models.TextField(
        blank=True,
        verbose_name='Observaciones'
    )

    # Fecha de creación del registro.
    fecha_creacion = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f'{self.contrato.codigo} - {self.mes_referencia:%m/%Y}'

    class Meta:
        verbose_name = 'Pago'
        verbose_name_plural = 'Pagos'
        ordering = ['-mes_referencia']

        # Evitamos registrar dos mensualidades
        # para el mismo contrato y mes.
        constraints = [
            models.UniqueConstraint(
                fields=['contrato', 'mes_referencia'],
                name='unique_pago_contrato_mes'
            )
        ]
