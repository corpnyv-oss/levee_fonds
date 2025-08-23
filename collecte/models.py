from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, FileExtensionValidator
from django.core.exceptions import ValidationError
import uuid
from django.contrib.auth.models import AbstractUser
from simple_history.models import HistoricalRecords
from django.utils import timezone


# Named helper to generate a string UUID for defaults (serializable by migrations)
def generate_reference():
    return str(uuid.uuid4())

try:
    from .utils.clam_scan import scan_file
except Exception:
    # fallback scanner that does nothing in dev if ClamAV not available
    def scan_file(file):
        return {'infected': False, 'reason': None}

# validators personnalisés
def validate_file_size(file):
    max_size = getattr(settings, 'MAX_UPLOAD_SIZE', 5 * 1024 * 1024)  # 5 MB par défaut
    if file and hasattr(file, 'size') and file.size > max_size:
        raise ValidationError(f"Fichier trop volumineux. Taille max : {max_size // (1024*1024)} MB.")

def validate_file_mime(file, allowed_content_types):
    # Essaie de vérifier le content_type si disponible (UploadedFile), sinon se rabat sur l'extension
    if not file:
        return
    content_type = getattr(file, 'content_type', None)
    if content_type:
        if content_type not in allowed_content_types:
            raise ValidationError("Type de fichier non autorisé.")
    else:
        # fallback: vérifie l'extension
        name = getattr(file, 'name', '')
        if not any(name.lower().endswith(ext) for ext in ['.pdf', '.jpg', '.jpeg', '.png']):
            raise ValidationError("Extension de fichier non autorisée.")

# Fonctions nommées utilisables par les migrations (éviter lambda non sérialisable)
def validate_image_mime(file):
    return validate_file_mime(file, ['image/jpeg', 'image/png'])

def validate_pdf_mime(file):
    return validate_file_mime(file, ['application/pdf'])

# Create your models here.

class Cagnotte(models.Model):
    STATUT_CHOICES = [
        ('active', 'Active'),
        ('terminee', 'Terminée'),
        ('en_attente', 'En attente'),
        ('archivee', 'Archivée'),
    ]

    titre = models.CharField(max_length=255)
    description = models.TextField()
    objectif = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0.01)])
    image = models.ImageField(
        upload_to='cagnottes/', blank=True, null=True,
        validators=[
            FileExtensionValidator(['jpg', 'jpeg', 'png']),
            validate_file_size,
            validate_image_mime,
        ]
    )
    date_debut = models.DateField()
    date_fin = models.DateField()
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='en_attente')
    cree_le = models.DateTimeField(auto_now_add=True)
    modifie_le = models.DateTimeField(auto_now=True)

    def clean(self):
        if self.date_debut and self.date_fin and self.date_fin < self.date_debut:
            raise ValidationError("La date de fin doit être postérieure ou égale à la date de début.")
        super().clean()

    def __str__(self):
        return self.titre

class Participation(models.Model):
    STATUT_CHOICES = [
        ('en_attente', 'En attente'),
        ('validee', 'Validée'),
        ('refusee', 'Refusée'),
        ('remboursee', 'Remboursée'),
    ]

    utilisateur = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='participations')
    cagnotte = models.ForeignKey('Cagnotte', on_delete=models.CASCADE, related_name='participations')
    montant = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0.01)])
    date_participation = models.DateTimeField(auto_now_add=True)
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='en_attente')
    recu_pdf = models.FileField(
        upload_to='recu_pdfs/', blank=True, null=True,
        validators=[
            FileExtensionValidator(['pdf']),
            validate_file_size,
            validate_pdf_mime,
        ]
    )
    # Use CharField for reference to remain compatible with existing tests and
    # legacy data that use human-readable refs like 'ref-alice'. Provide a
    # default generator so missing references are auto-filled (like previous
    # UUIDField behavior).
    reference = models.CharField(max_length=100, unique=True, default=generate_reference)
    history = HistoricalRecords()

    def save(self, *args, **kwargs):
        # Vérifie le fichier uploadé avec ClamAV avant sauvegarde (si disponible)
        file_field = getattr(self, 'recu_pdf', None)
        if file_field:
            try:
                result = scan_file(file_field)
                if result and result.get('infected'):
                    raise ValidationError("Le fichier contient un malware (ClamAV).")
            except ValidationError:
                raise
            except Exception:
                # En dev, ne pas bloquer si le scanner échoue - journaliser en prod
                pass
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.utilisateur} - {self.cagnotte} - {self.montant} FCFA"

class Transaction(models.Model):
    STATUT_CHOICES = [
        ('en_attente', 'En attente'),
        ('reussie', 'Réussie'),
        ('echouee', 'Échouée'),
        ('annulee', 'Annulée'),
    ]

    # Allow multiple transactions for a single participation (attempts, retries, different PSP refs)
    participation = models.ForeignKey('Participation', on_delete=models.PROTECT, related_name='transactions')
    reference_psp = models.CharField(max_length=100, unique=True, db_index=True)
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='en_attente')
    horodatage = models.DateTimeField(auto_now_add=True)
    provider_ref = models.CharField(max_length=100, unique=True, db_index=True, help_text="Pour l'idempotence des webhooks")
    history = HistoricalRecords()

    def __str__(self):
        return f"Transaction {self.reference_psp} - {self.statut}"

class WebhookEvent(models.Model):
    STATUT_CHOICES = [
        ('recu', 'Reçu'),
        ('traite', 'Traité'),
        ('erreur', 'Erreur'),
    ]

    transaction = models.ForeignKey('Transaction', on_delete=models.CASCADE, related_name='webhooks')
    payload = models.JSONField()
    signature = models.CharField(max_length=255)
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='recu')
    horodatage = models.DateTimeField(auto_now_add=True)
    ip_source = models.GenericIPAddressField(blank=True, null=True)
    history = HistoricalRecords()

    def __str__(self):
        return f"Webhook {self.transaction.reference_psp} - {self.statut}"

class Actualite(models.Model):
    cagnotte = models.ForeignKey('Cagnotte', on_delete=models.CASCADE, related_name='actualites')
    titre = models.CharField(max_length=255)
    contenu = models.TextField()
    image = models.ImageField(upload_to='actualites/', blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.titre} ({self.cagnotte})"

class Utilisateur(AbstractUser):
    ROLES = [
        ('utilisateur', 'Utilisateur'),
        ('admin', 'Administrateur'),
    ]
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, choices=ROLES, default='utilisateur')
    deux_facteurs_active = models.BooleanField(default=False)

    # token d'activation persisté (utilisé pour activation par email)
    activation_token = models.UUIDField(null=True, blank=True, db_index=True, editable=False)
    activation_token_created_at = models.DateTimeField(null=True, blank=True)
    
    # Ajout de related_name personnalisés pour éviter les conflits
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        related_name='collecte_utilisateur_set',
        related_query_name='utilisateur',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name='collecte_utilisateur_set',
        related_query_name='utilisateur',
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def generate_activation_token(self):
        token = uuid.uuid4()
        self.activation_token = token
        self.activation_token_created_at = timezone.now()
        self.is_active = False
        # sauvegarder seulement les champs modifiés
        self.save(update_fields=['activation_token', 'activation_token_created_at', 'is_active'])
        return str(token)

    def __str__(self):
        return f"{self.email} ({self.role})"
