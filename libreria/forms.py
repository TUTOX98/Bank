from django import forms
from django.core.exceptions import ValidationError
from .models import Cliente

from django import forms
from django.core.exceptions import ValidationError
from .models import Cliente

def validate_digits(value):
    if not value.isdigit():
        raise ValidationError('Este campo debe contener solo números.')

def validate_password_length(value):
    if len(value) < 6:
        raise ValidationError('La contraseña debe tener al menos 6 caracteres.')

class ClienteForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Cliente
        fields = ['cedula_cli', 'nombre_cli', 'apellido_cli', 'telefono_cli', 'direccion_cli', 'cod_ciudad', 'password']

    def __init__(self, *args, **kwargs):
        super(ClienteForm, self).__init__(*args, **kwargs)
        self.fields['cedula_cli'].validators.append(validate_digits)
        self.fields['telefono_cli'].validators.append(validate_digits)
        self.fields['password'].validators.append(validate_password_length)
        self.fields['cedula_cli'].label = 'Cédula'
        self.fields['nombre_cli'].label = 'Nombre'
        self.fields['apellido_cli'].label = 'Apellido'
        self.fields['telefono_cli'].label = 'Teléfono'
        self.fields['direccion_cli'].label = 'Dirección'
        self.fields['cod_ciudad'].label = 'Ciudad'
        self.fields['password'].label = 'Contraseña'
