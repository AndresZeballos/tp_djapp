from django import forms
from django.contrib.auth.models import User
from .models import Instituto

from django.db import models

class Image(models.Model):
    image = models.ImageField(upload_to='profile_pics/')

class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ('image', )

class SignUpForm(forms.Form):
    name = forms.CharField(max_length=30, label='Nombre')
    cellphone = forms.CharField(max_length=30, label='Telefono')
    username = forms.CharField(max_length=254, label='Correo')
    password1 = forms.CharField(widget=forms.PasswordInput, label='Password')
    password2 = forms.CharField(widget=forms.PasswordInput, label='Confirmar Password')

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'name', 'cellphone', )

class PerfilForm(forms.ModelForm):
    email = forms.CharField(max_length=254, label='Correo')

    class Meta:
        model = Instituto
        fields = ('nombre', 'descripcion', 'email', 'logo', \
            'telefono', 'direccion', 'latitud', 'longitud', 'centros', \
            'materias', 'facilidades', 'formasPago', 'comodidades', )

