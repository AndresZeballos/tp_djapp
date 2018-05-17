from django.shortcuts import render, get_object_or_404, reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.utils import timezone

from .models import Instituto, Mensaje

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
    institutos = Instituto.objects.order_by('-posicionamiento')[:5]
    return render(request, 'Institutos/Institutos.html', {'institutos_list': institutos})

def instituto(request, instituto_id):
    instituto = get_object_or_404(Instituto, pk=instituto_id)
    return render(request, 'Institutos/Instituto.html', {'instituto': instituto})

def nuevo_mensaje(request, instituto_id):
    instituto = get_object_or_404(Instituto, pk=instituto_id)
    m = Mensaje(nombre=request.POST['nombre'], fecha=timezone.now())
    m.telefono = ""
    m.email = ""
    m.mensaje = ""
    m.instituto = instituto
    m.save()
    return HttpResponseRedirect(reverse('perfil', args=(instituto.id,)))