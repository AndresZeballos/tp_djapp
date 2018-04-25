from django.shortcuts import render, get_object_or_404, reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.utils import timezone

from .models import Instituto, Mensaje

def index(request):
    institutos_list = Instituto.objects.order_by('-posicionamiento')[:5]
    context = { 'institutos_list': institutos_list, }
    return render(request, 'Institutos/index.html', context)
    
def buscar(request):
    institutos = Instituto.objects.order_by('-posicionamiento')[:5]
    output = ', '.join([i.nombre for i in institutos])
    return HttpResponse(output)
    
def perfil(request, instituto_id):
    instituto = get_object_or_404(Instituto, pk=instituto_id)
    return render(request, 'Institutos/perfil.html', {'instituto': instituto})

def nuevo_mensaje(request, instituto_id):
    instituto = get_object_or_404(Instituto, pk=instituto_id)
    m = Mensaje(nombre=request.POST['nombre'], fecha=timezone.now())
    m.telefono = ""
    m.email = ""
    m.mensaje = ""
    m.instituto = instituto
    m.save()
    return HttpResponseRedirect(reverse('perfil', args=(instituto.id,)))
