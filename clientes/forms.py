
# Importamos forms para trabajar con formularios de Django.
from django import forms

# Importamos ValidationError para mostrar mensajes personalizados.
from django.core.exceptions import ValidationError

# Importamos los modelos necesarios para el formulario.
from .models import Cliente, Provincia, Canton, Parroquia


# Creamos el formulario basado en el modelo Cliente.
class ClienteForm(forms.ModelForm):

    # Campo para seleccionar una provincia desde PostgreSQL.
    provincia_geo = forms.ModelChoiceField(
        queryset=Provincia.objects.none(),
        label='Provincia',
        empty_label='Seleccione una provincia',
        widget=forms.Select(attrs={
            'class': 'form-select',
            'id': 'id_provincia_geo',
        })
    )

    # Campo para seleccionar un cantón.
    canton_geo = forms.ModelChoiceField(
        queryset=Canton.objects.none(),
        label='Cantón',
        empty_label='Seleccione un cantón',
        widget=forms.Select(attrs={
            'class': 'form-select',
            'id': 'id_canton_geo',
        })
    )

    # Campo para seleccionar una parroquia.
    parroquia = forms.ModelChoiceField(
        queryset=Parroquia.objects.none(),
        label='Parroquia',
        empty_label='Seleccione una parroquia',
        widget=forms.Select(attrs={
            'class': 'form-select',
            'id': 'id_parroquia',
        })
    )

    # Configuramos los campos del formulario.
    class Meta:

        # Indicamos que utilizaremos el modelo Cliente.
        model = Cliente

        # Seleccionamos los campos que aparecerán.
        fields = [
            'cedula',
            'nombres',
            'apellidos',
            'telefono',
            'correo',
            'provincia_geo',
            'canton_geo',
            'parroquia',
            'sector',
            'direccion',
            'estado',
        ]

        # Personalizamos la apariencia de los campos.
        widgets = {

            # Aplicamos clases de Bootstrap a los campos de texto.
            'cedula': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese la cédula',
            }),

            'nombres': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese los nombres',
            }),

            'apellidos': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese los apellidos',
            }),

            'telefono': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese el teléfono',
            }),

            'correo': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese el correo electrónico',
            }),

            # El sector se escribe manualmente.
            'sector': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese el barrio o sector',
            }),

            # Reducimos la altura del campo de dirección.
            'direccion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Ingrese la dirección domiciliaria',
            }),

            # Aplicamos Bootstrap al estado del cliente.
            'estado': forms.Select(attrs={
                'class': 'form-select',
            }),
        }

    # Configuramos las consultas cuando se crea el formulario.
    def __init__(self, *args, **kwargs):

        # Ejecutamos la configuración original de ModelForm.
        super().__init__(*args, **kwargs)

        # Mostramos solamente las 24 provincias oficiales.
        self.fields['provincia_geo'].queryset = (
            Provincia.objects.exclude(codigo='90').order_by('nombre')
        )

        # Obtenemos la provincia seleccionada.
        provincia_id = self.data.get('provincia_geo')

        # Si estamos editando un cliente, recuperamos su provincia.
        if not provincia_id and self.instance.pk:
            if self.instance.provincia_geo_id:
                provincia_id = self.instance.provincia_geo_id

        # Cargamos únicamente los cantones de esa provincia.
        if provincia_id:
            self.fields['canton_geo'].queryset = Canton.objects.filter(
                provincia_id=provincia_id
            ).order_by('nombre')

        # Obtenemos el cantón seleccionado.
        canton_id = self.data.get('canton_geo')

        # Si estamos editando un cliente, recuperamos su cantón.
        if not canton_id and self.instance.pk:
            if self.instance.canton_geo_id:
                canton_id = self.instance.canton_geo_id

        # Cargamos únicamente las parroquias de ese cantón.
        if canton_id:
            self.fields['parroquia'].queryset = Parroquia.objects.filter(
                canton_id=canton_id
            ).order_by('nombre')

    # Comprobamos que las selecciones geográficas sean coherentes.
    def clean(self):

        # Ejecutamos las validaciones originales del formulario.
        datos = super().clean()

        # Recuperamos los valores seleccionados.
        provincia = datos.get('provincia_geo')
        canton = datos.get('canton_geo')
        parroquia = datos.get('parroquia')

        # Comprobamos que el cantón pertenezca a la provincia.
        if provincia and canton:
            if canton.provincia_id != provincia.id:
                self.add_error(
                    'canton_geo',
                    'El cantón no pertenece a la provincia seleccionada.'
                )

        # Comprobamos que la parroquia pertenezca al cantón.
        if canton and parroquia:
            if parroquia.canton_id != canton.id:
                self.add_error(
                    'parroquia',
                    'La parroquia no pertenece al cantón seleccionado.'
                )

        # Devolvemos los datos validados.
        return datos

    # Validamos que la cédula no esté registrada anteriormente.
    def clean_cedula(self):

        # Recuperamos la cédula ingresada.
        cedula = self.cleaned_data.get('cedula')

        # Buscamos si existe otro cliente con la misma cédula.
        cliente_existente = Cliente.objects.filter(
            cedula=cedula
        ).exclude(
            pk=self.instance.pk
        ).exists()

        # Si existe, mostramos un mensaje en español.
        if cliente_existente:
            raise ValidationError(
                'Esta cédula ya se encuentra registrada.'
            )

        # Devolvemos la cédula validada.
        return cedula

    # Guardamos también los nombres en los campos antiguos del modelo.
    def save(self, commit=True):

        # Obtenemos la instancia sin guardarla todavía.
        cliente = super().save(commit=False)

        # Recuperamos la provincia seleccionada.
        provincia = self.cleaned_data.get('provincia_geo')

        # Recuperamos el cantón seleccionado.
        canton = self.cleaned_data.get('canton_geo')

        # Copiamos los nombres a los campos de texto existentes.
        if provincia:
            cliente.provincia = provincia.nombre

        if canton:
            cliente.canton = canton.nombre

        # Guardamos el cliente si commit es verdadero.
        if commit:
            cliente.save()

            # Guardamos las relaciones adicionales si existen.
            self.save_m2m()

        # Devolvemos el cliente.
        return cliente

