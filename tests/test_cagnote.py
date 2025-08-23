from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from collecte.models import Cagnotte, Participation, Transaction
from django.utils import timezone
from datetime import timedelta
from decimal import Decimal


class ValidationAndWebhookTests(TestCase):
    def setUp(self):
        User = get_user_model()
        # create_user for custom user model expects email as USERNAME_FIELD
        self.user = User.objects.create_user(email='test@example.com', username='testuser', password='testpass')
        self.cagnotte = Cagnotte.objects.create(
            titre='Test',
            description='desc',
            objectif=Decimal('100.00'),
            date_debut=timezone.now().date(),
            date_fin=(timezone.now() + timedelta(days=10)).date(),
            statut='active'
        )

    def test_cagnotte_date_validation(self):
        c = Cagnotte(
            titre='bad',
            description='bad',
            objectif=Decimal('10.00'),
            date_debut=timezone.now().date(),
            date_fin=(timezone.now() - timedelta(days=1)).date(),
        )
        with self.assertRaises(ValidationError):
            c.full_clean()

    def test_participation_montant_validator(self):
        p = Participation(
            utilisateur=self.user,
            cagnotte=self.cagnotte,
            montant=Decimal('0.00')  # invalide
        )
        with self.assertRaises(ValidationError):
            p.full_clean()

    def test_recu_pdf_size_and_extension_validator(self):
        small_pdf = SimpleUploadedFile("test.pdf", b"%PDF-1.4\n%...", content_type="application/pdf")
        p = Participation(
            utilisateur=self.user,
            cagnotte=self.cagnotte,
            montant=Decimal('10.00'),
            recu_pdf=small_pdf
        )
        # should validate (taille et extension ok)
        try:
            p.full_clean()
        except ValidationError as e:
            self.fail(f"Validation levée alors qu'elle ne devrait pas: {e}")

    def test_image_size_and_extension_validator(self):
        img = SimpleUploadedFile("img.png", b"\x89PNG\r\n\x1a\n...", content_type="image/png")
        self.cagnotte.image = img  # type: ignore[assignment]
        try:
            self.cagnotte.full_clean()
        except ValidationError as e:
            self.fail(f"Validation image levée: {e}")

    def test_webhook_idempotence_get_or_create(self):
        p = Participation.objects.create(utilisateur=self.user, cagnotte=self.cagnotte, montant=Decimal('5.00'))
        provider_ref = "webhook-12345"
        # Simule handler idempotent: get_or_create par provider_ref
        tx1, created1 = Transaction.objects.get_or_create(
            provider_ref=provider_ref,
            defaults={'participation': p, 'reference_psp': 'psp-1', 'statut': 'reussie'}
        )
        tx2, created2 = Transaction.objects.get_or_create(
            provider_ref=provider_ref,
            defaults={'participation': p, 'reference_psp': 'psp-1', 'statut': 'reussie'}
        )
        self.assertTrue(created1)
        self.assertFalse(created2)
        self.assertEqual(tx1.pk, tx2.pk)

    def test_recu_pdf_invalid_extension(self):
        bad_pdf = SimpleUploadedFile("not_a_pdf.txt", b"just text", content_type="text/plain")
        p = Participation(utilisateur=self.user, cagnotte=self.cagnotte, montant=Decimal('10.00'), recu_pdf=bad_pdf)
        with self.assertRaises(ValidationError):
            p.full_clean()

    def test_recu_pdf_too_large(self):
        # assume validator limits around 5MB; create >5MB to trigger
        large_content = b"a" * (6 * 1024 * 1024)
        large_pdf = SimpleUploadedFile("large.pdf", large_content, content_type="application/pdf")
        p = Participation(utilisateur=self.user, cagnotte=self.cagnotte, montant=Decimal('10.00'), recu_pdf=large_pdf)
        with self.assertRaises(ValidationError):
            p.full_clean()

    def test_image_invalid_extension(self):
        bmp = SimpleUploadedFile("img.bmp", b"BM...", content_type="image/bmp")
        self.cagnotte.image = bmp  # type: ignore[assignment]
        with self.assertRaises(ValidationError):
            self.cagnotte.full_clean()

    def test_cagnotte_objectif_must_be_positive(self):
        c = Cagnotte(
            titre='neg',
            description='invalid objectif',
            objectif=Decimal('-50.00'),
            date_debut=timezone.now().date(),
            date_fin=(timezone.now() + timedelta(days=1)).date(),
        )
        with self.assertRaises(ValidationError):
            c.full_clean()

    def test_transaction_create_with_different_provider_refs_creates_distinct(self):
        p = Participation.objects.create(utilisateur=self.user, cagnotte=self.cagnotte, montant=Decimal('5.00'))
        tx1 = Transaction.objects.create(provider_ref="ref-A", participation=p, reference_psp='psp-A', statut='reussie')
        tx2 = Transaction.objects.create(provider_ref="ref-B", participation=p, reference_psp='psp-B', statut='reussie')
        self.assertNotEqual(tx1.pk, tx2.pk)