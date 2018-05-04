from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('on_login', views.on_login, name='on_login'),
    path('perfil', views.perfil, name='perfil'),
]