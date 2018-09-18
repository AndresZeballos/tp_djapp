from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Instituto

class SignUpForm(UserCreationForm):
    name = forms.CharField(max_length=30, required=False, help_text='Optional.', label='Nombre')
    password1 = forms.CharField(widget=forms.PasswordInput, label='Password')
    password2 = forms.CharField(widget=forms.PasswordInput, label='Confirmar Password')

    class Meta:
        model = User
        fields = ('username', 'name', 'password1', 'password2', )

class PerfilForm(forms.ModelForm):

    class Meta:
        model = Instituto
        fields = ('nombre', 'subtitulo', 'descripcion', 'descripcion_corta', \
            'telefono','celular','direccion','ciudad','departamento', 'centros', \
            'materias', 'facilidades', 'formasPago', 'comodidades', )
            