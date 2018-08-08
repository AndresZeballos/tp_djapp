from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.', label='Nombre')
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.', label='Email')
    password1 = forms.CharField(widget=forms.PasswordInput, label='Password')
    password2 = forms.CharField(widget=forms.PasswordInput, label='Confirmar Password')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'email', 'password1', 'password2', )
