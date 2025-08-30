"""
Module de sécurité pour les webhooks et l'API
"""
import hmac
import hashlib
import time
from typing import Optional, Dict, Any
from django.conf import settings
from django.core.exceptions import ValidationError
from django.http import HttpRequest
from django.utils import timezone
from datetime import timedelta
import logging

logger = logging.getLogger(__name__)

class WebhookSecurity:
    """Classe de sécurité pour les webhooks"""
    
    def __init__(self):
        self.secret_key = getattr(settings, 'WEBHOOK_SECRET_KEY', 'default-secret-key-change-in-production')
        self.allowed_ips = getattr(settings, 'WEBHOOK_ALLOWED_IPS', [])
        self.timestamp_window = getattr(settings, 'WEBHOOK_TIMESTAMP_WINDOW', 300)  # 5 minutes
        
    def verify_hmac(self, payload: bytes, signature: str, timestamp: Optional[str] = None) -> bool:
        """
        Vérifie la signature HMAC du webhook
        
        Args:
            payload: Corps de la requête en bytes
            signature: Signature HMAC reçue
            timestamp: Horodatage du webhook (optionnel)
            
        Returns:
            bool: True si la signature est valide
        """
        try:
            # Vérifier l'horodatage si fourni
            if timestamp:
                if not self._verify_timestamp(timestamp):
                    logger.warning(f"Webhook timestamp invalide: {timestamp}")
                    return False
            
            # Calculer la signature attendue
            expected_signature = hmac.new(
                self.secret_key.encode('utf-8'),
                payload,
                hashlib.sha256
            ).hexdigest()
            
            # Comparaison constante (évite les attaques par timing)
            return hmac.compare_digest(signature, expected_signature)
            
        except Exception as e:
            logger.error(f"Erreur lors de la vérification HMAC: {e}")
            return False
    
    def _verify_timestamp(self, timestamp: str) -> bool:
        """
        Vérifie que l'horodatage du webhook est dans la fenêtre de temps autorisée
        
        Args:
            timestamp: Horodatage ISO du webhook
            
        Returns:
            bool: True si l'horodatage est valide
        """
        try:
            webhook_time = timezone.datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
            current_time = timezone.now()
            
            # Vérifier que le webhook n'est pas trop ancien
            if webhook_time < current_time - timedelta(seconds=self.timestamp_window):
                return False
                
            # Vérifier que le webhook n'est pas dans le futur (tolérance de 1 minute)
            if webhook_time > current_time + timedelta(minutes=1):
                return False
                
            return True
            
        except Exception as e:
            logger.error(f"Erreur lors de la vérification de l'horodatage: {e}")
            return False
    
    def verify_ip_address(self, ip_address: str) -> bool:
        """
        Vérifie que l'IP source est dans la liste autorisée
        
        Args:
            ip_address: Adresse IP source
            
        Returns:
            bool: True si l'IP est autorisée
        """
        if not self.allowed_ips:
            logger.warning("Aucune IP autorisée configurée pour les webhooks")
            return True  # En développement, accepter toutes les IPs
            
        return ip_address in self.allowed_ips
    
    def verify_webhook_request(self, request: HttpRequest, signature: str, timestamp: Optional[str] = None) -> Dict[str, Any]:
        """
        Vérifie la sécurité complète d'une requête webhook
        
        Args:
            request: Requête HTTP Django
            signature: Signature HMAC reçue
            timestamp: Horodatage du webhook (optionnel)
            
        Returns:
            Dict avec le statut de vérification et les détails
        """
        result = {
            'is_valid': False,
            'errors': [],
            'warnings': []
        }
        
        # 1. Vérifier l'IP source
        client_ip = self._get_client_ip(request)
        if not self.verify_ip_address(client_ip):
            result['errors'].append(f"IP source non autorisée: {client_ip}")
        
        # 2. Vérifier la signature HMAC
        if not self.verify_hmac(request.body, signature, timestamp):
            result['errors'].append("Signature HMAC invalide")
        
        # 3. Vérifier l'horodatage si fourni
        if timestamp and not self._verify_timestamp(timestamp):
            result['warnings'].append("Horodatage du webhook suspect")
        
        # Le webhook est valide s'il n'y a pas d'erreurs critiques
        result['is_valid'] = len(result['errors']) == 0
        
        # Journaliser le résultat
        if result['is_valid']:
            logger.info(f"Webhook validé avec succès depuis {client_ip}")
        else:
            logger.warning(f"Webhook rejeté depuis {client_ip}: {result['errors']}")
        
        return result
    
    def _get_client_ip(self, request: HttpRequest) -> str:
        """
        Récupère l'IP réelle du client (gère les proxies)
        
        Args:
            request: Requête HTTP Django
            
        Returns:
            str: Adresse IP du client
        """
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            return x_forwarded_for.split(',')[0].strip()
        return request.META.get('REMOTE_ADDR', 'unknown')


class RateLimiter:
    """Classe de limitation de débit pour l'API"""
    
    def __init__(self):
        self.rate_limits = {
            'auth': {'requests': 5, 'window': 300},  # 5 tentatives par 5 minutes
            'participations': {'requests': 10, 'window': 60},  # 10 par minute
            'webhooks': {'requests': 100, 'window': 60},  # 100 par minute
        }
    
    def is_allowed(self, endpoint: str, identifier: str) -> bool:
        """
        Vérifie si une requête est autorisée selon la limitation de débit
        
        Args:
            endpoint: Endpoint de l'API
            identifier: Identifiant unique (IP, user_id, etc.)
            
        Returns:
            bool: True si la requête est autorisée
        """
        # TODO: Implémenter avec Redis ou base de données
        # Pour l'instant, retourner True
        return True


# Instances globales
webhook_security = WebhookSecurity()
rate_limiter = RateLimiter()
