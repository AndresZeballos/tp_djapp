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
    path('BuscarProfe', views.buscarProfe, name='buscarProfe'),
    path('Instituto/<int:instituto_id>/', views.instituto, name='instituto'),
    path('Instituto/<int:instituto_id>/Nuevo-Mensaje', views.nuevo_mensaje, name='nuevo_mensaje'),
    path('Contacto', views.contacto, name='contacto'),
    path('Quienes-Somos', views.contacto, name='nosotros'),
    path('Sobre-Nosotros', views.sobre_nosotros, name='sobre_nosotros'),
    path('PruebaCorreo', views.prueba_correo, name='prueba_correo'),
    path('admin/mensajes/', views.mensajes, name='mensajes'),
    path('admin/leidos/', views.leidos, name='leidos'),
    path('admin/Pendientes/', views.pendientes, name='pendientes'),
    path('admin/marcarLeido/<int:mensaje_id>/', views.marcar_leido, name='marcar_leido'),
    #path('admin/mandar_link/<int:mensaje_id>/', views.mandar_link, name='mandar_link'),
    path('admin/habilitarInstituto/<int:id>/', views.habilitarInstituto, name='habilitar_instituto'),
    path('Activar/<hash_id>/', views.activar, name='activar'),
    #path('admin/paradasCoords/', views.paradasCoords, name='paradasCoords'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
