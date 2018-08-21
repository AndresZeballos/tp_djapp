from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
import hashlib

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
    referencia = models.IntegerField(default=0)
    logo =  models.ImageField(upload_to='images/profile_pics/', default = 'images/profile_pics/blank-profile.jpg')
    nombre = models.CharField(max_length=50, default='')
    subtitulo = models.CharField(max_length=100, default='')
    descripcion = models.CharField(max_length=200, default='')
    descripcion_corta = models.CharField(max_length=100, default='')
    telefono = models.CharField(max_length=20, null=True)
    celular = models.CharField(max_length=20, null=True)
    direccion = models.CharField(max_length=100, default='')
    ciudad = models.CharField(max_length=50, default='Montevideo')
    departamento = models.CharField(max_length=50, default='Montevideo')
    pais = models.CharField(max_length=50, default='Uruguay')
    latitud = models.FloatField(default=0)
    longitud = models.FloatField(default=0)
    creado = models.DateTimeField(default=datetime.now, null=True)
    modificado = models.DateTimeField(default=datetime.now, null=True)
    posicionamiento = models.IntegerField(default=0)
    facilidades = models.ManyToManyField(Facilidad)
    formasPago = models.ManyToManyField(FormaPago)
    comodidades = models.ManyToManyField(Comodidad)
    barrios = models.ManyToManyField(Barrio)
    facilidades = models.ManyToManyField(Facilidad)
    centros = models.ManyToManyField(Centro)
    materias = models.ManyToManyField(Materia)

    def __str__(self):
        return "%s" % (self.nombre)

class Profesor(models.Model):
    nombre = models.CharField(max_length=100)
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
    mensaje = models.CharField(max_length=4000)
    motivo = models.ForeignKey(Motivo, on_delete=models.PROTECT, blank=True, null=True)
    instituto = models.ForeignKey(Instituto, on_delete=models.PROTECT, blank=True, null=True)
    centro = models.ForeignKey(Centro, on_delete=models.PROTECT, blank=True, null=True)

    def __str__(self):
        return "%s - %s" % (self.fecha, self.nombre)
    