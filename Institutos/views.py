from django.conf import settings
from django.shortcuts import render, get_object_or_404, reverse, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.core.validators import validate_email

from django.contrib.auth import views as auth_views
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login

from .models import Instituto, Mensaje, UsuarioLegado, Centro, Materia, Parada, Omnibus, Comodidad, Facilidad, FormaPago, Profesor
from .forms import SignUpForm, PerfilForm, ImageForm

from django.contrib.auth.models import User

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.core.mail import send_mail, EmailMessage

import urllib.request
from urllib.parse   import urlencode
import json

from decouple import config
DEBUG = config('DEBUG', cast=bool)
MAPS_API_KEY = config('MAPS_API_KEY')
DOMAIN = config('DOMAIN')

EMAIL_HOST_USER = config('EMAIL_ACCOUNT')
CONTACT_EMAIL = config('CONTACT_EMAIL')

def index(request):
    centros = list(Centro.objects.all())
    materias = list(Materia.objects.all())
    return render(request, 'Institutos/Index.html', {'centros': centros, 'materias': materias, 'api_key': MAPS_API_KEY})

def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request.POST)
        username = request.POST['username']
        password = request.POST['password']
        legado = UsuarioLegado.objects.filter(username=username).first()
        user = User.objects.filter(username=username).first()
        if DEBUG:
            print(legado)
            if legado != None:
                print(legado.migrado)
                print(legado.is_active())
                print(legado.check_password(password))
            print(user)
        if legado == None or (legado is not None and legado.migrado):
            # Si es un usuario nuevo, realizo el login
            # Si es un usuario ya migrado, realizo el login
            user = authenticate(username=username, password=password)
            if user is not None and user.is_active:
                auth_login(request, user)
                return on_login(request)
            else:
                return render(request, 'registration/login.html', {'form': form, 'error': 'Usuario o contraseña no válidos'})
        if legado is not None and not legado.migrado:
            # Si es un usuario migrado, activo el usuario y seteo la password
            if legado.check_password(password) and legado.is_active() :
                user.set_password(password)
                user.is_active = True
                user.save()
                legado.migrado = True
                legado.save()
                user = authenticate(username=username, password=password)
                if user is not None and user.is_active:
                    auth_login(request, user)
                    return on_login(request)
                else:
                    return render(request, 'registration/login.html', {'form': form, 'error': 'Usuario o contraseña no válidos'})
            else:
                return render(request, 'registration/login.html', {'form': form, 'error': 'Usuario o contraseña no válidos'})
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

def password_reset(request):
    if request.method == 'POST':
        username = request.POST['username']
        user = User.objects.filter(username=username).first()
        if user != None:
            i = Instituto.objects.get(usuario=user)
            if i != None:
                i.update_hash_pass()
                i.save()
                mensaje = 'Por favor ingrese al siguiente enlace para resetear la contraseña: http://' + DOMAIN + '/Recuperar/' + i.hash_id + '/'
                email = EmailMessage('Recuperar contraseña', mensaje, EMAIL_HOST_USER, [user.email, ], [CONTACT_EMAIL], reply_to=[user.email],)
                email.send()
        return render(request, 'Institutos/Mensaje.html', {'instituto_id': 0, 'titulo': 'Resetear Contraseña', 'mensaje': 'Se ha enviado un correo para resetear la contraseña', 'volver': True})
    return render(request, 'Institutos/Contrasena.html')

def password_confirm(request, hash_id):
    lista = list(Instituto.objects.filter(hash_id=hash_id))
    if len(lista) == 0:
        return render(request, 'Institutos/Recuperar.html', {'validlink': False})
    i = lista[0]
    
    if request.method == 'POST':
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        # Seteear la pass
        if i != None:
            i.usuario.set_password(password1)
            i.usuario.save()
            i.update_hash_pass()
            i.save()
            return render(request, 'Institutos/Mensaje.html', {'instituto_id': 0, 'titulo': 'Se recuperó la contraseña', 'mensaje': 'Se recuperó la contraseña', 'volver': True})
    return render(request, 'Institutos/Recuperar.html', {'validlink': True, 'hash_id': hash_id})

