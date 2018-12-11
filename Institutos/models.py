from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
import hashlib
import math

class UsuarioLegado(models.Model):
    username = models.CharField(max_length=30)
    email = models.CharField(max_length=50, null=True)
    password = models.CharField(max_length=32, null=True)
    activo = models.BooleanField(default=False)

    def __str__(self):
        return "%s - %s" % (self.username, self.email)

    def check_password(self, password):
        m = hashlib.md5()
        m.update(password.encode('utf-8'))
        return self.password==m.hexdigest()

    def is_active(self):
        return self.activo
    
class Facilidad(models.Model):
    nombre = models.CharField(max_length=50)

    def __str__(self):
        return "%s" % (self.nombre)
    
class FormaPago(models.Model):
    nombre = models.CharField(max_length=50)

    def __str__(self):
        return "%s" % (self.nombre)
    
class Comodidad(models.Model):
    nombre = models.CharField(max_length=50)

    def __str__(self):
        return "%s" % (self.nombre)
    
class RedSocial(models.Model):
    nombre = models.CharField(max_length=50)

    def __str__(self):
        return "%s" % (self.nombre)
    
class Motivo(models.Model):
    nombre = models.CharField(max_length=50)

    def __str__(self):
        return "%s" % (self.nombre)

class Barrio(models.Model):
    nombre = models.CharField(max_length=50)

    def __str__(self):
        return "%s" % (self.nombre)
    
class Centro(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return "%s" % (self.nombre)

class Materia(models.Model):
    nombre = models.CharField(max_length=50)
    centro = models.ForeignKey(Centro, on_delete=models.PROTECT)

    def __str__(self):
        return "%s - %s" % (self.centro, self.nombre)

class Instituto(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.PROTECT)
    estado = models.IntegerField(default=0, null=True)
    hash_id = models.CharField(max_length=32, null=True)
    referencia = models.IntegerField(default=0, null=True)
    logo =  models.ImageField(upload_to='images/profile_pics/', default = 'images/profile_pics/blank-profile.jpg')
    nombre = models.CharField(max_length=50, default='')
    subtitulo = models.CharField(max_length=100, default='')
    descripcion = models.CharField(max_length=200, default='')
    descripcion_corta = models.CharField(max_length=200, default='')
    telefono = models.CharField(max_length=20, null=True)
    celular = models.CharField(max_length=20, null=True)
    direccion = models.CharField(max_length=100, default='', null=True)
    ciudad = models.CharField(max_length=50, default='Montevideo')
    departamento = models.CharField(max_length=50, default='Montevideo')
    pais = models.CharField(max_length=50, default='Uruguay')
    latitud = models.FloatField(default=0)
    longitud = models.FloatField(default=0)
    creado = models.DateTimeField(default=datetime.now, null=True)
    modificado = models.DateTimeField(default=datetime.now, null=True)
    posicionamiento = models.IntegerField(default=0)
    esDestacado = models.NullBooleanField(default=False)
    facilidades = models.ManyToManyField(Facilidad)
    formasPago = models.ManyToManyField(FormaPago)
    comodidades = models.ManyToManyField(Comodidad)
    barrios = models.ManyToManyField(Barrio)
    centros = models.ManyToManyField(Centro)
    materias = models.ManyToManyField(Materia)
    ultima_distancia = 0

    def distancia(self, lat, lng):
        radius = 6371 # km
        dlat = math.radians(lat-self.latitud)
        dlon = math.radians(lng-self.longitud)
        a = math.sin(dlat/2) * math.sin(dlat/2) + math.cos(math.radians(self.latitud)) \
            * math.cos(math.radians(lat)) * math.sin(dlon/2) * math.sin(dlon/2)
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
        d = radius * c
        self.ultima_distancia = d
        return d

    def updateRelation(self, attribute, ids):
        elems = attribute.all()
        for e in elems:
            attribute.remove(e)
        for i in ids.all():
            attribute.add(i)

    def update_hash(self):
        m = hashlib.md5()
        m.update(self.nombre.encode('utf-8'))
        self.hash_id = m.hexdigest()

    def __str__(self):
        return "%s - %s" % (self.id, self.nombre)

class Profesor(models.Model):
    nombre = models.CharField(max_length=200)
    instituto = models.ForeignKey(Instituto, on_delete=models.PROTECT)

    def __str__(self):
        return "%s - %s" % (self.instituto, self.nombre)

class Enlace(models.Model):
    instituto = models.ForeignKey(Instituto, on_delete=models.PROTECT)
    redSocial = models.ForeignKey(RedSocial, on_delete=models.PROTECT)
    link = models.CharField(max_length=200)
    
    def __str__(self):
        return "%s - %s" % (self.instituto, self.redSocial)

class Transporte(models.Model):
    distancia = models.IntegerField(default=0)
    lineas = models.CharField(max_length=200)
    instituto = models.ForeignKey(Instituto, on_delete=models.PROTECT)

    def __str__(self):
        return "%s - %s" % (self.instituto, self.lineas)
    
class Mensaje(models.Model):
    fecha = models.DateTimeField()
    nombre = models.CharField(max_length=200)
    telefono = models.CharField(max_length=20)
    email = models.CharField(max_length=100)
    asunto = models.CharField(max_length=200, null=True)
    mensaje = models.CharField(max_length=4000)
    motivo = models.ForeignKey(Motivo, on_delete=models.PROTECT, blank=True, null=True)
    instituto = models.ForeignKey(Instituto, on_delete=models.PROTECT, blank=True, null=True)
    centro = models.ForeignKey(Centro, on_delete=models.PROTECT, blank=True, null=True)
    leido = models.BooleanField(default=False)
    linkEnviado = models.BooleanField(default=False)
    emailVerificado = models.BooleanField(default=False)

    def __str__(self):
        return "%s - %s" % (self.fecha, self.nombre)


class Calle(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre
        
class Omnibus(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

class Parada(models.Model):
    latitud = models.FloatField(default=0)
    longitud = models.FloatField(default=0)
    calle = models.ForeignKey(Calle, on_delete=models.PROTECT, related_name='calle')
    esquina = models.ForeignKey(Calle, on_delete=models.PROTECT, related_name='esquina')
    lineas = models.ManyToManyField(Omnibus)

    def __str__(self):
        return "%s - %s - %s" % (self.id, self.calle, self.esquina)
        
