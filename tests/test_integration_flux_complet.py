import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta
from collecte.models import Cagnotte, Participation, Transaction, WebhookEvent
import json

User = get_user_model()

@pytest.mark.django_db
def test_flux_complet_cagnotte():
    # 1. Création d'un utilisateur admin
    admin = User.objects.create_superuser(
        email='admin@example.com',
        username='admin',
        password='testpass123',
        role='admin'
    )
    
    # 2. Création d'un utilisateur standard
    user = User.objects.create_user(
        email='user@example.com',
        username='user',
        password='testpass123',
        role='utilisateur'
    )
    
    client = APIClient()
    
    # 3. Authentification de l'admin
    client.force_authenticate(user=admin)
    
    # 4. Création d'une cagnotte
    cagnotte_data = {
        'titre': 'Test Cagnotte',
        'description': 'Description de test',
        'montant_objectif': 1000.00,
        'date_limite': (timezone.now() + timedelta(days=30)).isoformat(),
        'est_publique': True
    }
    
    response = client.post(
        reverse('cagnotte-list'),
        data=json.dumps(cagnotte_data),
        content_type='application/json'
    )
    assert response.status_code == 201
    cagnotte_id = response.data['id']
    
    # 5. Authentification en tant qu'utilisateur standard
    client.force_authenticate(user=user)
    
    # 6. Participation à la cagnotte
    participation_data = {
        'cagnotte': cagnotte_id,
        'montant': 100.00,
        'moyen_paiement': 'carte_credit'
    }
    
    response = client.post(
        reverse('participation-list'),
        data=json.dumps(participation_data),
        content_type='application/json'
    )
    assert response.status_code == 201
    participation_id = response.data['id']
    
    # 7. Simulation d'un webhook de paiement réussi
    client.force_authenticate(user=None)  # Aucune authentification pour les webhooks
    
    webhook_data = {
        'transaction_id': 'test_transaction_123',
        'status': 'success',
        'amount': '100.00',
        'currency': 'XAF',
        'timestamp': timezone.now().isoformat(),
        'metadata': {
            'participation_id': participation_id,
            'provider_ref': 'test_provider_ref_123'
        }
    }
    
    # Signature du webhook (à implémenter selon votre logique)
    signature = 'test_signature'
    
    response = client.post(
        reverse('webhook-payment'),
        data=json.dumps(webhook_data),
        content_type='application/json',
        HTTP_X_SIGNATURE=signature
    )
    assert response.status_code == 200
    
    # 8. Vérification des données
    participation = Participation.objects.get(id=participation_id)
    assert participation.statut == 'validee'
    
    transaction = Transaction.objects.filter(participation=participation).first()
    assert transaction is not None
    assert transaction.statut == 'reussie'
    
    webhook = WebhookEvent.objects.filter(transaction=transaction).first()
    assert webhook is not None
    assert webhook.statut == 'traite'
