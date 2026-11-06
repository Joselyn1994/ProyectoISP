

# Importamos los formularios de Django.
from django import forms

# Importamos los modelos necesarios.
from .models import Contrato
from clientes.models import Cliente


# Personalizamos cómo aparecen los clientes en la lista.
class ClienteChoiceField(forms.ModelChoiceField):

    def label_from_instance(self, cliente):

        # Mostramos cédula y nombres completos.
        return (
            f'{cliente.cedula} - '
            f'{cliente.nombres} {cliente.apellidos}'
        )


class ContratoForm(forms.ModelForm):

    # Utilizamos nuestra lista personalizada de clientes.
    cliente = ClienteChoiceField(
        queryset=Cliente.objects.all(),
        widget=forms.Select(attrs={
            'class': 'form-select',
        }),
        label='Seleccionar cliente'
    )

    class Meta:

        # Modelo que utilizará el formulario.
        model = Contrato

        # Campos del contrato.
        fields = [
            'codigo',
            'cliente',
            'plan',
            'fecha_inicio',
            'fecha_fin',
            'estado',
            'observaciones',
        ]

        # Etiquetas de los campos.
        labels = {
            'codigo': 'Código del contrato',
            'plan': 'Seleccionar plan de Internet',
            'fecha_inicio': 'Fecha de inicio',
            'fecha_fin': 'Fecha de finalización',
            'estado': 'Estado del contrato',
            'observaciones': 'Observaciones',
        }

        # Diseño visual de los campos.
        widgets = {

            'codigo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej. CONT-001',
            }),

            'plan': forms.Select(attrs={
                'class': 'form-select',
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

