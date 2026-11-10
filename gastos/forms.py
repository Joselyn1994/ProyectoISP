from django import forms
from .models import Gasto


class GastoForm(forms.ModelForm):

    class Meta:
        model = Gasto

        fields = [
            'categoria',
            'descripcion',
            'monto',
            'fecha_gasto',
            'metodo_pago',
            'comprobante',
            'observaciones',
        ]

        widgets = {
            'categoria': forms.Select(
                attrs={'class': 'form-select'}
            ),
            'descripcion': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ej. Compra de cable de red'
                }
            ),
            'monto': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': '0.00',
                    'step': '0.01',
                    'min': '0.01'
                }
            ),
            'fecha_gasto': forms.DateInput(
                attrs={
                    'class': 'form-control',
                    'type': 'date'
                }
            ),
            'metodo_pago': forms.Select(
                attrs={'class': 'form-select'}
            ),
            'comprobante': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Número de comprobante (opcional)'
                }
            ),
            'observaciones': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 3,
                    'placeholder': 'Detalles adicionales (opcional)'
                }
            ),
        }