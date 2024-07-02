from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('perfil/', views.perfil, name='perfil'),
    path('ingresar/', views.login, name='login'),
    path('historial/', views.historialCompras, name='historial'),
    path('direccion/', views.verDireccion, name='verDireccion'),
    path('editarDireccion/', views.editarDireccion, name='editarDireccion'),
]