from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.sessions.models import Session
from django.utils import timezone
from gym.models import Producto, Usuario, Sucursal, Stock, Almacen

def landing_view(request):
    return render(request, "landing_page.html")


def _sesion_activa_de_verdad(user):
    """
    Pregunta a la tabla real de sesiones si el session_key guardado sigue
    vivo. Si el navegador se cerró de golpe sin logout, la sesión expira
    sola y esto da False -> se entra directo, sin bloqueo fantasma.
    Asume SESSION_ENGINE por defecto (django.contrib.sessions.backends.db).
    """
    if not user.session_key:
        return False
    return Session.objects.filter(
        session_key=user.session_key,
        expire_date__gt=timezone.now(),
    ).exists()


def login_view(request):
    if request.user.is_authenticated:
        messages.info(request, f"El usuario {request.user.nombre} ya está logeado.")
        return redirect('panel_view')

    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password')
        forzar = request.POST.get('forzar') == '1'

        user = authenticate(request, email=email, password=password)

        if user is None or not user.is_active:
            messages.error(request, "Email o contraseña incorrectos.")
            return render(request, 'login.html')

        if _sesion_activa_de_verdad(user) and not forzar:
            return render(request, 'login_confirmar_sesion.html', {
                'email': email,
                'password': password,
            })

        if forzar and user.session_key:
            Session.objects.filter(session_key=user.session_key).delete()

        login(request, user)
        request.session.save()
        user.session_key = request.session.session_key
        user.save(update_fields=['session_key'])

        messages.success(request, f"Bienvenido {user.nombre}!")
        return redirect('panel_view')

    return render(request, 'login.html')


def logout_view(request):
    if request.user.is_authenticated:
        request.user.session_key = None
        request.user.save(update_fields=['session_key'])
        logout(request)
        messages.success(request, "Sesión cerrada correctamente.")
    return redirect('login')


#@login_required(login_url='login')
#def panel_view(request):
#    return render(request, 'base.html')


UMBRAL_STOCK_BAJO = 5  # provisional: no hay campo de "stock mínimo" en el modelo todavía


@login_required(login_url='login')
def panel_view(request):
    empresa = request.user.fk_empresa

    context = {
        'fecha_actual': timezone.now(),

        # Conteos operativos, NADA de montos de dinero (esta pantalla la ve
        # cualquier usuario, sin importar su rol/permisos).
        'total_productos_terminados': Producto.objects.filter(
            fk_empresa=empresa, is_active=True, fk_tipo_producto__codigo='PROD-TERM'
        ).count(),
        'total_insumos': Producto.objects.filter(
            fk_empresa=empresa, is_active=True, fk_tipo_producto__codigo='INS-RAW'
        ).count(),
        'total_procesados': Producto.objects.filter(
            fk_empresa=empresa, is_active=True, fk_tipo_producto__codigo='PROD-PROC'
        ).count(),
        'total_combos': Producto.objects.filter(
            fk_empresa=empresa, is_active=True, fk_tipo_producto__codigo='COMBO-PACK'
        ).count(),
        'total_usuarios': Usuario.objects.filter(
            sucursal__fk_empresa=empresa, is_active=True
        ).count(),
        'total_sucursales': Sucursal.objects.filter(fk_empresa=empresa, estado=True).count(),
        'total_almacenes': Almacen.objects.filter(sucursal__fk_empresa=empresa, is_active=True).count(),

        'stock_bajo_count': Stock.objects.filter(
            producto_variante__producto__fk_empresa=empresa,
            cantidad_actual__lte=UMBRAL_STOCK_BAJO,
            cantidad_actual__gt=0,
        ).count(),
        'stock_agotado_count': Stock.objects.filter(
            producto_variante__producto__fk_empresa=empresa,
            cantidad_actual__lte=0,
        ).count(),
    }

    return render(request, 'panel.html', context)