def registro(request):
    form = SignUpForm()
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = User.objects.create_user(username=username, email=username, password=raw_password)
            #auth_login(request, user)
            i = Instituto(usuario=user) 
            i.nombre = request.POST['name']
            i.telefono = request.POST['cellphone']
            
            i.update_hash()
            i.save()

            mensaje = 'Por favor ingrese al siguiente enlace para verificar su dirección de correo: http://' + DOMAIN + '/Activar/' + i.hash_id + '/'
            email = EmailMessage('Verificación de Correo', mensaje, EMAIL_HOST_USER, [user.email, ], [CONTACT_EMAIL], reply_to=[user.email],)
            email.send()
            return render(request, 'Institutos/Mensaje.html', {'instituto_id': 0, 'titulo': 'Registrate', 'mensaje': 'Se ha enviado a su email un correo de verificación de la cuenta', 'volver': True})
        else:
            return render(request, 'registration/registro.html', {'form': form})
    return render(request, 'registration/registro.html', {'form': form})

def activar(request, hash_id):
    m = list(Instituto.objects.filter(estado=0).filter(hash_id=hash_id))[0]
    m.estado = 1
    m.save()
    #form = SignUpForm(initial={'name': m.nombre, 'username': m.email})
    #return render(request, 'registration/registro.html', {'form': form})
    return HttpResponseRedirect(reverse('login'))

@login_required(login_url='/login')
def perfil(request):
    if request.user.is_staff:
        return HttpResponseRedirect(reverse('admin:index'))
    instituto = Instituto.objects.get(usuario=request.user)
    form = PerfilForm(instance=instituto)
    return render(request, 'Institutos/Perfil.html', {'instituto': instituto, 'api_key': settings.MAPS_API_KEY, 'form': form})

@login_required(login_url='/login')
def perfil_edit(request):
    if request.user.is_staff:
        return HttpResponseRedirect(reverse('admin:index'))
    if request.method == 'POST':
        if DEBUG:
            print('request.POST')
            print(request.POST)
            print('request.FILES')
            print(request.FILES)
        form = PerfilForm(request.POST, request.FILES)
        if form.is_valid():
            if DEBUG:
                print('form.cleaned_data')
                print(form.cleaned_data)
            instituto = Instituto.objects.filter(usuario=request.user)
            instituto.update(**{k:form.cleaned_data[k] for k in ('nombre', \
                'descripcion', 'telefono', 'direccion', 'latitud', 'longitud', ) if k in form.cleaned_data})
            if (len(request.FILES) > 0):
                instituto.update(**{k:form.cleaned_data[k] for k in ('logo', ) if k in form.cleaned_data})
            instituto = Instituto.objects.get(usuario=request.user)
            instituto.updateRelation(instituto.centros, form.cleaned_data['centros'])
            instituto.updateRelation(instituto.facilidades, form.cleaned_data['facilidades'])
            instituto.updateRelation(instituto.formasPago, form.cleaned_data['formasPago'])
            instituto.updateRelation(instituto.comodidades, form.cleaned_data['comodidades'])
            instituto.updateRelation(instituto.materias, form.cleaned_data['materias'])
            instituto.save()

            print(len(list(instituto.omnibuses.all())))
            instituto.omnibuses.clear()
            paradas = list(Parada.objects.all())
            for p in paradas:
                parada = get_object_or_404(Parada, pk=p.id)
                instituto.distancia(parada.latitud, parada.longitud)
                if instituto.ultima_distancia <= 0.5:
                    for l in parada.lineas.all():
                        instituto.omnibuses.add(Omnibus.objects.get(id=l.id))
            instituto.save()
            print(len(list(instituto.omnibuses.all())))

            Profesor.objects.filter(instituto=instituto).delete()

            prof_list = [values for key, values in request.POST.lists() if key=='profesores']
            if len(prof_list) > 0:
                profesores = prof_list[0]
                for profe in profesores:
                    p = Profesor(nombre=profe, instituto=instituto)
                    p.save()
            
            form = ImageForm(request.POST, request.FILES)
            try: 
                if form.is_valid():
                    form.save()
                else:
                    print(form.errors)
            except:
                pass
            
        else:
            print(form.errors)

        return HttpResponseRedirect(reverse('perfil'))
    instituto = Instituto.objects.get(usuario=request.user)
    form = PerfilForm(instance=instituto)

    centros = list(Centro.objects.all())
    materias = list(Materia.objects.all())
    comodidades = list(Comodidad.objects.all())
    facilidades = list(Facilidad.objects.all())
    formasPago = list(FormaPago.objects.all())

    return render(request, 'Institutos/Perfil_edit.html', {'instituto': instituto, 'api_key': settings.MAPS_API_KEY, 'form': form, \
        'centros': centros, 'materias': materias, 'comodidades': comodidades, 'facilidades': facilidades, 'formasPago': formasPago, })

