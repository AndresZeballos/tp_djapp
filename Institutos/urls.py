from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.index, name='index'),
    path('Ingresar/', views.login, name='ingresar'),
    path('on_login', views.on_login, name='on_login'),
    
    path('RecuperarPassword/', views.password_reset, name='password_reset'),
    path('Recuperar/<hash_id>/', views.password_confirm, name='password_confirm'),
    #path(r'^password_reset/done/$', auth_views.password_reset_done, name='password_reset_done'),
    #path(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', auth_views.password_reset_confirm, name='password_reset_confirm'),
    #path(r'^reset/done/$', auth_views.password_reset_complete, name='password_reset_complete'),

    path('Registro', views.registro, name='registro'),
    path('Perfil', views.perfil, name='perfil'),
    path('Perfil_edit', views.perfil_edit, name='perfil_edit'),
    path('Buscar', views.buscar, name='buscar'),
    path('BuscarProfe', views.buscarProfe, name='buscarProfe'),
    path('Instituto/<int:instituto_id>/', views.instituto, name='instituto'),
    #path('Instituto/<int:instituto_id>/Nuevo-Mensaje', views.nuevo_mensaje, name='nuevo_mensaje'),
    path('Contacto/', views.contacto, name='contacto'),
    path('Contacto/<int:instituto_id>/', views.contacto, name='contacto'),
    path('Sobre-Nosotros', views.sobre_nosotros, name='nosotros'),
    #path('PruebaCorreo', views.prueba_correo, name='prueba_correo'),
    path('admin/mensajes/', views.mensajes, name='mensajes'),
    path('admin/leidos/', views.leidos, name='leidos'),
    path('admin/Pendientes/', views.pendientes, name='pendientes'),
    path('admin/Activos/', views.activos, name='activos'),
    path('admin/Inactivos/', views.inactivos, name='inactivos'),
    path('admin/marcarLeido/<int:mensaje_id>/', views.marcar_leido, name='marcar_leido'),
    #path('admin/mandar_link/<int:mensaje_id>/', views.mandar_link, name='mandar_link'),
    path('admin/habilitarInstituto/<int:id>/', views.habilitarInstituto, name='habilitar_instituto'),
    path('admin/deshabilitarInstituto/<int:id>/', views.deshabilitarInstituto, name='deshabilitar_instituto'),
    path('admin/cargarParadas', views.cargarParadas, name='cargar_paradas'),
    path('Activar/<hash_id>/', views.activar, name='activar'),
    path('admin/paradasCoords/', views.paradasCoords, name='paradasCoords'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)