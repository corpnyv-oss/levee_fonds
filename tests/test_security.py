import json
import pytest
from typing import Any
from django.contrib.auth import get_user_model
from django.test import override_settings
from rest_framework.test import APIClient
from collecte.models import Cagnotte, Participation, Transaction


@pytest.mark.django_db
def test_participations_filtered_by_owner():
    User = get_user_model()
    alice = User.objects.create_user(email="alice@test.com", username="alice", password="pass", role="utilisateur")
    bob = User.objects.create_user(email="bob@test.com", username="bob", password="pass", role="utilisateur")

    # Préparer une cagnotte (créée par admin pour simplicité)
    admin = User.objects.create_user(email="admin@test.com", username="admin", password="adminpass", role="admin")
    cagnotte = Cagnotte.objects.create(titre="C1", description="d", objectif=1000, date_debut="2025-01-01", date_fin="2025-12-31", statut='active')

    # Participations pour chaque user
    pa: Any = Participation.objects.create(utilisateur=alice, cagnotte=cagnotte, montant=100, statut='en_attente', reference='ref-alice')
    pb: Any = Participation.objects.create(utilisateur=bob, cagnotte=cagnotte, montant=200, statut='en_attente', reference='ref-bob')

    api = APIClient()
    api.force_authenticate(user=alice)
    res: Any = api.get('/api/participations/')
    assert res.status_code == 200
    ids = [p['id'] for p in (res.json() or [])]
    assert pa.id in ids
    assert pb.id not in ids  # Alice ne voit pas la participation de Bob


@pytest.mark.django_db
def test_transactions_filtered_by_owner():
    User = get_user_model()
    alice = User.objects.create_user(email="alice@test.com", username="alice", password="pass", role="utilisateur")
    bob = User.objects.create_user(email="bob@test.com", username="bob", password="pass", role="utilisateur")
    cagnotte = Cagnotte.objects.create(titre="C1", description="d", objectif=1000, date_debut="2025-01-01", date_fin="2025-12-31", statut='active')

    pa = Participation.objects.create(utilisateur=alice, cagnotte=cagnotte, montant=100, statut='en_attente', reference='ref-alice')
    pb = Participation.objects.create(utilisateur=bob, cagnotte=cagnotte, montant=200, statut='en_attente', reference='ref-bob')

    ta: Any = Transaction.objects.create(participation=pa, reference_psp='psp-a', provider_ref='prov-a', statut='en_attente')
    tb: Any = Transaction.objects.create(participation=pb, reference_psp='psp-b', provider_ref='prov-b', statut='en_attente')

    api = APIClient()
    api.force_authenticate(user=alice)
    res: Any = api.get('/api/transactions/')
    assert res.status_code == 200
    ids = [t['id'] for t in (res.json() or [])]
    assert ta.id in ids
    assert tb.id not in ids  # Alice ne voit pas la transaction de Bob


@pytest.mark.django_db
@override_settings(SINGPAY_WEBHOOK_SECRET='testsecret')
def test_singpay_webhook_signature_invalid_returns_401():
    # Payload minimal
    payload = {"status": "paid", "provider_ref": "p1", "reference": "r1"}

    api = APIClient()
    # Signature manquante/incorrecte
    res: Any = api.post('/api/webhooks/singpay/', data=json.dumps(payload), content_type='application/json', HTTP_X_SIGNATURE='bad')
    assert res.status_code == 401
