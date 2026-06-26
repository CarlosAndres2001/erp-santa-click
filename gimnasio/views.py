from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

def landing_view(request):
    return render(request, "landing_page.html")

def login_view(request):
    if request.user.is_authenticated:
        messages.info(request, f"El usuario {request.user.nombre} ya está logeado.")
        return redirect('panel_view')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None and user.is_active:
            if user.is_logged_in:
                messages.error(request, "Este usuario ya tiene sesión activa. Cierre la sesión antes de iniciar nuevamente.")
                return redirect('login')

            user.is_logged_in = True
            user.save()
            login(request, user)
            messages.success(request, f"Bienvenido {user.nombre}!")
            return redirect('panel_view')
        else:
            messages.error(request, "Usuario o contraseña incorrecta")

    return render(request, 'login.html')


def logout_view(request):
    if request.user.is_authenticated:
        request.user.is_logged_in = False
        request.user.save()
        logout(request)
        messages.success(request, "Sesión cerrada correctamente.")
    return redirect('login')


@login_required(login_url='login')
def panel_view(request):
    return render(request, 'base.html')
