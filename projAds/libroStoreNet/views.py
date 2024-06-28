from django.shortcuts import render
from libroStoreNet.models import *


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
    # return render(request, "masLeidos.html", data)
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

def perfil(request):
    usuario = Cliente.objects.get(id=1)
    data = {
        'usuario': usuario,
    }
    return render(request, "perfil.html", data)
"""