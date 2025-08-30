"""
Modèle 2FA simple et robuste pour l'application
"""
import pyotp
import qrcode
import base64
import io
from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta

User = get_user_model()

class TOTPDevice(models.Model):
    """
    Modèle pour les appareils TOTP (Google Authenticator, etc.)
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='totp_devices')
    name = models.CharField(max_length=64, help_text="Nom de l'appareil (ex: iPhone, Android)")
    key = models.CharField(max_length=32, unique=True, help_text="Clé secrète TOTP")
    confirmed = models.BooleanField(default=False, help_text="Appareil confirmé par l'utilisateur")
    last_used = models.DateTimeField(null=True, blank=True, help_text="Dernière utilisation")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Appareil TOTP"
        verbose_name_plural = "Appareils TOTP"
        unique_together = ['user', 'name']
    
    def __str__(self):
        return f"{self.user.email} - {self.name}"
    
    def get_totp(self):
        """Retourne l'objet TOTP pour cet appareil"""
        return pyotp.TOTP(self.key)
    
    def verify_token(self, token):
        """
        Vérifie un token TOTP
        
        Args:
            token: Token à 6 chiffres
            
        Returns:
            bool: True si le token est valide
        """
        totp = self.get_totp()
        
        # Vérifier le token avec une fenêtre de tolérance de 1 période
        if totp.verify(token, valid_window=1):
            self.last_used = timezone.now()
            self.save(update_fields=['last_used'])
            return True
        return False
    
    def get_qr_code(self, email):
        """
        Génère un QR code pour l'ajout dans Google Authenticator
        
        Args:
            email: Email de l'utilisateur
            
        Returns:
            str: QR code en base64
        """
        totp = self.get_totp()
        
        # Créer l'URI TOTP standard
        uri = totp.provisioning_uri(
            name=email,
            issuer_name="FAPAG Collecte"
        )
        
        # Générer le QR code
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(uri)
        qr.make(fit=True)
        
        # Créer l'image
        img = qr.make_image(fill_color="black", back_color="white")
        
        # Convertir en base64
        buffer = io.BytesIO()
        img.save(buffer, format='PNG')
        img_str = base64.b64encode(buffer.getvalue()).decode()
        
        return f"data:image/png;base64,{img_str}"
    
    @classmethod
    def create_for_user(cls, user, name="Default"):
        """
        Crée un nouvel appareil TOTP pour un utilisateur
        
        Args:
            user: Utilisateur Django
            name: Nom de l'appareil
            
        Returns:
            TOTPDevice: Nouvel appareil créé
        """
        # Générer une nouvelle clé secrète
        key = pyotp.random_base32()
        
        # Créer l'appareil
        device = cls.objects.create(
            user=user,
            name=name,
            key=key
        )
        
        return device


class BackupCode(models.Model):
    """
    Codes de sauvegarde pour récupérer l'accès en cas de perte de l'appareil 2FA
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='backup_codes')
    code = models.CharField(max_length=10, unique=True, help_text="Code de sauvegarde à 8 chiffres")
    used = models.BooleanField(default=False, help_text="Code déjà utilisé")
    used_at = models.DateTimeField(null=True, blank=True, help_text="Date d'utilisation")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Code de sauvegarde"
        verbose_name_plural = "Codes de sauvegarde"
    
    def __str__(self):
        return f"{self.user.email} - {self.code}"
    
    def use_code(self):
        """Marque le code comme utilisé"""
        self.used = True
        self.used_at = timezone.now()
        self.save(update_fields=['used', 'used_at'])
    
    @classmethod
    def generate_for_user(cls, user, count=8):
        """
        Génère des codes de sauvegarde pour un utilisateur
        
        Args:
            user: Utilisateur Django
            count: Nombre de codes à générer
            
        Returns:
            list: Liste des codes générés
        """
        import secrets
        
        codes = []
        for _ in range(count):
            # Générer un code à 8 chiffres
            code = ''.join(secrets.choice('0123456789') for _ in range(8))
            
            # S'assurer qu'il est unique
            while cls.objects.filter(code=code).exists():
                code = ''.join(secrets.choice('0123456789') for _ in range(8))
            
            # Créer le code
            backup_code = cls.objects.create(user=user, code=code)
            codes.append(backup_code.code)
        
        return codes


class LoginAttempt(models.Model):
    """
    Suivi des tentatives de connexion pour la sécurité
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='login_attempts')
    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField(blank=True)
    success = models.BooleanField(default=False)
    requires_2fa = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Tentative de connexion"
        verbose_name_plural = "Tentatives de connexion"
        ordering = ['-created_at']
    
    def __str__(self):
        status = "SUCCESS" if self.success else "FAILED"
        return f"{self.user.email} - {status} - {self.ip_address}"
    
    @classmethod
    def record_attempt(cls, user, ip_address, user_agent="", success=False, requires_2fa=False):
        """
        Enregistre une tentative de connexion
        
        Args:
            user: Utilisateur Django
            ip_address: Adresse IP de la tentative
            user_agent: User-Agent du navigateur
            success: Si la connexion a réussi
            requires_2fa: Si la 2FA était requise
        """
        return cls.objects.create(
            user=user,
            ip_address=ip_address,
            user_agent=user_agent,
            success=success,
            requires_2fa=requires_2fa
        )
