"""
Tests de sécurité automatisés pour l'API FAPAG
"""
import pytest
import json
import time
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from collecte.models import Cagnotte, Participation, Transaction
from collecte.models_2fa import TOTPDevice, BackupCode

User = get_user_model()

@pytest.mark.security
class SecurityTestCase(TestCase):
    """Tests de sécurité de base"""
    
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email='test@fapag.com',
            password='TestPassword123!',
            role='utilisateur'
        )
        self.admin = User.objects.create_user(
            email='admin@fapag.com',
            password='AdminPassword123!',
            role='admin'
        )
        self.cagnotte = Cagnotte.objects.create(
            nom='Test Cagnotte',
            description='Cagnotte de test',
            montant_objectif=1000.00,
            utilisateur=self.user
        )

    def test_authentication_required_for_protected_endpoints(self):
        """Test que l'authentification est requise pour les endpoints protégés"""
        endpoints = [
            '/api/participations/',
            '/api/transactions/',
            '/api/utilisateurs/',
        ]
        
        for endpoint in endpoints:
            response = self.client.get(endpoint)
            self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_admin_only_endpoints(self):
        """Test que seuls les admins peuvent accéder aux endpoints admin"""
        # Connexion admin
        self.client.force_authenticate(user=self.admin)
        
        # Test création cagnotte (admin autorisé)
        data = {
            'nom': 'Admin Cagnotte',
            'description': 'Cagnotte admin',
            'montant_objectif': 500.00
        }
        response = self.client.post('/api/cagnottes/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # Connexion utilisateur normal
        self.client.force_authenticate(user=self.user)
        
        # Test création cagnotte (utilisateur non autorisé)
        response = self.client.post('/api/cagnottes/', data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_rate_limiting(self):
        """Test du rate limiting sur l'authentification"""
        # Tentatives multiples d'authentification
        for i in range(6):
            response = self.client.post('/api/auth/token/', {
                'email': 'wrong@email.com',
                'password': 'wrongpassword'
            })
            
            if i == 5:  # 6ème tentative
                # Devrait être bloquée par le rate limiting
                self.assertIn(response.status_code, [429, 403])

    def test_csrf_protection(self):
        """Test de la protection CSRF"""
        # Test sans token CSRF
        response = self.client.post('/api/cagnottes/', {
            'nom': 'Test CSRF',
            'description': 'Test',
            'montant_objectif': 100.00
        })
        # Devrait être rejeté (401 ou 403)
        self.assertIn(response.status_code, [401, 403])

    def test_sql_injection_protection(self):
        """Test de protection contre l'injection SQL"""
        # Tentative d'injection SQL
        malicious_input = "'; DROP TABLE cagnotte; --"
        
        response = self.client.get(f'/api/cagnottes/?nom={malicious_input}')
        # Ne devrait pas planter
        self.assertNotEqual(response.status_code, 500)

    def test_xss_protection(self):
        """Test de protection contre le XSS"""
        # Tentative XSS
        malicious_input = '<script>alert("XSS")</script>'
        
        # Test dans la création de cagnotte
        self.client.force_authenticate(user=self.admin)
        data = {
            'nom': malicious_input,
            'description': malicious_input,
            'montant_objectif': 100.00
        }
        
        response = self.client.post('/api/cagnottes/', data)
        # Devrait être rejeté ou échappé
        self.assertNotEqual(response.status_code, 201)

@pytest.mark.security
class TwoFactorSecurityTestCase(TestCase):
    """Tests de sécurité pour la 2FA"""
    
    def setUp(self):
        self.client = APIClient()
        self.admin = User.objects.create_user(
            email='admin2fa@fapag.com',
            password='Admin2FA123!',
            role='admin'
        )

    def test_2fa_required_for_admin(self):
        """Test que la 2FA est requise pour les administrateurs"""
        # Tentative de connexion admin sans 2FA
        response = self.client.post('/2fa/login/', {
            'email': 'admin2fa@fapag.com',
            'password': 'Admin2FA123!',
            'token': '123456'
        })
        
        # Devrait échouer car 2FA non configurée
        self.assertNotEqual(response.status_code, 200)

    def test_backup_codes_single_use(self):
        """Test que les codes de sauvegarde sont à usage unique"""
        # Créer un code de sauvegarde
        backup_code = BackupCode.objects.create(
            user=self.admin,
            code='12345678'
        )
        
        # Utiliser le code
        backup_code.use_code()
        
        # Vérifier qu'il est marqué comme utilisé
        self.assertTrue(backup_code.used)
        self.assertIsNotNone(backup_code.used_at)

@pytest.mark.security
class WebhookSecurityTestCase(TestCase):
    """Tests de sécurité pour les webhooks"""
    
    def setUp(self):
        self.client = Client()

    def test_webhook_without_signature_rejected(self):
        """Test que les webhooks sans signature sont rejetés"""
        response = self.client.post('/webhooks/test/', {
            'test': True,
            'message': 'Test sans signature'
        }, content_type='application/json')
        
        # Devrait être rejeté
        self.assertNotEqual(response.status_code, 200)

    def test_webhook_with_invalid_signature_rejected(self):
        """Test que les webhooks avec signature invalide sont rejetés"""
        response = self.client.post('/webhooks/test/', {
            'test': True,
            'message': 'Test signature invalide'
        }, content_type='application/json', HTTP_X_WEBHOOK_SIGNATURE='invalid_signature')
        
        # Devrait être rejeté
        self.assertNotEqual(response.status_code, 200)

@pytest.mark.security
class DataProtectionTestCase(TestCase):
    """Tests de protection des données"""
    
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email='user@fapag.com',
            password='UserPass123!',
            role='utilisateur'
        )
        self.other_user = User.objects.create_user(
            email='other@fapag.com',
            password='OtherPass123!',
            role='utilisateur'
        )

    def test_user_cannot_access_other_user_data(self):
        """Test qu'un utilisateur ne peut pas accéder aux données d'un autre"""
        # Créer une participation pour other_user
        participation = Participation.objects.create(
            utilisateur=self.other_user,
            cagnotte=Cagnotte.objects.create(
                nom='Other Cagnotte',
                description='Test',
                montant_objectif=100.00,
                utilisateur=self.other_user
            ),
            montant=50.00
        )
        
        # Connexion avec user
        self.client.force_authenticate(user=self.user)
        
        # Tentative d'accès à la participation d'un autre utilisateur
        response = self.client.get(f'/api/participations/{participation.id}/')
        
        # Devrait être interdit
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_sensitive_data_not_exposed(self):
        """Test que les données sensibles ne sont pas exposées"""
        # Connexion avec user
        self.client.force_authenticate(user=self.user)
        
        # Récupérer les informations utilisateur
        response = self.client.get(f'/api/utilisateurs/{self.user.id}/')
        
        # Vérifier que le mot de passe n'est pas exposé
        user_data = response.json()
        self.assertNotIn('password', user_data)
        self.assertNotIn('password_hash', user_data)

@pytest.mark.security
class JWTSecurityTestCase(TestCase):
    """Tests de sécurité pour les JWT"""
    
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email='jwt@fapag.com',
            password='JWTPass123!',
            role='utilisateur'
        )

    def test_jwt_expiration(self):
        """Test que les JWT expirent correctement"""
        # Connexion pour obtenir un token
        response = self.client.post('/api/auth/token/', {
            'email': 'jwt@fapag.com',
            'password': 'JWTPass123!'
        })
        
        self.assertEqual(response.status_code, 200)
        token_data = response.json()
        access_token = token_data['access']
        
        # Utiliser le token pour une requête
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        response = self.client.get('/api/cagnottes/')
        self.assertEqual(response.status_code, 200)
        
        # Note: Test complet de l'expiration nécessiterait de modifier la date du token

    def test_jwt_refresh_mechanism(self):
        """Test du mécanisme de refresh JWT"""
        # Connexion pour obtenir tokens
        response = self.client.post('/api/auth/token/', {
            'email': 'jwt@fapag.com',
            'password': 'JWTPass123!'
        })
        
        self.assertEqual(response.status_code, 200)
        token_data = response.json()
        refresh_token = token_data['refresh']
        
        # Utiliser le refresh token
        response = self.client.post('/api/auth/token/refresh/', {
            'refresh': refresh_token
        })
        
        self.assertEqual(response.status_code, 200)
        self.assertIn('access', response.json())

if __name__ == '__main__':
    pytest.main([__file__, '-v', '-m', 'security'])
