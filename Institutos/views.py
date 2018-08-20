from django.conf import settings
from django.shortcuts import render, get_object_or_404, reverse, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.utils import timezone

from django.contrib.auth import views as auth_views
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login

from .models import Instituto, Mensaje, UsuarioLegado
from .forms import SignUpForm

from django.contrib.auth.models import User

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.core.mail import send_mail


from decouple import config
DEBUG = config('DEBUG', cast=bool)

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

def registro(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            auth_login(request, user)
            i = Instituto(usuario=user) #, otro=request.POST['nombre'], fecha=timezone.now())
            #m.telefono = request.POST['telefono']
            i.save()
            return redirect('on_login')
    else:
        form = SignUpForm()
    return render(request, 'registration/registro.html', {'form': form})

@login_required(login_url='/login')
def perfil(request):
    if request.user.is_staff:
        return HttpResponseRedirect(reverse('admin:index'))
    instituto = Instituto.objects.get(usuario=request.user)
    return render(request, 'Institutos/perfil.html', {'instituto': instituto, 'api_key': settings.MAPS_API_KEY})

def buscar(request):
    lat = float(request.GET['lat'])
    lng = float(request.GET['lng'])
    page = int(request.GET.get('page', 1))
    #institutos = list(Instituto.objects.filter(test_id__in=test_ids)[:10])

    posicionados = list(Instituto.objects.filter(posicionamiento__gt=0))
    #map(lambda instituto: instituto.distancia(lat, lng), posicionados)
    for i in posicionados:
        i.distancia(lat, lng)
    #posicionados.sort(key=lambda instituto: instituto.distancia(lat, lng))
    posicionados = list(filter(lambda i: i.ultima_distancia <= 1, posicionados))
    #posicionados = posicionados.filter(ultima_distancia__lte=1)
    posicionados.sort(key=lambda instituto: instituto.ultima_distancia)
    posicionados.sort(key=lambda instituto: instituto.posicionamiento, reverse=True)
    
    organicos = list(Instituto.objects.filter(posicionamiento=0))
    #map(lambda instituto: instituto.distancia(lat, lng), organicos)
    for i in organicos:
        i.distancia(lat, lng)
    # El filtro de radio de 1 km no aplica a los resultados organicos - 30/07/18
    #organicos = list(filter(lambda i: i.ultima_distancia <= 1, organicos))
    organicos.sort(key=lambda instituto: instituto.ultima_distancia)

    institutos = posicionados + organicos
    
    paginator = Paginator(institutos, 10)
    
    # Calculo la pagina actual
    institutos = institutos[(page-1)*10:page*10]
    try:
        inst_page = paginator.page(page)
    except PageNotAnInteger:
        inst_page = paginator.page(1)
    except EmptyPage:
        inst_page = paginator.page(paginator.num_pages)
    if (DEBUG):
        return render(request, 'Institutos/Institutos_debug.html', {'institutos': institutos, 'pager': inst_page, 'lat': lat, 'lng': lng})
    else:
        return render(request, 'Institutos/Institutos.html', {'institutos': institutos, 'pager': inst_page, 'lat': lat, 'lng': lng})

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

def prueba_correo(request):
    send_mail(request.GET['asunto'], request.GET['mensaje'], 'prueba@tuprofe.com.uy', [request.GET['email'], ])
    return render(request, 'Institutos/Sobre-Nosotros.html')


### Admin site requests
def mensajes(request):
    mensajes = list(Mensaje.objects.filter(leido=False).filter(instituto=None))
    return render(request, 'admin/mensajes.html', {'mensajes': mensajes})

def leidos(request):
    mensajes = list(Mensaje.objects.filter(leido=True).filter(instituto=None))
    return render(request, 'admin/leidos.html', {'mensajes': mensajes})

def marcar_leido(request, mensaje_id):
    m = get_object_or_404(Mensaje, pk=mensaje_id)
    m.leido = True
    m.save()
    return HttpResponseRedirect(reverse('mensajes'))

def mandar_link(request, mensaje_id):
    m = get_object_or_404(Mensaje, pk=mensaje_id)
    m.update_hash()
    send_mail('Verificación de Correo', \
        'Por favor ingrese al siguiente enlace para verificar su dirección de correo: http://127.0.0.1:8000/Activar/' + m.hash_id + '/', \
        'prueba@tuprofe.com.uy', [m.email, ])
    m.linkEnviado = True
    m.save()
    return HttpResponseRedirect(reverse('leidos'))

def activar(request, hash_id):
    m = list(Mensaje.objects.filter(hash_id=hash_id))[0]
    m.emailVerificado = True
    m.save()
    return HttpResponseRedirect(reverse('registro'))
