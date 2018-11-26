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

from .models import Instituto, Mensaje, UsuarioLegado, Centro, Materia, Parada
from .forms import SignUpForm, PerfilForm

from django.contrib.auth.models import User

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.core.mail import send_mail

import urllib.request
from urllib.parse   import urlencode
import json

from decouple import config
DEBUG = config('DEBUG', cast=bool)
MAPS_API_KEY = config('MAPS_API_KEY')

def index(request):
    centros = list(Centro.objects.all())
    materias = list(Materia.objects.all())
    return render(request, 'Institutos/Index.html', {'centros': centros, 'materias': materias})

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
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = User.objects.create_user(username=username, email=username, password=raw_password)
            auth_login(request, user)
            i = Instituto(usuario=user) 
            i.nombre = request.POST['name']
            i.telefono = request.POST['cellphone']
            
            i.update_hash()
            send_mail('Verificación de Correo', \
                'Por favor ingrese al siguiente enlace para verificar su dirección de correo: http://127.0.0.1:8000/Activar/' + i.hash_id + '/', \
                'prueba@tuprofe.com.uy', [username, ])
            i.save()
            return redirect('on_login')
    else:
        form = SignUpForm()
    return render(request, 'registration/registro.html', {'form': form})

@login_required(login_url='/login')
def perfil(request):
    if request.user.is_staff:
        return HttpResponseRedirect(reverse('admin:index'))
    if request.method == 'POST':
        form = PerfilForm(request.POST)
        form.is_valid()
        instituto = Instituto.objects.filter(usuario=request.user)
        instituto.update(**{k:form.cleaned_data[k] for k in ('nombre', \
            'subtitulo', 'descripcion', 'descripcion_corta', 'telefono','celular','direccion','ciudad',) if k in form.cleaned_data})
        instituto = Instituto.objects.get(usuario=request.user)
        instituto.updateRelation(instituto.centros, form.cleaned_data['centros'])
        instituto.updateRelation(instituto.facilidades, form.cleaned_data['facilidades'])
        instituto.updateRelation(instituto.formasPago, form.cleaned_data['formasPago'])
        instituto.updateRelation(instituto.comodidades, form.cleaned_data['comodidades'])
        instituto.updateRelation(instituto.materias, form.cleaned_data['materias'])
        instituto.save()
    instituto = Instituto.objects.get(usuario=request.user)
    form = PerfilForm(instance=instituto)
    return render(request, 'Institutos/perfil.html', {'instituto': instituto, 'api_key': settings.MAPS_API_KEY, 'form': form})

def buscar(request):
    lat = float(request.POST['lat'])
    lng = float(request.POST['lng'])
    page = int(request.POST.get('page', 1))

    centro = request.POST.get('centro', "")
    materia = request.POST.get('materia', "")

    destacados = list(Instituto.objects.filter(esDestacado=True).filter(centros__nombre=centro).filter(materias__nombre=materia))

    posicionados = list(Instituto.objects.filter(posicionamiento__gt=0).filter(centros__nombre=centro).filter(materias__nombre=materia))

    for i in posicionados:
        i.distancia(lat, lng)

    posicionados = list(filter(lambda i: i.ultima_distancia <= 1.5, posicionados))
    posicionados.sort(key=lambda instituto: instituto.ultima_distancia)
    posicionados.sort(key=lambda instituto: instituto.posicionamiento, reverse=True)
    
    organicos = list(Instituto.objects.filter(posicionamiento=0).filter(centros__nombre=centro).filter(materias__nombre=materia))

    for i in organicos:
        i.distancia(lat, lng)
    # El filtro de radio de 1 km no aplica a los resultados organicos - 30/07/18
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
        return render(request, 'Institutos/Institutos_debug.html', {'institutos': institutos, 'destacados': destacados, 'pager': inst_page, 'lat': lat, 'lng': lng, 'centro': centro, 'materia': materia})
    else:
        return render(request, 'Institutos/Institutos.html', {'institutos': institutos, 'destacados': destacados, 'pager': inst_page, 'lat': lat, 'lng': lng, 'centro': centro, 'materia': materia})

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
    m = list(Instituto.objects.filter(hash_id=hash_id))[0]
    m.estado = 1
    m.save()
    #form = SignUpForm(initial={'name': m.nombre, 'username': m.email})
    #return render(request, 'registration/registro.html', {'form': form})
    return HttpResponseRedirect(reverse('login'))

def paradas(request):
    paradas = list(Parada.objects.all())
    return render(request, 'admin/paradas.html', {'paradas': paradas})

def paradasCoords(request):
    paradas = list(Parada.objects.all())
    for p in paradas:
        parada = get_object_or_404(Parada, pk=p.id)
        try:
            #parada.calle.nombre = ''.join([i if ord(i) < 128 else ' ' for i in parada.calle.nombre])
            #parada.esquina.nombre = ''.join([i if ord(i) < 128 else ' ' for i in parada.esquina.nombre])
            parada.calle.nombre = parada.calle.nombre.replace('Ã‘', 'Ñ').replace('Â´', "'")
            parada.esquina.nombre = parada.esquina.nombre.replace('Ã‘', 'Ñ').replace('Â´', "'")


            d = (parada.calle.nombre + " y " + parada.esquina.nombre)#.replace(' ', '+')
            
            print(d)
            query = dict(key=MAPS_API_KEY, address=d+',montevideo,uruguay')

            #req = urllib.request.Request(('https://maps.googleapis.com/maps/api/geocode/json?key='+MAPS_API_KEY+'&address='+d+',montevideo,uruguay'))
            req = urllib.request.Request(('https://maps.googleapis.com/maps/api/geocode/json?'+urlencode(query)))
        
        
            response = urllib.request.urlopen(req)
            print('---------------------------------------------------------------------')
            #except Exception as inst:
            #    print (type(inst))     # the exception instanc
            #    print (inst.args )     # arguments stored in .args
            #    print (inst       )
            #if response 
            j = json.loads(response.read())
            parada.latitud = j['results'][0]['geometry']['location']['lat']
            parada.longitud = j['results'][0]['geometry']['location']['lng']
            
            parada.calle.save()
            parada.esquina.save()
            parada.save()
        except Exception as inst:
            print (type(inst))     # the exception instanc
            print (inst.args )     # arguments stored in .args
            print (inst       )

    return render(request, 'admin/paradas.html', {'paradas': paradas})


