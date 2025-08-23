from django.http import HttpRequest, HttpResponse
from typing import Any, Callable

class SecurityHeadersMiddleware:
    """
    Middleware pour ajouter des en-têtes de sécurité HTTP.
    """
    def __init__(self, get_response: Callable[[HttpRequest], Any]):
        self.get_response = get_response

    def __call__(self, request: HttpRequest) -> HttpResponse:
        response = self.get_response(request)
        
        # En-têtes de sécurité
        security_headers = {
            'X-Content-Type-Options': 'nosniff',
            'X-Frame-Options': 'DENY',
            'X-XSS-Protection': '1; mode=block',
            'Referrer-Policy': 'same-origin',
            'Permissions-Policy': 'camera=(), microphone=(), geolocation=()',
            'Cross-Origin-Opener-Policy': 'same-origin',
            'Cross-Origin-Resource-Policy': 'same-origin',
        }
        
        # Ajout des en-têtes à la réponse
        for header, value in security_headers.items():
            if header not in response:
                response[header] = value
                
        return response
