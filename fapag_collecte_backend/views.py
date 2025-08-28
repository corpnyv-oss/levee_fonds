from django.http import JsonResponse, HttpResponse
from django.template.loader import render_to_string
from django.views.decorators.http import require_http_methods
from django_ratelimit.exceptions import Ratelimited

def accueil(request):
    """
    Vue d'accueil simple sans authentification
    """
    return JsonResponse({
        'message': 'Bienvenue sur l\'API de collecte de fonds FAPAG',
        'endpoints': {
            'documentation': '/swagger/',
            'api': '/api/',
            'admin': '/admin/'
        },
        'status': 'opérationnel'
    })


def ratelimited_error(request, exception=None):
    """
    Vue personnalisée pour les erreurs de rate limiting
    """
    response = JsonResponse({
        'error': 'Too many requests',
        'message': 'Vous avez dépassé le nombre de tentatives autorisées. Veuillez réessayer plus tard.',
        'status_code': 429
    }, status=429)
    
    # Ajout des en-têtes de rate limiting
    if hasattr(exception, 'wait'):
        wait = exception.wait()
        response['Retry-After'] = str(wait)
        response['X-RateLimit-Reset'] = str(wait)
    
    return response
