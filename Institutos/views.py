from django.shortcuts import render
from django.http import HttpResponse

from .models import Instituto

# Create your views here.

def index(request):
    return HttpResponse("Hola mundo! Este será la página de bienvenida al sitio")

    
def buscar(request):
    institutos = Instituto.objects.order_by('-posicionamiento')[:5]
    output = ', '.join([i.nombre for i in institutos])
    return HttpResponse(output)

