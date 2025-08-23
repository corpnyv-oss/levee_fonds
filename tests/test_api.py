import pytest
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from typing import Any


@pytest.mark.django_db
def test_cagnottes_permissions():
    User = get_user_model()
    admin = User.objects.create_user(email="admin@test.com", username="admin", password="adminpass", role="admin")
    client_user = User.objects.create_user(email="client@test.com", username="client", password="clientpass", role="utilisateur")

    api = APIClient()

    # Non authentifié
    response: Any = api.get('/api/cagnottes/')
    assert response.status_code == 200

    # Client authentifié
    api.force_authenticate(user=client_user)
    response: Any = api.post('/api/cagnottes/', {"titre": "Test", "description": "desc", "objectif": 1000, "date_debut": "2025-08-18", "date_fin": "2025-09-18"})
    assert response.status_code == 403

    # Admin authentifié
    api.force_authenticate(user=admin)
    response: Any = api.post('/api/cagnottes/', {"titre": "Test", "description": "desc", "objectif": 1000, "date_debut": "2025-08-18", "date_fin": "2025-09-18"})
    assert response.status_code == 201