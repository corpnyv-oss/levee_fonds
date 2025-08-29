from django.http import JsonResponse, HttpRequest
from django.conf import settings


def accueil(request: HttpRequest) -> JsonResponse:
    """Accueil du backend: simple JSON informatif."""
    return JsonResponse({
        "app": "fapag_collecte_backend",
        "message": "Bienvenue sur l'API de collecte de fonds FAPAG",
        "endpoints": {
            "documentation": "/swagger/",
            "api": "/api/",
            "admin": "/admin/",
            "health": "/healthz/",
        },
        "debug": bool(getattr(settings, "DEBUG", False)),
        "status": "operational",
    })


def health(request: HttpRequest) -> JsonResponse:
    """Endpoint de health-check très léger (sans accès DB)."""
    return JsonResponse({
        "status": "ok",
        "app": "fapag_collecte_backend",
    })
