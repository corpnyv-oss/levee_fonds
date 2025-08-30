"""
Vues sécurisées pour les webhooks
"""
import json
import logging
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.utils import timezone
from .decorators import secure_webhook, audit_log
from .models import Transaction, WebhookEvent, Participation
from .security import webhook_security

logger = logging.getLogger(__name__)


@csrf_exempt
@require_http_methods(["POST"])
@secure_webhook(require_hmac=True, require_timestamp=True, require_ip_check=True)
@audit_log("Webhook PSP reçu", "Transaction")
def psp_webhook(request):
    """
    Endpoint webhook sécurisé pour les notifications de paiement des PSP
    
    En-têtes requis:
    - X-Webhook-Signature: Signature HMAC du payload
    - X-Webhook-Timestamp: Horodatage ISO du webhook
    - Content-Type: application/json
    
    Corps de la requête:
    {
        "provider_ref": "unique_id_from_psp",
        "reference_psp": "psp_transaction_id",
        "status": "success|failed|cancelled",
        "amount": 1000.00,
        "currency": "XAF",
        "metadata": {...}
    }
    """
    try:
        # Parser le payload JSON
        payload = json.loads(request.body)
        
        # Extraire les données essentielles
        provider_ref = payload.get('provider_ref')
        reference_psp = payload.get('reference_psp')
        status_psp = payload.get('status')
        amount = payload.get('amount')
        
        if not all([provider_ref, reference_psp, status_psp]):
            logger.error(f"Webhook invalide: données manquantes - {payload}")
            return JsonResponse(
                {'error': 'Données manquantes'}, 
                status=400
            )
        
        # Vérifier l'idempotence (éviter le double traitement)
        existing_webhook = WebhookEvent.objects.filter(
            transaction__provider_ref=provider_ref
        ).first()
        
        if existing_webhook:
            logger.info(f"Webhook déjà traité: {provider_ref}")
            return JsonResponse(
                {'message': 'Webhook déjà traité', 'id': existing_webhook.id}, 
                status=200
            )
        
        # Créer ou mettre à jour la transaction
        transaction, created = Transaction.objects.get_or_create(
            provider_ref=provider_ref,
            defaults={
                'reference_psp': reference_psp,
                'statut': _map_psp_status(status_psp),
                'participation_id': payload.get('participation_id'),  # Si fourni
            }
        )
        
        if not created:
            # Mettre à jour la transaction existante
            transaction.reference_psp = reference_psp
            transaction.statut = _map_psp_status(status_psp)
            transaction.save()
        
        # Créer l'événement webhook
        webhook_event = WebhookEvent.objects.create(
            transaction=transaction,
            payload=payload,
            signature=request.headers.get('X-Webhook-Signature', ''),
            statut='recu',
            ip_source=webhook_security._get_client_ip(request)
        )
        
        # Traiter le statut du paiement
        if status_psp == 'success':
            _process_successful_payment(transaction, amount)
        elif status_psp == 'failed':
            _process_failed_payment(transaction)
        
        logger.info(f"Webhook traité avec succès: {provider_ref}")
        
        return JsonResponse({
            'message': 'Webhook reçu et traité',
            'webhook_id': webhook_event.id,
            'transaction_id': transaction.id
        }, status=200)
        
    except json.JSONDecodeError:
        logger.error("Webhook invalide: JSON malformé")
        return JsonResponse(
            {'error': 'JSON invalide'}, 
            status=400
        )
    except Exception as e:
        logger.error(f"Erreur lors du traitement du webhook: {e}")
        return JsonResponse(
            {'error': 'Erreur interne'}, 
            status=500
        )


@csrf_exempt
@require_http_methods(["POST"])
@secure_webhook(require_hmac=True, require_timestamp=False, require_ip_check=True)
@audit_log("Webhook de test reçu", "System")
def test_webhook(request):
    """
    Endpoint de test pour vérifier la configuration de sécurité
    
    En-têtes requis:
    - X-Webhook-Signature: Signature HMAC du payload
    - Content-Type: application/json
    """
    try:
        payload = json.loads(request.body)
        
        return JsonResponse({
            'message': 'Webhook de test reçu avec succès',
            'payload': payload,
            'timestamp': timezone.now().isoformat(),
            'security': 'HMAC verified'
        }, status=200)
        
    except Exception as e:
        logger.error(f"Erreur dans le webhook de test: {e}")
        return JsonResponse(
            {'error': 'Erreur interne'}, 
            status=500
        )


def _map_psp_status(psp_status: str) -> str:
    """Mappe les statuts PSP vers les statuts internes"""
    status_mapping = {
        'success': 'reussie',
        'failed': 'echouee',
        'cancelled': 'annulee',
        'pending': 'en_attente'
    }
    return status_mapping.get(psp_status.lower(), 'en_attente')


def _process_successful_payment(transaction: Transaction, amount: float):
    """Traite un paiement réussi"""
    try:
        # Mettre à jour le statut de la participation
        if transaction.participation:
            participation = transaction.participation
            participation.statut = 'validee'
            participation.save()
            
            logger.info(f"Participation {participation.id} validée pour {amount}")
            
            # TODO: Envoyer un email de confirmation
            # TODO: Générer un reçu PDF
            
    except Exception as e:
        logger.error(f"Erreur lors du traitement du paiement réussi: {e}")


def _process_failed_payment(transaction: Transaction):
    """Traite un paiement échoué"""
    try:
        # Mettre à jour le statut de la participation
        if transaction.participation:
            participation = transaction.participation
            participation.statut = 'refusee'
            participation.save()
            
            logger.info(f"Participation {participation.id} refusée")
            
            # TODO: Envoyer un email d'échec
            # TODO: Notifier l'utilisateur
            
    except Exception as e:
        logger.error(f"Erreur lors du traitement du paiement échoué: {e}")