def buscar(request):
    centros = list(Centro.objects.all())
    materias = list(Materia.objects.all())

    lat = request.POST.get('lat', "")
    lng = request.POST.get('lng', "")
    if lat == "" or lng == "":
        return HttpResponseRedirect(reverse('index'))
    lat = float(lat)
    lng = float(lng)
    page = int(request.POST.get('page', 1))

    direccion = request.POST.get('dir', "")

    centro = request.POST.get('centro', "")
    materia = request.POST.get('materia', "")

    destacados = list(Instituto.objects.filter(estado=2).filter(esDestacado=True).filter(centros__nombre=centro).filter(materias__nombre=materia).distinct())

    for i in destacados:
        i.distancia(lat, lng)

    posicionados = list(Instituto.objects.filter(estado=2).filter(posicionamiento__gt=0).filter(centros__nombre=centro).filter(materias__nombre=materia).distinct())
    
    for i in posicionados:
        i.distancia(lat, lng)

    posicionados = list(filter(lambda i: i.ultima_distancia <= 1.5, posicionados))
    posicionados.sort(key=lambda instituto: instituto.ultima_distancia)
    posicionados.sort(key=lambda instituto: instituto.posicionamiento, reverse=True)
    
    organicos = list(Instituto.objects.filter(estado=2).filter(posicionamiento=0).filter(centros__nombre=centro).filter(materias__nombre=materia))

    for i in organicos:
        i.distancia(lat, lng)
    # El filtro de radio de 1 km no aplica a los resultados organicos - 30/07/18
    organicos.sort(key=lambda instituto: instituto.ultima_distancia)

    institutos = posicionados + organicos

    print(posicionados)

    flatten = lambda l: list(set([item for sublist in l for item in sublist]))

    comodidades = flatten([list(a.comodidades.all()) for a in institutos])
    formas = flatten([list(a.formasPago.all()) for a in institutos])
    facilidades = flatten([list(a.facilidades.all()) for a in institutos])

    #paginator = Paginator(institutos, 10)
    
    # Calculo la pagina actual
    #institutos = institutos[(page-1)*10:page*10]
    #try:
    #    inst_page = paginator.page(page)
    #except PageNotAnInteger:
    #    inst_page = paginator.page(1)
    #except EmptyPage:
    #    inst_page = paginator.page(paginator.num_pages)

    # , 'pager': inst_page
    #if (DEBUG):
    #    return render(request, 'Institutos/Institutos_debug.html', {'institutos': institutos, 'destacados': destacados, 'direccion': direccion, 'lat': lat, 'lng': lng, 'centro': centro, 'materia': materia, 'api_key': settings.MAPS_API_KEY })
    #else:

    return render(request, 'Institutos/Institutos.html', { \
        'comodidades': comodidades, 'formas': formas, 'facilidades': facilidades, \
        'centros': centros, 'materias': materias, 'institutos': institutos, 'destacados': destacados, \
        'direccion': direccion, 'lat': lat, 'lng': lng, 'centro': centro, 'materia': materia, 'api_key': settings.MAPS_API_KEY, 'searchResponsive': True })

