
# Importamos los formularios de Django.
from django import forms

# Importamos los modelos necesarios.
from .models import Contrato
from clientes.models import Cliente
from planes.models import PlanInternet


# Personalizamos cómo aparecen los clientes en la lista.
class ClienteChoiceField(forms.ModelChoiceField):

    def label_from_instance(self, cliente):
        return (
            f'{cliente.cedula} - '
            f'{cliente.nombres} {cliente.apellidos}'
        )


# Personalizamos cómo aparecen los planes en la lista.
class PlanChoiceField(forms.ModelChoiceField):

    def label_from_instance(self, plan):
        return f'{plan.nombre} - {plan.velocidad} Mbps'


class ContratoForm(forms.ModelForm):

    # Lista personalizada de clientes.
    cliente = ClienteChoiceField(
        queryset=Cliente.objects.all(),
        widget=forms.Select(attrs={
            'class': 'form-select',
        }),
        label='Seleccionar cliente'
    )

    # Lista de planes activos.
    plan = PlanChoiceField(
        queryset=PlanInternet.objects.filter(
            estado='activo'
        ).order_by('precio_mensual'),
        widget=forms.Select(attrs={
            'class': 'form-select',
            'id': 'id_plan',
        }),
        label='Seleccionar plan de Internet'
    )

    class Meta:

        model = Contrato

        fields = [
            'codigo',
            'cliente',
            'plan',
            'fecha_inicio',
            'fecha_fin',
            'estado',
            'observaciones',
        ]

        labels = {
            'codigo': 'Código del contrato',
            'plan': 'Seleccionar plan de Internet',
            'fecha_inicio': 'Fecha de inicio',
            'fecha_fin': 'Fecha de finalización',
            'estado': 'Estado del contrato',
            'observaciones': 'Observaciones',
        }

        widgets = {
            'codigo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej. CONT-001',
            }),

            'fecha_inicio': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
            }),

            'fecha_fin': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
            }),

            'estado': forms.Select(attrs={
                'class': 'form-select',
            }),

            'observaciones': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Observaciones del contrato...',
            }),
        }
