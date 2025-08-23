import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status

User = get_user_model()

@pytest.mark.django_db
class TestAuthentication:
    def setup_method(self):
        self.client = APIClient()
        self.user_data = {
            'email': 'test@example.com',
            'username': 'testuser',
            'password': 'TestPass123!',
            'first_name': 'Test',
            'last_name': 'User'
        }
        self.user = User.objects.create_user(**self.user_data)
        self.user.is_active = True
        self.user.save()

    def test_register_user(self):
        """Test user registration with valid data"""
        data = {
            'email': 'new@example.com',
            'username': 'newuser',
            'password': 'NewPass123!',
            'password2': 'NewPass123!',
            'first_name': 'New',
            'last_name': 'User'
        }
        response = self.client.post('/api/auth/register/', data)
        assert response.status_code == status.HTTP_201_CREATED
        assert 'access' in response.data
        assert 'refresh' in response.data

    def test_login_user(self):
        """Test user login with valid credentials"""
        data = {
            'email': self.user_data['email'],
            'password': self.user_data['password']
        }
        response = self.client.post('/api/auth/login/', data)
        assert response.status_code == status.HTTP_200_OK
        assert 'access' in response.data
        assert 'refresh' in response.data

    def test_refresh_token(self):
        """Test token refresh"""
        refresh = RefreshToken.for_user(self.user)
        data = {'refresh': str(refresh)}
        response = self.client.post('/api/auth/token/refresh/', data)
        assert response.status_code == status.HTTP_200_OK
        assert 'access' in response.data

    def test_protected_endpoint(self):
        """Test access to protected endpoint"""
        # Without token
        response = self.client.get('/api/user/me/')
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

        # With token
        refresh = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
        response = self.client.get('/api/user/me/')
        assert response.status_code == status.HTTP_200_OK
        assert response.data['email'] == self.user.email
