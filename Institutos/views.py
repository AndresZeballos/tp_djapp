from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from . import models

# Create your views here.

def index(request):
    return HttpResponse("Página principal del sitio")

def on_login(request):
    if request.user.is_authenticated:
        if request.user.is_staff:
            return HttpResponseRedirect(reverse('admin:index'))
        else:
            return HttpResponseRedirect(reverse('perfil'))
    else:
        return HttpResponseRedirect(reverse('login'))

@login_required(login_url='/login')
def perfil(request):
    if request.user.is_staff:
        return HttpResponseRedirect(reverse('admin:index'))
    return render(request, 'Institutos/perfil.html')

def buscar(request):
    return render(request, 'Institutos/Institutos.html', {'list': models.Instituto.objects.all()})