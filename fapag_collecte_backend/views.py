from django.http import JsonResponse

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
