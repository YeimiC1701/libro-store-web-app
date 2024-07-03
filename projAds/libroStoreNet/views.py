import re

# from django.contrib.auth.decorators import login_required
# from django.contrib.auth import update_session_auth_hash
from collections import Counter

from django.contrib import messages
from django.contrib.auth.hashers import check_password, make_password
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import get_list_or_404, get_object_or_404, redirect, render
from django.views.decorators.csrf import csrf_exempt
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
    masLeidos = (
        Libro.objects.select_related("categoria")
        .filter(categoria="1")
        .prefetch_related("autores")
    )
    novedades = (
        Libro.objects.select_related("categoria")
        .filter(categoria="2")
        .prefetch_related("autores")
    )
    data = {
        "titulo": {"masLeidos": "# Libros más leídos", "novedades": "# Novedades"},
        "librosMasLeidos": masLeidos,
        "novedades": novedades,
    }
    return render(request, "index.html", data)


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
"""


def perfil(request):
    idUsuario = request.session.get("cliente_id")
    usuario = Cliente.objects.get(id=idUsuario)

    data = {
        "usuario": usuario,
    }

    return render(request, "perfil.html", data)


def historialCompras(request):
    idUsuario = request.session.get("cliente_id")
    usuario = Cliente.objects.get(id=idUsuario)
    print("Usuario: ", usuario)
    compras = Transaccion.objects.select_related("cliente").filter(cliente=usuario)
    data = {
        "compras": compras,
    }

    return render(request, "historial-compras.html", data)


# Crear la vista de registro
def register(request):
    if request.method == 'POST':
        print(request.POST)  # Imprimir los datos POST para debuguear

        # Obtener los datos del formulario
        firstName = request.POST.get('firstName')
        lastName = request.POST.get('lastName')
        middleName = request.POST.get('middleName', '').strip()
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirmPassword = request.POST.get('confirmPassword')

        # Imprimir los datos para debuguear
        print(f"First Name: {firstName}")
        print(f"Last Name: {lastName}")
        print(f"Middle Name: {middleName}")
        print(f"Email: {email}")
        print(f"Password: {password}")
        print(f"Confirm Password: {confirmPassword}")

        # Verificar que el correo electrónico no esté vacío
        if not email:
            messages.error(request, 'El correo electrónico es obligatorio.')
            return redirect('register')

        # Verificar que las contraseñas coincidan
        if password != confirmPassword:
            messages.error(request, 'Las contraseñas no coinciden.')
            return redirect('register')

        # Verificar la validez del correo electrónico
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            messages.error(request, 'Correo electrónico inválido.')
            return redirect('register')

        # Verificar si el correo electrónico ya está registrado
        if Cliente.objects.filter(emailCliente=email).exists():
            messages.error(request, 'El correo electrónico ya está registrado.')
            return redirect('register')

        # Verificar que la contraseña cumpla con los criterios
        if not re.match(r'^(?=.*[A-Z])(?=.*\d)(?=.*[\/\-\*\_])[A-Za-z\d\/\-\*\_]{8,}$', password):
            messages.error(request, 'La contraseña debe contener al menos 8 caracteres, una letra mayúscula, un número y un símbolo especial (/, -, *, _).')
            return redirect('register')

        # Crear un nuevo cliente y guardar en la base de datos
        cliente = Cliente(
            nombresCliente=firstName,
            apellidoPaternoCliente=lastName,
            apellidoMaternoCliente=middleName if middleName else None,
            emailCliente=email,
            contraseniaCliente=make_password(password),
            estatusCliente='a'  # Activo
        )
        cliente.save()
        messages.success(request, 'Registro exitoso. Ya puedes iniciar sesión.')
        return redirect('login')

    # Renderizar la página de registro
    return render(request, 'CrearCuenta.html')


# Crear la vista de inicio de sesión
def login(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        cliente = Cliente.objects.filter(emailCliente=email).first()

        if cliente and check_password(password, cliente.contraseniaCliente):
            request.session["cliente_id"] = cliente.id
            messages.success(request, "Inicio de sesión exitoso.")
            return redirect("home")
        else:
            messages.error(
                request,
                "Correo o contraseña incorrectos. Por favor, inténtelo de nuevo.",
            )

    return render(request, "ingresar.html")


# Crear la vista de cierre de sesión
def logout(request):
    if "cliente_id" in request.session:
        del request.session["cliente_id"]
    return redirect("home")  # Redirigir a la página de inicio o de inicio de sesión


"""         Old cart

