from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Cliente
from django.contrib.auth.hashers import make_password, check_password
import re


# Create your views here.
def home(request):
    return render(request, 'index.html')

def register(request):
    if request.method == 'POST':
        print(request.POST)  # Print the POST data. Para debugear

        # Obtiene los datos del formulario
        first_name = request.POST.get('firstName')
        last_name = request.POST.get('lastName')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirmPassword')

        # Imprime los datos para debuguear
        print(f"First Name: {first_name}")
        print(f"Last Name: {last_name}")
        print(f"Email: {email}")
        print(f"Password: {password}")
        print(f"Confirm Password: {confirm_password}")

        # Verifica que el email no esté vacío
        if not email:
            messages.error(request, 'El correo electrónico es obligatorio.')
            return redirect('register')

        # Verifica que las contraseñas coincidan
        if password != confirm_password:
            messages.error(request, 'Las contraseñas no coinciden.')
            return redirect('register')

        # Verifica la validez del email
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            messages.error(request, 'Correo electrónico inválido.')
            return redirect('register')

        # Verifica si el email ya está registrado
        if Cliente.objects.filter(emailCliente=email).exists():
            messages.error(request, 'El correo electrónico ya está registrado.')
            return redirect('register')

        # Verifica que la contraseña cumpla con los criterios
        if not re.match(r'^(?=.*[A-Z])(?=.*\d)(?=.*[\/\-\*\_])[A-Za-z\d\/\-\*\_]{8,}$', password):
            messages.error(request, 'La contraseña debe contener al menos 8 caracteres, una letra mayúscula, un número y un símbolo especial (/, -, *, _).')
            return redirect('register')

        # Crea un nuevo cliente y guarda en la base de datos
        cliente = Cliente(
            nombresCliente=first_name,
            apellidoPaternoCliente=last_name,
            emailCliente=email,
            contraseniaCliente=make_password(password),
            estatusCliente='a'  # Activo
        )
        cliente.save()
        messages.success(request, 'Registro exitoso. Ya puedes iniciar sesión.')
        return redirect('login')

    # Renderiza la página de registro
    return render(request, 'CrearCuenta.html')


def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        cliente = Cliente.objects.filter(emailCliente=email).first()

        if cliente and check_password(password, cliente.contraseniaCliente):
            request.session['cliente_id'] = cliente.id
            messages.success(request, 'Login successful.')
            return redirect('home')  # Replace with your desired redirect
        else:
            messages.error(request, 'Invalid email or password.')

    return render(request, 'ingresar.html')

def logout(request):
    if 'cliente_id' in request.session:
        del request.session['cliente_id']
    return redirect('home')  # Redirect to home or login page
