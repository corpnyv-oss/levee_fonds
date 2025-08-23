import hashlib
import hmac
import json
import logging
from typing import Dict, Tuple

import requests
from django.conf import settings
from django.urls import reverse

logger = logging.getLogger(__name__)


class SingPayClient:
    def __init__(self):
        self.base_url = settings.SINGPAY_BASE_URL.rstrip('/')
        self.api_key = settings.SINGPAY_API_KEY
        self.client_id = settings.SINGPAY_CLIENT_ID
        self.secret = settings.SINGPAY_SECRET

    def _headers(self) -> Dict[str, str]:
        # Adapter selon le schéma d'auth SingPay (Bearer/API-Key). Placeholder générique:
        return {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json',
            'X-Client-Id': self.client_id,
        }

    def create_payment(self, *, amount: str, reference: str, return_url: str, cancel_url: str, webhook_url: str) -> Dict:
        """
        Crée une session/paiement chez SingPay et renvoie la réponse JSON.
        Adapter l'endpoint/payload selon la documentation SingPay.
        """
        url = f"{self.base_url}/payments"
        payload = {
            'amount': amount,
            'currency': 'XAF',  # Adapter si nécessaire
            'reference': reference,
            'return_url': return_url,
            'cancel_url': cancel_url,
            'webhook_url': webhook_url,
        }
        logger.info("Creating SingPay payment: ref=%s amount=%s", reference, amount)
        resp = requests.post(url, headers=self._headers(), data=json.dumps(payload), timeout=30)
        resp.raise_for_status()
        return resp.json()


def verify_signature(raw_body: bytes, provided_signature: str, secret: str) -> bool:
    """
    Vérifie la signature HMAC du webhook. Adapter l'algorithme/format à SingPay.
    """
    if not provided_signature:
        return False
    computed = hmac.new(secret.encode(), raw_body, hashlib.sha256).hexdigest()
    return hmac.compare_digest(computed, provided_signature)


def extract_provider_refs(data: Dict) -> Tuple[str | None, str | None, str | None]:
    """
    Extrait (status, provider_ref, reference_psp) depuis la charge utile SingPay.
    Adapter les clés selon la doc SingPay.
    """
    status = data.get('status')
    provider_ref = data.get('provider_ref') or data.get('id')
    reference_psp = data.get('reference') or data.get('merchant_reference')
    return status, provider_ref, reference_psp
