import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from decimal import Decimal
from collecte.models import Cagnotte, Participation
from unittest.mock import patch, MagicMock

User = get_user_model()

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def test_user():
    user = User.objects.create_user(
        email='user@example.com',
        username='testuser',
        password='testpass123',
        first_name='Test',
        last_name='User'
    )
    user.is_active = True
    user.save()
    return user

@pytest.fixture
def test_cagnotte(test_user):
    return Cagnotte.objects.create(
        titre='Test Cagnotte',
        description='Description de test',
        objectif=Decimal('1000.00'),
        createur=test_user,
        date_debut='2025-01-01',
        date_fin='2025-12-31'
    )

@pytest.mark.django_db
class TestPayments:
    def test_create_payment_intent(self, api_client, test_user, test_cagnotte):
        """Test creation of a payment intent"""
        # Get JWT token
        refresh = RefreshToken.for_user(test_user)
        api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
        
        # Test data
        data = {
            'cagnotte_id': test_cagnotte.id,
            'montant': '100.00',
            'moyen_paiement': 'mobile_money',
            'telephone': '237612345678',
            'operateur': 'mtn'
        }
        
        # Mock the SingPay API
        with patch('payments.singpay.SingPayClient.create_payment') as mock_create_payment:
            # Configure the mock
            mock_create_payment.return_value = {
                'success': True,
                'payment_intent_id': 'pi_test123',
                'client_secret': 'secret_test_123',
                'status': 'requires_payment_method'
            }
            
            # Make the request
            response = api_client.post('/api/payments/create-intent/', data, format='json')
            
            # Assertions
            assert response.status_code == status.HTTP_201_CREATED
            assert 'payment_intent_id' in response.data
            assert 'client_secret' in response.data
            
            # Verify the payment was created in the database
            assert Participation.objects.filter(
                cagnotte=test_cagnotte,
                donateur=test_user,
                montant=Decimal('100.00')
            ).exists()
    
    def test_webhook_handler(self, api_client):
        """Test webhook handler for payment events"""
        # Test data
        webhook_payload = {
            'event': 'payment.succeeded',
            'data': {
                'id': 'evt_test123',
                'payment_intent': 'pi_test123',
                'amount': 10000,  # in smallest currency unit (100.00 XAF)
                'currency': 'xaf',
                'status': 'succeeded',
                'metadata': {
                    'cagnotte_id': '1',
                    'user_id': '1'
                }
            }
        }
        
        # Mock the webhook signature verification
        with patch('payments.views.verify_webhook_signature', return_value=True):
            # Make the request
            response = api_client.post(
                '/api/webhooks/singpay/',
                data=webhook_payload,
                format='json',
                HTTP_X_SINGPAY_SIGNATURE='test_signature'
            )
            
            # Assertions
            assert response.status_code == status.HTTP_200_OK
            assert response.data['status'] == 'processed'
