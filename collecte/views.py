from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response

from rest_framework.permissions import AllowAny

class AccueilView(APIView):
    """
    Vue d'accueil de l'API de collecte de fonds
    """
    permission_classes = [AllowAny]  # Permet l'accès sans authentification
    
    def get(self, request):
        return Response({
            'message': 'Bienvenue sur l\'API de collecte de fonds FAPAG',
            'endpoints': {
                'documentation': '/swagger/',
                'api': '/api/',
                'admin': '/admin/'
            },
            'status': 'opérationnel'
        })
from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from django.conf import settings
from django.db import transaction
from django.utils import timezone
from datetime import timedelta
import json
import boto3
from botocore.exceptions import BotoCoreError, ClientError

from .models import Cagnotte, Participation, Transaction, WebhookEvent, Actualite, Utilisateur
from .serializers import (
    CagnotteSerializer, ParticipationSerializer, TransactionSerializer,
    WebhookEventSerializer, ActualiteSerializer, UtilisateurSerializer
)
from .permissions import IsAdminOrReadOnly, IsOwnerOrAdmin
from .payments.singpay import SingPayClient, verify_signature, extract_provider_refs

# Create your views here.

class CagnotteViewSet(viewsets.ModelViewSet):
    queryset = Cagnotte.objects.all()
    serializer_class = CagnotteSerializer
    permission_classes = [IsAdminOrReadOnly]

class ParticipationViewSet(viewsets.ModelViewSet):
    queryset = Participation.objects.all()
    serializer_class = ParticipationSerializer
    permission_classes = [IsOwnerOrAdmin]

    def get_queryset(self):
        user = self.request.user
        # Admin voit tout; sinon, seulement ses participations
        if user.is_authenticated and getattr(user, 'role', None) == 'admin':
            return super().get_queryset()
        return super().get_queryset().filter(utilisateur=user)

    def perform_create(self, serializer):
        # Empêche l'usurpation: force l'utilisateur courant
        serializer.save(utilisateur=self.request.user)

    @action(detail=True, methods=['post'], url_path='init-singpay')
    def init_singpay(self, request, pk=None):
        participation = self.get_object()
        client = SingPayClient()
        # Construire les URLs de retour et webhook
        return_url = settings.SINGPAY_RETURN_URL
        cancel_url = settings.SINGPAY_CANCEL_URL
        # Webhook URL absolue (suppose que le domaine est correctement configuré côté SingPay)
        webhook_url = request.build_absolute_uri('/api/webhooks/singpay/')

        # Créer paiement côté SingPay
        payload = client.create_payment(
            amount=str(participation.montant),
            reference=participation.reference,
            return_url=return_url,
            cancel_url=cancel_url,
            webhook_url=webhook_url,
        )

        # Extraire références provider et PSP depuis la réponse
        status, provider_ref, reference_psp = extract_provider_refs(payload)
        if not provider_ref and not reference_psp:
            return Response({'detail': 'Réponse SingPay invalide'}, status=502)

        # Créer/MàJ la transaction liée
        txn, _created = Transaction.objects.update_or_create(
            participation=participation,
            defaults={
                'reference_psp': reference_psp or participation.reference,
                'provider_ref': provider_ref or participation.reference,
                'statut': 'en_attente',
            }
        )

        payment_url = payload.get('payment_url') or payload.get('checkout_url')
        return Response({'payment_url': payment_url, 'transaction_id': txn.id})

class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = [IsOwnerOrAdmin]

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated and getattr(user, 'role', None) == 'admin':
            return super().get_queryset()
        # Restreindre aux transactions liées aux participations de l'utilisateur
        return super().get_queryset().filter(participation__utilisateur=user)

class WebhookEventViewSet(viewsets.ModelViewSet):
    queryset = WebhookEvent.objects.all()
    serializer_class = WebhookEventSerializer
    permission_classes = [permissions.IsAdminUser]

class ActualiteViewSet(viewsets.ModelViewSet):
    queryset = Actualite.objects.all()
    serializer_class = ActualiteSerializer
    permission_classes = [IsAdminOrReadOnly]

