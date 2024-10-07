from django.shortcuts import render
from .forms import PersonaForm
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        # Autenticación del usuario
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            # Iniciar sesión y redirigir a la página principal
            auth_login(request, user)  # Cambiar a auth_login para evitar conflictos
            render(request, 'main.html')  # Cambia la URL a la que desees redirigir
        else:
            # Mensaje de error si el usuario no existe o la contraseña es incorrecta
            messages.error(request, 'Usuario o contraseña incorrectos')
    
    return render(request, 'login.html')

@login_required
def register(request):
    if request.method == 'POST':
        form = PersonaForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()  # Guarda el registro en la base de datos
            return render(request, 'register.html')  # Redirige a una vista de lista o a otra página después de guardar
    else:
        form = PersonaForm()
    return render(request, 'register.html', {'form': form})

def exit(request):
    logout(request)
    return redirect('/')