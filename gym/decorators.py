# gym/decorators.py
from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages

def permiso_requerido(codigo_modulo, accion='ver'):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            # Si es administrador, pasa directo
            if request.user.rol.nombre.lower() == 'administrador':
                return view_func(request, *args, **kwargs)
            
            # Verificar permiso específico
            from gym.models import PermisoRol
            tiene_permiso = PermisoRol.objects.filter(
                rol=request.user.rol,
                modulo__codigo=codigo_modulo,
                **{f'puede_{accion}': True}
            ).exists()
            
            if tiene_permiso:
                return view_func(request, *args, **kwargs)
            
            messages.error(request, f'No tienes permiso para acceder a esta sección')
            return redirect('/')
        return wrapper
    return decorator