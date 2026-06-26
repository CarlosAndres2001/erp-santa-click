import threading

_local = threading.local()

class UsuarioMiddleware:
    """
    Middleware para guardar el usuario actual en thread local.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        _local.usuario_actual = getattr(request, 'user', None)
        response = self.get_response(request)
        return response

def get_usuario_actual():
    return getattr(_local, 'usuario_actual', None)
