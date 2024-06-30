from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Cliente
from django.contrib.auth.hashers import make_password, check_password
import re
from django.shortcuts import get_list_or_404
from .models import Libro

# Crear la vista principal
def home(request):
    return render(request, 'index.html')

# Crear la vista de registro
def register(request):
    if request.method == 'POST':
        print(request.POST)  # Imprimir los datos POST para debuguear

        # Obtener los datos del formulario
        firstName = request.POST.get('firstName')
        lastName = request.POST.get('lastName')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirmPassword = request.POST.get('confirmPassword')

        # Imprimir los datos para debuguear
        print(f"First Name: {firstName}")
        print(f"Last Name: {lastName}")
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
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        cliente = Cliente.objects.filter(emailCliente=email).first()

        if cliente and check_password(password, cliente.contraseniaCliente):
            request.session['cliente_id'] = cliente.id
            messages.success(request, 'Inicio de sesión exitoso.')
            return redirect('home')  # Reemplazar con la redirección deseada
        else:
            messages.error(request, 'Correo o contraseña incorrectos. Por favor, inténtelo de nuevo.')

    return render(request, 'ingresar.html')

# Crear la vista de cierre de sesión
def logout(request):
    if 'cliente_id' in request.session:
        del request.session['cliente_id']
    return redirect('home')  # Redirigir a la página de inicio o de inicio de sesión



from django.shortcuts import render, get_list_or_404
from .models import Libro

def cart(request):
    # For demonstration purposes, let's assume these are the book IDs from local storage
    book_ids = [1, 2, 3, 1, 2, 1]  # Replace this with actual logic to get IDs from local storage

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
