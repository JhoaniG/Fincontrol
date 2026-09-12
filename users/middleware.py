from django.utils.cache import add_never_cache_headers

class NoCacheMiddleware:
    """
    Middleware que previene que el navegador guarde en caché páginas que
    requieren autenticación. Esto soluciona el problema de volver "Atrás"
    y ver datos confidenciales después de cerrar sesión.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        
        # Si el usuario está autenticado, no queremos que el navegador
        # guarde en caché nada de la respuesta.
        if request.user.is_authenticated:
            add_never_cache_headers(response)
            
        return response
