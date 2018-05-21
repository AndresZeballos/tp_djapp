from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('on_login', views.on_login, name='on_login'),
    path('perfil', views.perfil, name='perfil'),
    path('buscar', views.buscar, name='buscar'),
    path('Instituto/<int:instituto_id>/', views.instituto, name='instituto'),
    path('Instituto/<int:instituto_id>/nuevo_mensaje', views.nuevo_mensaje, name='nuevo_mensaje'),
    path('contacto', views.contacto, name='contacto'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)