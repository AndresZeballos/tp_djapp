from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required

# Create your views here.

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

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
    return render(request, 'Institutos/perfil.html')