def cart(request):
    # For demonstration purposes, let's assume these are the book IDs from local storage
    book_ids = [3,5,4,6,7,7,5,5]  # Replace this with actual logic to get IDs from local storage

    # Count the occurrences of each book ID
    from collections import Counter
    book_counts = Counter(book_ids)

    # Fetch the books from the database based on these IDs
    books = get_list_or_404(Libro, id__in=book_counts.keys())

    # Create a list with book details and their counts
    book_details = []
    for book in books:
        book_details.append({
            'book': book,
            'count': book_counts[book.id],
            'available': book.stockLibro > 0,
            'max': book.stockLibro
        })

    # Pass the book data to the template
    return render(request, 'cart.html', {'book_details': book_details})

"""


@csrf_exempt
def remove_from_cart(request, book_id):
    if request.method == 'POST':
        # Retrieve the cart items from the session or create an empty list if not found
        cart_items = request.session.get('cart_items', [])
        
        # Remove the book ID from the cart items
        if book_id in cart_items:
            cart_items = [item for item in cart_items if item != book_id]
        
        # Save the updated cart items back to the session
        request.session['cart_items'] = cart_items
        
        # Respond with a success message
        return JsonResponse({'success': True})
    
    return JsonResponse({'success': False})

def cart(request):
    # Leer los elementos guardados en el carrito
    book_ids = request.session.get('cart_items', [])  # Default to an empty list if not found

    # Verificar si el carrito está vacío
    if not book_ids:
        messages.info(request, 'Tu bolsa está vacía.')
        return redirect('/')  # Redirigir a la página principal (lista de libros)

    # Conteo de ocurrencias de cada ID individual
    book_counts = Counter(book_ids)

    # Buscar los libros en la DB basado en el ID
    books = get_list_or_404(Libro, id__in=book_counts.keys())

    # Crear una lista con los datos de cada libro
    book_details = []
    for book in books:
        book_details.append({
            'book': book,
            'count': book_counts[book.id],
            'available': book.stockLibro > 0,
            'max': book.stockLibro
        })

    # Pasar la información de los libros a la plantilla
    return render(request, 'cart.html', {'book_details': book_details})

@csrf_exempt
def add_to_cart(request, book_id):
    if request.method == 'POST':
        # Retrieve the cart items from the session or create an empty list if not found
        cart_items = request.session.get('cart_items', [])
        
        # Add the new book ID to the cart items
        cart_items.append(book_id)
        
        # Save the updated cart items back to the session
        request.session['cart_items'] = cart_items
        
        # Respond with a success message
        return JsonResponse({'success': True})
    
    return JsonResponse({'success': False})

def clear_cart(request):
    # Clear the cart items from the session
    request.session['cart_items'] = []
    
    # Redirect to the cart page or any other appropriate page
    return redirect('cart')

# Implementación de vistas de Abraham
def verDatos(request):
    idUsuario = request.session.get("cliente_id")
    cliente = Cliente.objects.get(id=idUsuario)

    data = {
        "cliente": cliente,
    }

    return render(request, "datos-cliente.html", data)


def editarDatos(request):
    if request.method == "POST":
        idUsuario = request.session.get("cliente_id")
        usuario = Cliente.objects.get(id=idUsuario)
        nombre = request.POST.get("nombres").strip().title()
        apellidoPaterno = request.POST.get("apPaterno").strip().title()
        apellidoMaterno = request.POST.get("apMaterno").strip().title()
        email = request.POST.get("email").strip().lower()
        currentEmail = request.POST.get("currentEmail").strip().lower()
        currentPassword = request.POST.get("currentPassword").strip()
        contrasenia1 = request.POST.get("password1").strip()
        contrasenia2 = request.POST.get("password2").strip()

        # Verify current email and password
        if usuario.emailCliente != currentEmail or not check_password(
            currentPassword, usuario.contraseniaCliente
        ):
            messages.error(
                request, "La información de inicio de sesión actual es incorrecta."
            )
            return redirect("/perfil/")

        # Verify new passwords match
        if contrasenia1 and contrasenia1 != contrasenia2:
            messages.error(
                request, "Las contraseñas no coinciden. Por favor, inténtelo de nuevo."
            )
            return redirect("/perfil/")

        # Verify password requirements
        if contrasenia1 and not (
            len(contrasenia1) >= 8
            and any(char.isdigit() for char in contrasenia1)
            and any(char.isupper() for char in contrasenia1)
            and any(char in "/-*_," for char in contrasenia1)
        ):
            messages.error(
                request,
                "La nueva contraseña debe tener al menos 8 caracteres, un número, una letra mayúscula y un símbolo especial (/, -, *, _, ,).",
            )
            return redirect("/perfil/")

        usuario.nombresCliente = nombre
        usuario.apellidoPaternoCliente = apellidoPaterno
        usuario.apellidoMaternoCliente = apellidoMaterno
        usuario.emailCliente = email

        if contrasenia1:
            usuario.contraseniaCliente = make_password(contrasenia1)

        usuario.save()

    return redirect("/datos/")


def verDireccion(request):
    idUsuario = request.session.get("cliente_id")
    usuario = Cliente.objects.get(id=idUsuario)
    domicilio = Domicilio.objects.select_related("cliente").filter(cliente=usuario)
    domicilio = domicilio.first()

    data = {
        "direccion": domicilio,
    }

    return render(request, "direccion.html", data)


def editarDireccion(request):
    if request.method == "POST":
        idDireccion = request.POST.get("idDireccion")

        if not idDireccion:
            cliente = Cliente.objects.get(id=request.session.get("cliente_id"))
            print("Cliente en editarDireccion: ", cliente.nombresCliente)

            direccion = Domicilio(
                calleDomicilio=request.POST.get("calle").strip().title(),
                numeroExteriorDomicilio=request.POST.get("numero").strip().title(),
                codigoPostalDomicilio=request.POST.get("codigoPostal").strip().title(),
                coloniaDomicilio=request.POST.get("colonia").strip().title(),
                municipioDomicilio=request.POST.get("delMnpio").strip().title(),
                estadoDomicilio=request.POST.get("estado").strip().title(),
                cliente=cliente,
            )

            print("Direccion en editarDireccion: ", direccion)
            direccion.save()

        else:
            idDireccion = int(idDireccion)
            calle = request.POST.get("calle").strip().title()
            numero = request.POST.get("numero").strip().title()
            colonia = request.POST.get("colonia").strip().title()
            codigoPostal = request.POST.get("codigoPostal").strip().title()
            delMnpio = request.POST.get("delMnpio").strip().title()
            estado = request.POST.get("estado").strip().title()

            nuevaDireccion = Domicilio.objects.get(id=idDireccion)
            nuevaDireccion.calleDomicilio = calle
            nuevaDireccion.numeroExteriorDomicilio = numero
            nuevaDireccion.coloniaDomicilio = colonia
            nuevaDireccion.codigoPostalDomicilio = codigoPostal
            nuevaDireccion.municipioDomicilio = delMnpio
            nuevaDireccion.estadoDomicilio = estado
            nuevaDireccion.save()

    return redirect('/direccion/')

def catalogo(request):
    query = request.GET.get("q", "")
    sort_by = request.GET.get("sort", "tituloLibro")

    if query:
        libros = Libro.objects.filter(
            Q(tituloLibro__icontains=query)
            | Q(resumenLibro__icontains=query)
            | Q(precioLibro__icontains=query)
        ).order_by("-" + sort_by)
    else:
        libros = Libro.objects.all().prefetch_related("autores").order_by("-" + sort_by)

    paginator = Paginator(libros, 10)  # 10 libros por página

    numero_pagina = request.GET.get("page")
    page_obj = paginator.get_page(numero_pagina)

    return render(
        request,
        "catalogo.html",
        {"page_obj": page_obj, "sort_by": sort_by, "query": query},
    )


def libroDetalle(request, pk):
    libro = get_object_or_404(Libro.objects.prefetch_related("autores"), pk=pk)
    return render(request, "libroDetalle.html", {"libro": libro})

def checkout(request):
    # redirigir a login si no ha sesion abierta
    if 'cliente_id' not in request.session:
        return redirect('login')
    
    # Datos del cliente
    idUsuario = request.session.get('cliente_id')
    usuario = Cliente.objects.get(id = idUsuario)
    domicilio = Domicilio.objects.select_related('cliente').filter(cliente = usuario)
    domicilio = domicilio.first()

    # Retrieve the cart items from the session or create an empty list if not found
    idLibros = request.session.get("cart_items", [])
    conteo_libros = Counter(idLibros)

    libros = Libro.objects.filter(id__in=idLibros)

    # Crear los items del pedido
    items_pedido = []
    print('Libros ennnnnnnnnn pedido', conteo_libros)
    for libro in libros:
        cantidad = conteo_libros[libro.id]
        item = {
            'libro': libro,
            'cantidad': cantidad,  
            'precio': libro.precioLibro,
            'subtotal': libro.precioLibro * cantidad, 
        }
        items_pedido.append(item)
    
    # Calcular el total
    total = sum(item['precio'] for item in items_pedido)
    
    # Construir el pedido
    pedido = {
        'items': items_pedido,
        'total': total,
    }
    
    data = {
        'direccion': domicilio,
        'usuario': usuario,
        'pedido': pedido,
    }

    return render(request, "checkout.html", data)


# def finalizarCompra(request):
#     if request.method == 'POST':
#         # Datos del cliente
#         idUsuario = request.session.get('cliente_id')
#         usuario = Cliente.objects.get(id = idUsuario)
        
#         # Retrieve the cart items from the session or create an empty list if not found
#         cart_items = request.session.get("cart_items", [])

#     return redirect('historial')