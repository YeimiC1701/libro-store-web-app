from django.contrib import messages
from django.shortcuts import redirect, render
from libroStoreNet.models import *
from django.contrib.auth.hashers import check_password, make_password
import re


# Create your views here.

"""
Función de vista que recupera los 10 libros más leídos y los muestra en la plantilla 'masLeidos.html'.

Args:
    request: El objeto de solicitud HTTP.

Returns:
    Una respuesta HTTP que renderiza la plantilla 'masLeidos.html' con los libros más leídos.
"""
def home(request):
    masLeidos = Libro.objects.select_related('categoria').filter(
                    categoria='1').prefetch_related('autores')
    novedades = Libro.objects.select_related('categoria').filter(
                    categoria='2').prefetch_related('autores')
    data = {
        'titulo': {"masLeidos": "# Libros más leídos", "novedades": "# Novedades"},
        'librosMasLeidos': masLeidos,
        'novedades': novedades,
    }
    return render(request, 'index.html', data)

"""
# Vista de pruebas para redireccion 
def uno(request):
    librosMasLeidos = Libro.objects.select_related('categoria').filter(
                    categoria='2').prefetch_related('autores')[:3]
    data = {
        'titulo': '# VISTA DE PRUEBAS #',
        'librosMasLeidos': librosMasLeidos,
    }
    return render(request, "uno.html", data)

"""
def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        cliente = Cliente.objects.filter(emailCliente=email).first()
        print("Cliente: ", cliente, "contraseña: ", password)

        if cliente and check_password(password, cliente.contraseniaCliente):
            request.session['cliente_id'] = cliente.id
            messages.success(request, 'Login successful.')
            print("Login successful.")
            return redirect('perfil')  # Replace with your desired redirect
        elif cliente and password == cliente.contraseniaCliente:
            request.session['cliente_id'] = cliente.id
            messages.success(request, 'Login successful.')
            print("Login successful.")
            return redirect('perfil')  # Replace with your desired redirect
        else:
            print("Login failed dentro de else.")
            messages.error(request, 'Correo o contraseña incorrectos. Por favor, inténtelo de nuevo.')
    
    print("Login failed en la vista.")
    return render(request, 'login.html')


def perfil(request):
    idUsuario = request.session.get('cliente_id')
    usuario = Cliente.objects.get(id = idUsuario)

    data = {
        'usuario': usuario,
    }

    return render(request, "perfil.html", data)


def historialCompras(request):
    idUsuario = request.session.get('cliente_id')
    usuario = Cliente.objects.get(id = idUsuario)
    print("Usuario: ", usuario)
    compras = Transaccion.objects.select_related('cliente').filter(cliente = usuario)
    data = {
        'compras': compras,
    }

    return render(request, "historial-compras.html", data)