def buscarProfe(request):
    texto = request.POST['texto']
    page = int(request.POST.get('page', 1))

    institutos = list(Instituto.objects.filter(estado=2).filter(nombre__icontains=texto))
    '''
    paginator = Paginator(institutos, 10)
    
    # Calculo la pagina actual
    institutos = institutos[(page-1)*10:page*10]
    try:
        inst_page = paginator.page(page)
    except PageNotAnInteger:
        inst_page = paginator.page(1)
    except EmptyPage:
        inst_page = paginator.page(paginator.num_pages)
    return render(request, 'Institutos/InstitutosSimple.html', {'institutos': institutos, 'pager': inst_page, 'texto': texto})
    '''

    
    flatten = lambda l: list(set([item for sublist in l for item in sublist]))

    comodidades = flatten([list(a.comodidades.all()) for a in institutos])
    formas = flatten([list(a.formasPago.all()) for a in institutos])
    facilidades = flatten([list(a.facilidades.all()) for a in institutos])

    return render(request, 'Institutos/InstitutosSimple.html', {'institutos': institutos, 'texto': texto, \
        'comodidades': comodidades, 'formas': formas, 'facilidades': facilidades, \
        'api_key': settings.MAPS_API_KEY, 'searchResponsive': True })

def instituto(request, instituto_id):
    instituto = get_object_or_404(Instituto, pk=instituto_id)
    return render(request, 'Institutos/Instituto.html', {'instituto': instituto, 'api_key': settings.MAPS_API_KEY})

def contacto(request, instituto_id=0):
    if request.method == 'POST':
        m = Mensaje(nombre=request.POST['nombre'], fecha=timezone.now())
        m.telefono = request.POST['telefono']
        m.email = request.POST['email']
        m.asunto = request.POST['asunto']
        m.mensaje = request.POST['mensaje']
        if instituto_id != 0:
            instituto = get_object_or_404(Instituto, pk=instituto_id)
            m.instituto = instituto
        errores = ""
        if m.nombre.strip() == "":
            errores += "El ingreso del nombre es obligatorio. <br>"
        if m.email.strip() == "":
            errores += "El ingreso del correo electrónico es obligatorio. <br>"
        try:
            validate_email(request.POST['email'])
        except:
            errores += "El correo electrónico ingresado no es válido. <br>"
        if m.mensaje.strip() == "":
            errores += "El ingreso del mensaje es obligatorio. <br>"
        
        if errores == "":
            m.save()
            errores = "El mensaje ha sido enviado correctamente."
            mensaje = 'Contacto: ' + m.telefono + ', ' + m.email + '. Mensaje:' + m.mensaje
            if instituto_id != 0:
                email = EmailMessage(m.asunto, mensaje, EMAIL_HOST_USER, [m.instituto.usuario.email, ], [CONTACT_EMAIL], reply_to=[m.email],)
                email.send()
            else:
                email = EmailMessage(m.asunto, mensaje, EMAIL_HOST_USER, [CONTACT_EMAIL , ], reply_to=[m.email],)
                email.send()
            m = Mensaje()
        else:
            print(errores)

        if instituto_id != 0:
            #return HttpResponseRedirect(reverse('instituto', (instituto.id,), {'mensaje': m, 'errores': errores}))
            return render(request, 'Institutos/Contacto.html', {'instituto_id': instituto_id, 'mensaje': m, 'errores': errores})
        else:
            return render(request, 'Institutos/Contacto.html', {'instituto_id': 0, 'mensaje': m, 'errores': errores})
    return render(request, 'Institutos/Contacto.html', {'instituto_id': instituto_id})

def sobre_nosotros(request):
    return render(request, 'Institutos/Sobre-Nosotros.html')

def prueba_correo(request):
    send_mail(request.GET['asunto'], request.GET['mensaje'], EMAIL_HOST_USER, [request.GET['email'], ])
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

