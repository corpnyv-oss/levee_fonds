"""
Décorateurs de sécurité pour l'API
"""
import functools
import logging
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from .security import webhook_security, rate_limiter

logger = logging.getLogger(__name__)


def secure_webhook(require_hmac=True, require_timestamp=True, require_ip_check=True):
    """
    Décorateur pour sécuriser les endpoints webhook
    
    Args:
        require_hmac: Vérifier la signature HMAC
        require_timestamp: Vérifier l'horodatage
        require_ip_check: Vérifier l'IP source
    """
    def decorator(view_func):
        @csrf_exempt
        @require_http_methods(["POST"])
        @functools.wraps(view_func)
        def wrapper(request, *args, **kwargs):
            try:
                # Récupérer les en-têtes de sécurité
                signature = request.headers.get('X-Webhook-Signature')
                timestamp = request.headers.get('X-Webhook-Timestamp') if require_timestamp else None
                
                # Vérifications de sécurité
                if require_hmac and not signature:
                    logger.warning("Webhook rejeté: signature HMAC manquante")
                    return JsonResponse(
                        {'error': 'Signature HMAC requise'}, 
                        status=401
                    )
                
                # Vérifier la sécurité du webhook
                security_result = webhook_security.verify_webhook_request(
                    request, 
                    signature or '', 
                    timestamp
                )
                
                if not security_result['is_valid']:
                    logger.warning(f"Webhook rejeté: {security_result['errors']}")
                    return JsonResponse(
                        {'error': 'Webhook non autorisé', 'details': security_result['errors']}, 
                        status=403
                    )
                
                # Vérifier la limitation de débit
                client_ip = webhook_security._get_client_ip(request)
                if not rate_limiter.is_allowed('webhooks', client_ip):
                    logger.warning(f"Rate limit dépassé pour {client_ip}")
                    return JsonResponse(
                        {'error': 'Trop de requêtes'}, 
                        status=429
                    )
                
                # Appeler la vue originale
                return view_func(request, *args, **kwargs)
                
            except Exception as e:
                logger.error(f"Erreur lors de la vérification de sécurité du webhook: {e}")
                return JsonResponse(
                    {'error': 'Erreur interne de sécurité'}, 
                    status=500
                )
        
        return wrapper
    return decorator


def rate_limit(endpoint, requests_per_window, window_seconds):
    """
    Décorateur pour limiter le débit des requêtes
    
    Args:
        endpoint: Nom de l'endpoint pour la limitation
        requests_per_window: Nombre de requêtes autorisées
        window_seconds: Fenêtre de temps en secondes
    """
    def decorator(view_func):
        @functools.wraps(view_func)
        def wrapper(request, *args, **kwargs):
            # Identifier le client (IP ou user_id)
            if request.user.is_authenticated:
                identifier = str(request.user.id)
            else:
                identifier = webhook_security._get_client_ip(request)
            
            # Vérifier la limitation de débit
            if not rate_limiter.is_allowed(endpoint, identifier):
                logger.warning(f"Rate limit dépassé pour {endpoint} - {identifier}")
                return JsonResponse(
                    {'error': 'Trop de requêtes', 'retry_after': window_seconds}, 
                    status=429
                )
            
            return view_func(request, *args, **kwargs)
        
        return wrapper
    return decorator


def audit_log(action, resource_type=None):
    """
    Décorateur pour journaliser les actions importantes
    
    Args:
        action: Description de l'action
        resource_type: Type de ressource affectée
    """
    def decorator(view_func):
        @functools.wraps(view_func)
        def wrapper(request, *args, **kwargs):
            # Journaliser avant l'action
            user_info = f"user:{request.user.id}" if request.user.is_authenticated else "anonymous"
            ip_address = webhook_security._get_client_ip(request)
            
            logger.info(
                f"AUDIT: {action} - {user_info} - IP:{ip_address} - "
                f"Resource:{resource_type} - Method:{request.method}"
            )
            
            try:
                # Exécuter la vue
                response = view_func(request, *args, **kwargs)
                
                # Journaliser le succès
                logger.info(
                    f"AUDIT: {action} SUCCESS - {user_info} - "
                    f"Status:{response.status_code}"
                )
                
                return response
                
            except Exception as e:
                # Journaliser l'échec
                logger.error(
                    f"AUDIT: {action} FAILED - {user_info} - "
                    f"Error:{str(e)}"
                )
                raise
        
        return wrapper
    return decorator
