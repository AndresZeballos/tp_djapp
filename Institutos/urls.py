from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('Ingresar/', views.login, name='ingresar'),
    path('on_login', views.on_login, name='on_login'),
    path('Registro', views.registro, name='registro'),
    path('Perfil', views.perfil, name='perfil'),
    path('Buscar', views.buscar, name='buscar'),
    path('Instituto/<int:instituto_id>/', views.instituto, name='instituto'),
    path('Instituto/<int:instituto_id>/Nuevo-Mensaje', views.nuevo_mensaje, name='nuevo_mensaje'),
    path('Contacto', views.contacto, name='contacto'),
    path('Sobre-Nosotros', views.sobre_nosotros, name='sobre_nosotros'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)