'''
def mandar_link(request, mensaje_id):
    m = get_object_or_404(Mensaje, pk=mensaje_id)
    m.update_hash()
    send_mail('Verificación de Correo', \
        'Por favor ingrese al siguiente enlace para verificar su dirección de correo: http://127.0.0.1:8000/Activar/' + m.hash_id + '/', \
        'prueba@tuprofe.com.uy', [m.email, ])
    m.linkEnviado = True
    m.save()
    return HttpResponseRedirect(reverse('leidos'))
'''



def pendientes(request):
    pendientes = list(Instituto.objects.filter(estado=1))
    return render(request, 'admin/Pendientes.html', {'pendientes': pendientes})

def activos(request):
    activos = list(Instituto.objects.filter(estado=2))
    return render(request, 'admin/Activos.html', {'activos': activos})

def inactivos(request):
    inactivos = list(Instituto.objects.filter(estado=3))
    return render(request, 'admin/Inactivos.html', {'inactivos': inactivos})


def habilitarInstituto(request, id):
    m = get_object_or_404(Instituto, pk=id)
    m.estado = 2
    m.save()
    return HttpResponseRedirect('/admin/')


def deshabilitarInstituto(request, id):
    m = get_object_or_404(Instituto, pk=id)
    m.estado = 3
    m.save()
    return HttpResponseRedirect('/admin/')







def paradasCoords(request):
    paradas = list(Parada.objects.all())#.filter(latitud=0))
    for p in paradas:
        parada = get_object_or_404(Parada, pk=p.id)
        print('---------------------------------------------------------------------')
        try:
            #parada.calle.nombre = ''.join([i if ord(i) < 128 else ' ' for i in parada.calle.nombre])
            #parada.esquina.nombre = ''.join([i if ord(i) < 128 else ' ' for i in parada.esquina.nombre])
            parada.calle.nombre = parada.calle.nombre.replace('Ã‘', 'Ñ').replace('Â´', "'")
            parada.esquina.nombre = parada.esquina.nombre.replace('Ã‘', 'Ñ').replace('Â´', "'")


            d = (parada.calle.nombre + " y " + parada.esquina.nombre).replace(' ', '%2C')
            
            print(d)
            query = dict(key=MAPS_API_KEY, address=d+', montevideo, uruguay')
            print(query)

            #req = urllib.request.Request(('https://maps.googleapis.com/maps/api/geocode/json?key='+MAPS_API_KEY+'&address='+d+',montevideo,uruguay'))
            url = 'https://maps.googleapis.com/maps/api/geocode/json?'+urlencode(query)
            print(url)
            req = urllib.request.Request(url)
        
        
            response = urllib.request.urlopen(req)
            #except Exception as inst:
            #    print (type(inst))     # the exception instanc
            #    print (inst.args )     # arguments stored in .args
            #    print (inst       )
            #if response 
            j = json.loads(response.read())
            print(j)
            parada.latitud = j['results'][0]['geometry']['location']['lat']
            parada.longitud = j['results'][0]['geometry']['location']['lng']
            
            parada.calle.save()
            parada.esquina.save()
            parada.save()
        except Exception as inst:
            print (type(inst))     # the exception instanc
            print (inst.args )     # arguments stored in .args
            print (inst       )
            break

    return render(request, 'admin/paradas.html', {'paradas': paradas})


def cargarParadas(request):
    paradas = list(Parada.objects.all())
    institutos = list(Instituto.objects.filter(estado=2))
    for p in paradas:
        parada = get_object_or_404(Parada, pk=p.id)
        for i in institutos:
            instituto = get_object_or_404(Instituto, pk=i.id)
            print(str(instituto.id) + " - " + str(p.id) + " - " + str((parada.latitud, parada.longitud)))
            instituto.distancia(parada.latitud, parada.longitud)
            if instituto.ultima_distancia <= 0.5:
                for l in parada.lineas.all():
                    instituto.omnibuses.add(Omnibus.objects.get(id=l.id))
                instituto.save()
                print(str(instituto.id) + " - " + str(len(instituto.omnibuses.all())))

    return render(request, 'admin/paradas.html', {'paradas': paradas})

