
from django.db import models

# Importamos los modelos de clientes y planes.
from clientes.models import Cliente
from planes.models import PlanInternet


class Contrato(models.Model):

    # Estados disponibles para el contrato.
    ESTADOS = [
        ('activo', 'Activo'),
        ('suspendido', 'Suspendido'),
        ('finalizado', 'Finalizado'),
    ]

    # Código único del contrato.
    codigo = models.CharField(
        max_length=20,
        unique=True,
        verbose_name='Código del contrato'
    )

    # Cliente que contrata el servicio.
    cliente = models.ForeignKey(
        Cliente,
        on_delete=models.PROTECT,
        related_name='contratos',
        verbose_name='Cliente'
    )

    # Plan de Internet contratado.
    plan = models.ForeignKey(
        PlanInternet,
        on_delete=models.PROTECT,
        related_name='contratos',
        verbose_name='Plan de Internet'
    )

    # Fecha de inicio del servicio.
    fecha_inicio = models.DateField(
        verbose_name='Fecha de inicio'
    )

    # Fecha de finalización (opcional).
    fecha_fin = models.DateField(
        null=True,
        blank=True,
        verbose_name='Fecha de finalización'
    )

    # Estado actual del contrato.
    estado = models.CharField(
        max_length=15,
        choices=ESTADOS,
        default='activo',
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
        return f'{self.codigo} - {self.cliente}'

    class Meta:
        verbose_name = 'Contrato'
        verbose_name_plural = 'Contratos'
        ordering = ['-fecha_creacion']
