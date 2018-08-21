from django.conf import settings
from django.shortcuts import render, get_object_or_404, reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.utils import timezone

from django.contrib.auth import views as auth_views
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate

from .models import Instituto, Mensaje, UsuarioLegado
from django.contrib.auth.models import User

def index(request):
    return render(request, 'Institutos/Index.html')

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        legado = UsuarioLegado.objects.filter(username=username).first()
        user = User.objects.filter(username=username).first()
        if legado == None:
            return auth_views.login(request)
        if legado != None and legado.is_active() and legado.check_password(password):
            user.set_password(password)
            user.is_active = True
            user.save()
            return auth_views.login(request)
        form = AuthenticationForm()
        return render(request, 'registration/login.html', {'form': form})
    else:
        form = AuthenticationForm()
        return render(request, 'registration/login.html', {'form': form})

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
    instituto = Instituto.objects.get(usuario=request.user)
    return render(request, 'Institutos/perfil.html', {'instituto': instituto, 'api_key': settings.MAPS_API_KEY})

def buscar(request):
    institutos = Instituto.objects.order_by('-posicionamiento')[:5]
    return render(request, 'Institutos/Institutos.html', {'institutos_list': institutos})

def instituto(request, instituto_id):
    instituto = get_object_or_404(Instituto, pk=instituto_id)
    return render(request, 'Institutos/Instituto.html', {'instituto': instituto, 'api_key': settings.MAPS_API_KEY})

def nuevo_mensaje(request, instituto_id):
    m = Mensaje(nombre=request.POST['nombre'], fecha=timezone.now())
    m.telefono = request.POST['telefono']
    m.email = request.POST['email']
    m.mensaje = request.POST['mensaje']
    if instituto_id != 0:
        instituto = get_object_or_404(Instituto, pk=instituto_id)
        m.instituto = instituto
    m.save()
    if instituto_id != 0:
        return HttpResponseRedirect(reverse('instituto', args=(instituto.id,)))
    else:
        return HttpResponseRedirect(reverse('contacto'))
    
def contacto(request):
    return render(request, 'Institutos/Contacto.html')

def sobre_nosotros(request):
    return render(request, 'Institutos/Sobre-Nosotros.html')