class UtilisateurViewSet(viewsets.ModelViewSet):
    queryset = Utilisateur.objects.all()
    serializer_class = UtilisateurSerializer
    permission_classes = [permissions.IsAdminUser]


class SingPayWebhookView(APIView):
    authentication_classes = []  # auth via signature
    permission_classes = []
    throttle_scope = 'webhooks'

    def post(self, request):
        raw = request.body
        try:
            data = json.loads(raw.decode('utf-8'))
        except Exception:
            return Response({'detail': 'Payload invalide'}, status=400)

        signature = request.headers.get('X-Signature') or request.headers.get('X-SingPay-Signature')
        if not verify_signature(raw, signature, settings.SINGPAY_WEBHOOK_SECRET):
            return Response({'detail': 'Signature invalide'}, status=401)

        # Anti-replay: timestamp header is required and must be fresh (<= 5 min)
        ts_header = request.headers.get('X-Timestamp') or request.headers.get('X-SingPay-Timestamp')
        if not ts_header:
            return Response({'detail': 'Horodatage manquant'}, status=400)
        try:
            ts = int(ts_header)
            now = int(timezone.now().timestamp())
            if abs(now - ts) > 300:  # 5 minutes window
                return Response({'detail': 'Horodatage expiré'}, status=400)
        except Exception:
            return Response({'detail': 'Horodatage invalide'}, status=400)

        status, provider_ref, reference_psp = extract_provider_refs(data)
        if not provider_ref and not reference_psp:
            return Response({'detail': 'Références introuvables'}, status=400)

        # Journaliser dès réception (statut 'recu') puis mettre à jour en 'traite' en fin
        ip = request.META.get('HTTP_X_FORWARDED_FOR', '').split(',')[0].strip() or request.META.get('REMOTE_ADDR')
        # IP allowlist if configured
        allowed_ips = getattr(settings, 'SINGPAY_ALLOWED_IPS', []) or []
        if allowed_ips and ip not in allowed_ips:
            return Response({'detail': 'IP non autorisée'}, status=403)
        event = None

        with transaction.atomic():
            # Verrouille la transaction DB pour éviter les courses si webhooks multiples
            txn = None
            if provider_ref:
                txn = Transaction.objects.select_for_update().filter(provider_ref=provider_ref).first()
            if not txn and reference_psp:
                txn = Transaction.objects.select_for_update().filter(reference_psp=reference_psp).first()
            if not txn:
                return Response({'detail': 'Transaction inconnue'}, status=404)

            # Créer l'event 'recu'
            event = WebhookEvent.objects.create(
                transaction=txn,
                payload=data,
                signature=signature or '',
                statut='recu',
                ip_source=ip
            )

            # Idempotence: si déjà finalisée, retourne 200 sans changer
            if txn.statut in ('reussie', 'echouee', 'annulee'):
                event.statut = 'traite'
                event.save(update_fields=['statut'])
                return Response({'detail': 'Déjà traité'}, status=200)

            # Mettre à jour la transaction et la participation
            mapping = {
                'paid': 'reussie',
                'success': 'reussie',
                'failed': 'echouee',
                'canceled': 'annulee',
                'pending': 'en_attente',
            }
            new_status = mapping.get((status or '').lower(), 'en_attente')
            txn.statut = new_status
            txn.save(update_fields=['statut'])

            part = txn.participation
            if new_status == 'reussie':
                part.statut = 'validee'
            elif new_status in ('echouee', 'annulee'):
                part.statut = 'refusee'
            part.save(update_fields=['statut'])

            # Marquer l'event comme traité
            event.statut = 'traite'
            event.save(update_fields=['statut'])

        return Response({'detail': 'OK'}, status=200)


def generate_presigned_url(key, expires_in=3600):
    s3_client = boto3.client(
        's3',
        endpoint_url=settings.AWS_S3_ENDPOINT_URL,
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        region_name=settings.AWS_S3_REGION_NAME,
    )
    try:
        url = s3_client.generate_presigned_url('get_object', Params={'Bucket': settings.AWS_STORAGE_BUCKET_NAME, 'Key': key}, ExpiresIn=expires_in)
        return url
    except (BotoCoreError, ClientError):
        return None
