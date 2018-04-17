from django.db import models

class Facilidad(models.Model):
    nombre = models.CharField(max_length=200)
    
class FormaPago(models.Model):
    nombre = models.CharField(max_length=200)
    
class Comodidad(models.Model):
    nombre = models.CharField(max_length=200)
    
class RedSocial(models.Model):
    nombre = models.CharField(max_length=200)
    
class Motivo(models.Model):
    nombre = models.CharField(max_length=200)

class Barrio(models.Model):
    nombre = models.CharField(max_length=200)
    
class Centro(models.Model):
    nombre = models.CharField(max_length=200)

class Materia(models.Model):
    nombre = models.CharField(max_length=200)
    centro = models.ForeignKey(Centro, on_delete=models.PROTECT)

class Instituto(models.Model):
    facilidades = models.ManyToManyField(Facilidad)
    formasPago = models.ManyToManyField(FormaPago)
    comodidades = models.ManyToManyField(Comodidad)
    barrios = models.ManyToManyField(Barrio)
    facilidades = models.ManyToManyField(Facilidad)
    centros = models.ManyToManyField(Centro)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

class Profesor(models.Model):
    nombre = models.CharField(max_length=200)
    instituto = models.ForeignKey(Instituto, on_delete=models.PROTECT)

class Enlace(models.Model):
    instituto = models.OneToOneField(Instituto, on_delete=models.PROTECT)
    redSocial = models.OneToOneField(RedSocial, on_delete=models.PROTECT)
    link = models.CharField(max_length=200)
    
    class Meta:
        unique_together = (('instituto', 'redSocial'),)


class Transporte(models.Model):
    distancia = models.IntegerField(default=0)
    lineas = models.CharField(max_length=200)
    instituto = models.ForeignKey(Instituto, on_delete=models.PROTECT)
    
class Mensajes(models.Model):
    fecha = models.DateTimeField()
    nombre = models.CharField(max_length=200)
    telefono = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    mensaje = models.CharField(max_length=4000)
    motivo = models.ForeignKey(Motivo, on_delete=models.PROTECT)
    instituto = models.ForeignKey(Instituto, on_delete=models.PROTECT, null=True)
    centro = models.ForeignKey(Centro, on_delete=models.PROTECT, null=True)
    