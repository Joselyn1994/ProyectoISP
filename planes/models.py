

from django.db import models
from django.db import models


class PlanInternet(models.Model):

    # Estados disponibles para cada plan.
    ESTADOS = [
        ('activo', 'Activo'),
        ('inactivo', 'Inactivo'),
    ]

    # Nombre del plan de Internet.
    nombre = models.CharField(
        max_length=100,
        unique=True,
        verbose_name='Nombre del plan'
    )

    # Velocidad de Internet en Mbps.
    velocidad = models.PositiveIntegerField(
        verbose_name='Velocidad (Mbps)'
    )

    # Precio mensual del plan.
    precio_mensual = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        verbose_name='Precio mensual'
    )

    # Descripción del servicio.
    descripcion = models.TextField(
        blank=True,
        verbose_name='Descripción'
    )

    # Estado del plan.
    estado = models.CharField(
        max_length=10,
        choices=ESTADOS,
        default='activo'
    )

    # Fecha de creación.
    fecha_creacion = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f'{self.nombre} - {self.velocidad} Mbps'

    class Meta:
        verbose_name = 'Plan de Internet'
        verbose_name_plural = 'Planes de Internet'
        ordering = ['precio_mensual']
