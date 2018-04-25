from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('buscar/', views.buscar, name='buscar'),
    path('Instituto/<int:instituto_id>/', views.perfil, name='perfil'),
    path('Instituto/<int:instituto_id>/nuevo_mensaje', views.nuevo_mensaje, name='nuevo_mensaje'),
]