from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('perfil/', views.perfil, name='perfil'),
    path('ingresar/', views.login, name='login'),
    path('historial/', views.historialCompras, name='historial'),
    # path('uno/', views.uno, name='uno'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    #path('cart/', views.cart, name='cart'),
    #path('editarPerfil', views.update_profile, name='update_profile'),
    path('datos/', views.verDatos, name='verDatos'),
    path('editarDatos/', views.editarDatos, name='editarDatos'),
    path('books/', views.book_list, name='book_list'),
    path('cart/', views.cart, name='cart'),
    path('add_to_cart/<int:book_id>/', views.add_to_cart, name='add_to_cart'),
    path('clear_cart/', views.clear_cart, name='clear_cart'),
    path('direccion/', views.verDireccion, name='verDireccion'),
    path('editarDireccion/', views.editarDireccion, name='editarDireccion'),
    path('checkout/', views.checkout, name='checkout'),
]