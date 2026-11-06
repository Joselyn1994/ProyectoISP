
from django import forms
from .models import PlanInternet


class PlanInternetForm(forms.ModelForm):

    class Meta:
        model = PlanInternet

        # Campos que aparecerán en el formulario.
        fields = [
            'nombre',
            'velocidad',
            'precio_mensual',
            'descripcion',
            'estado',
        ]

        # Etiquetas y ayudas para el usuario.
        labels = {
            'nombre': 'Nombre del plan',
            'velocidad': 'Velocidad (Mbps)',
            'precio_mensual': 'Precio mensual ($)',
            'descripcion': 'Descripción del plan',
            'estado': 'Estado del plan',
        }

        # Personalizamos los campos.
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej. Plan Básico',
            }),
            'velocidad': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej. 50',
                'min': '1',
            }),
            'precio_mensual': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej. 20.00',
                'min': '0.01',
                'step': '0.01',
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Describe las características del plan...',
            }),
            'estado': forms.Select(attrs={
                'class': 'form-select',
            }),
        }
