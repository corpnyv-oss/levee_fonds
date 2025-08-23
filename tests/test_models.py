import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import timedelta
from decimal import Decimal
from collecte.models import Cagnotte, Participation, Categorie
from django.contrib.auth import get_user_model

User = get_user_model()

@pytest.mark.django_db
class TestCagnotteModel:
    def test_create_cagnotte(self):
        """Test creation of a cagnotte"""
        user = User.objects.create_user(
            email='creator@example.com',
            username='creator',
            password='testpass123'
        )
        
        # Create a test image file
        image = SimpleUploadedFile(
            name='test_image.jpg',
            content=open('collecte/tests/test_image.jpg', 'rb').read(),
            content_type='image/jpeg'
        )
        
        # Create a category
        category = Categorie.objects.create(nom='Test Category')
        
        # Create cagnotte
        cagnotte = Cagnotte.objects.create(
            titre='Test Cagnotte',
            description='Description de test',
            objectif=Decimal('1000.00'),
            createur=user,
            categorie=category,
            image=image,
            date_debut=timezone.now().date(),
            date_fin=(timezone.now() + timedelta(days=30)).date()
        )
        
        # Assertions
        assert str(cagnotte) == 'Test Cagnotte'
        assert cagnotte.montant_actuel == Decimal('0.00')
        assert cagnotte.est_active is True
        assert cagnotte.slug == 'test-cagnotte'
        
        # Test custom save method
        cagnotte.titre = 'Updated Title'
        cagnotte.save()
        assert cagnotte.slug == 'updated-title'
    
    def test_cagnotte_clean_method(self):
        """Test validation of cagnotte dates"""
        user = User.objects.create_user(
            email='creator@example.com',
            username='creator',
            password='testpass123'
        )
        
        # Test invalid date range
        with pytest.raises(ValidationError):
            cagnotte = Cagnotte(
                titre='Invalid Date Range',
                description='Test',
                objectif=Decimal('100.00'),
                createur=user,
                date_debut=(timezone.now() + timedelta(days=10)).date(),
                date_fin=timezone.now().date()
            )
            cagnotte.clean()

@pytest.mark.django_db
class TestParticipationModel:
    def test_create_participation(self):
        """Test creation of a participation"""
        user = User.objects.create_user(
            email='donor@example.com',
            username='donor',
            password='testpass123'
        )
        
        creator = User.objects.create_user(
            email='creator@example.com',
            username='creator',
            password='testpass123'
        )
        
        cagnotte = Cagnotte.objects.create(
            titre='Test Cagnotte',
            description='Description',
            objectif=Decimal('1000.00'),
            createur=creator,
            date_debut=timezone.now().date(),
            date_fin=(timezone.now() + timedelta(days=30)).date()
        )
        
        # Create participation
        participation = Participation.objects.create(
            cagnotte=cagnotte,
            donateur=user,
            montant=Decimal('50.00'),
            message='Bonne chance !',
            anonyme=False
        )
        
        # Assertions
        assert str(participation) == f'Participation de {user.username} à {cagnotte.titre}'
        assert participation.montant == Decimal('50.00')
        
        # Test montant_actuel update on cagnotte
        cagnotte.refresh_from_db()
        assert cagnotte.montant_actuel == Decimal('50.00')
    
    def test_participation_clean_method(self):
        """Test validation of participation amount"""
        user = User.objects.create_user(
            email='donor@example.com',
            username='donor',
            password='testpass123'
        )
        
        cagnotte = Cagnotte.objects.create(
            titre='Test Cagnotte',
            description='Description',
            objectif=Decimal('100.00'),
            createur=user,
            date_debut=timezone.now().date(),
            date_fin=(timezone.now() + timedelta(days=30)).date()
        )
        
        # Test negative amount
        with pytest.raises(ValidationError):
            participation = Participation(
                cagnotte=cagnotte,
                donateur=user,
                montant=Decimal('-10.00')
            )
            participation.clean()
            
        # Test amount too large
        with pytest.raises(ValidationError):
            participation = Participation(
                cagnotte=cagnotte,
                donateur=user,
                montant=Decimal('100000.00')
            )
            participation.clean()
