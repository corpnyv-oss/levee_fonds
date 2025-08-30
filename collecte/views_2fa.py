"""
Vues pour la gestion de la 2FA
"""
import json
import logging
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.contrib.auth import authenticate, login, get_user_model
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models_2fa import TOTPDevice, BackupCode, LoginAttempt
from .security import webhook_security

logger = logging.getLogger(__name__)
User = get_user_model()


@csrf_exempt
@require_http_methods(["POST"])
def setup_2fa(request):
    """
    Configure la 2FA pour un utilisateur
    
    Corps de la requête:
    {
        "email": "user@example.com",
        "password": "password123"
    }
    
    Réponse:
    {
        "qr_code": "data:image/png;base64,...",
        "secret_key": "ABCDEFGHIJKLMNOP",
        "backup_codes": ["12345678", "87654321", ...]
    }
    """
    try:
        data = json.loads(request.body)
        email = data.get('email')
        password = data.get('password')
        
        if not email or not password:
            return JsonResponse(
                {'error': 'Email et mot de passe requis'}, 
                status=400
            )
        
        # Authentifier l'utilisateur
        user = authenticate(request, username=email, password=password)
        if not user:
            return JsonResponse(
                {'error': 'Identifiants invalides'}, 
                status=401
            )
        
        # Vérifier que l'utilisateur est admin (2FA obligatoire pour les admins)
        if getattr(user, 'role', None) != 'admin':
            return JsonResponse(
                {'error': '2FA requis uniquement pour les administrateurs'}, 
                status=403
            )
        
        # Vérifier si la 2FA est déjà configurée
        existing_device = TOTPDevice.objects.filter(user=user, confirmed=True).first()
        if existing_device:
            return JsonResponse(
                {'error': '2FA déjà configuré pour cet utilisateur'}, 
                status=400
            )
        
        # Créer un nouvel appareil TOTP
        device = TOTPDevice.create_for_user(user, "Default")
        
        # Générer des codes de sauvegarde
        backup_codes = BackupCode.generate_for_user(user, count=8)
        
        # Enregistrer la tentative
        client_ip = webhook_security._get_client_ip(request)
        LoginAttempt.record_attempt(
            user=user,
            ip_address=client_ip,
            user_agent=request.META.get('HTTP_USER_AGENT', ''),
            success=True,
            requires_2fa=True
        )
        
        logger.info(f"2FA configuré pour l'utilisateur {user.email}")
        
        return JsonResponse({
            'message': '2FA configuré avec succès',
            'qr_code': device.get_qr_code(user.email),
            'secret_key': device.key,
            'backup_codes': backup_codes,
            'instructions': [
                '1. Scannez le QR code avec Google Authenticator',
                '2. Entrez le code à 6 chiffres pour confirmer',
                '3. Conservez les codes de sauvegarde en lieu sûr'
            ]
        }, status=200)
        
    except json.JSONDecodeError:
        return JsonResponse({'error': 'JSON invalide'}, status=400)
    except Exception as e:
        logger.error(f"Erreur lors de la configuration 2FA: {e}")
        return JsonResponse({'error': 'Erreur interne'}, status=500)


@csrf_exempt
@require_http_methods(["POST"])
def verify_2fa_setup(request):
    """
    Vérifie et confirme la configuration 2FA
    
    Corps de la requête:
    {
        "email": "user@example.com",
        "password": "password123",
        "token": "123456"
    }
    """
    try:
        data = json.loads(request.body)
        email = data.get('email')
        password = data.get('password')
        token = data.get('token')
        
        if not all([email, password, token]):
            return JsonResponse(
                {'error': 'Email, mot de passe et token requis'}, 
                status=400
            )
        
        # Authentifier l'utilisateur
        user = authenticate(request, username=email, password=password)
        if not user:
            return JsonResponse(
                {'error': 'Identifiants invalides'}, 
                status=401
            )
        
        # Trouver l'appareil TOTP non confirmé
        device = TOTPDevice.objects.filter(user=user, confirmed=False).first()
        if not device:
            return JsonResponse(
                {'error': 'Aucun appareil 2FA en attente de confirmation'}, 
                status=400
            )
        
        # Vérifier le token
        if not device.verify_token(token):
            return JsonResponse(
                {'error': 'Token 2FA invalide'}, 
                status=400
            )
        
        # Confirmer l'appareil
        device.confirmed = True
        device.save(update_fields=['confirmed'])
        
        logger.info(f"2FA confirmé pour l'utilisateur {user.email}")
        
        return JsonResponse({
            'message': '2FA confirmé avec succès',
            'device_name': device.name
        }, status=200)
        
    except json.JSONDecodeError:
        return JsonResponse({'error': 'JSON invalide'}, status=400)
    except Exception as e:
        logger.error(f"Erreur lors de la confirmation 2FA: {e}")
        return JsonResponse({'error': 'Erreur interne'}, status=500)


@csrf_exempt
@require_http_methods(["POST"])
def login_with_2fa(request):
    """
    Connexion avec vérification 2FA
    
    Corps de la requête:
    {
        "email": "user@example.com",
        "password": "password123",
        "token": "123456"
    }
    """
    try:
        data = json.loads(request.body)
        email = data.get('email')
        password = data.get('password')
        token = data.get('token')
        
        if not all([email, password, token]):
            return JsonResponse(
                {'error': 'Email, mot de passe et token 2FA requis'}, 
                status=400
            )
        
        # Authentifier l'utilisateur
        user = authenticate(request, username=email, password=password)
        if not user:
            client_ip = webhook_security._get_client_ip(request)
            LoginAttempt.record_attempt(
                user=User.objects.filter(email=email).first() or User(),
                ip_address=client_ip,
                user_agent=request.META.get('HTTP_USER_AGENT', ''),
                success=False,
                requires_2fa=True
            )
            return JsonResponse(
                {'error': 'Identifiants invalides'}, 
                status=401
            )
        
        # Vérifier si la 2FA est requise (pour les admins)
        if getattr(user, 'role', None) == 'admin':
            # Trouver l'appareil TOTP confirmé
            device = TOTPDevice.objects.filter(user=user, confirmed=True).first()
            if not device:
                return JsonResponse(
                    {'error': '2FA requis mais non configuré'}, 
                    status=400
                )
            
            # Vérifier le token 2FA
            if not device.verify_token(token):
                client_ip = webhook_security._get_client_ip(request)
                LoginAttempt.record_attempt(
                    user=user,
                    ip_address=client_ip,
                    user_agent=request.META.get('HTTP_USER_AGENT', ''),
                    success=False,
                    requires_2fa=True
                )
                return JsonResponse(
                    {'error': 'Token 2FA invalide'}, 
                    status=401
                )
        
        # Connexion réussie
        login(request, user)
        
        # Enregistrer la tentative réussie
        client_ip = webhook_security._get_client_ip(request)
        LoginAttempt.record_attempt(
            user=user,
            ip_address=client_ip,
            user_agent=request.META.get('HTTP_USER_AGENT', ''),
            success=True,
            requires_2fa=True
        )
        
        logger.info(f"Connexion 2FA réussie pour {user.email}")
        
        return JsonResponse({
            'message': 'Connexion réussie',
            'user': {
                'id': user.id,
                'email': user.email,
                'role': getattr(user, 'role', 'utilisateur')
            }
        }, status=200)
        
    except json.JSONDecodeError:
        return JsonResponse({'error': 'JSON invalide'}, status=400)
    except Exception as e:
        logger.error(f"Erreur lors de la connexion 2FA: {e}")
        return JsonResponse({'error': 'Erreur interne'}, status=500)


@csrf_exempt
@require_http_methods(["POST"])
def verify_backup_code(request):
    """
    Vérification avec un code de sauvegarde
    
    Corps de la requête:
    {
        "email": "user@example.com",
        "password": "password123",
        "backup_code": "12345678"
    }
    """
    try:
        data = json.loads(request.body)
        email = data.get('email')
        password = data.get('password')
        backup_code = data.get('backup_code')
        
        if not all([email, password, backup_code]):
            return JsonResponse(
                {'error': 'Email, mot de passe et code de sauvegarde requis'}, 
                status=400
            )
        
        # Authentifier l'utilisateur
        user = authenticate(request, username=email, password=password)
        if not user:
            return JsonResponse(
                {'error': 'Identifiants invalides'}, 
                status=401
            )
        
        # Vérifier le code de sauvegarde
        backup_code_obj = BackupCode.objects.filter(
            user=user,
            code=backup_code,
            used=False
        ).first()
        
        if not backup_code_obj:
            return JsonResponse(
                {'error': 'Code de sauvegarde invalide ou déjà utilisé'}, 
                status=400
            )
        
        # Marquer le code comme utilisé
        backup_code_obj.use_code()
        
        # Connexion réussie
        login(request, user)
        
        # Enregistrer la tentative réussie
        client_ip = webhook_security._get_client_ip(request)
        LoginAttempt.record_attempt(
            user=user,
            ip_address=client_ip,
            user_agent=request.META.get('HTTP_USER_AGENT', ''),
            success=True,
            requires_2fa=True
        )
        
        logger.info(f"Connexion avec code de sauvegarde pour {user.email}")
        
        return JsonResponse({
            'message': 'Connexion réussie avec code de sauvegarde',
            'user': {
                'id': user.id,
                'email': user.email,
                'role': getattr(user, 'role', 'utilisateur')
            }
        }, status=200)
        
    except json.JSONDecodeError:
        return JsonResponse({'error': 'JSON invalide'}, status=400)
    except Exception as e:
        logger.error(f"Erreur lors de la vérification du code de sauvegarde: {e}")
        return JsonResponse({'error': 'Erreur interne'}, status=500)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_2fa_status(request):
    """
    Récupère le statut 2FA de l'utilisateur connecté
    """
    try:
        user = request.user
        
        # Vérifier si la 2FA est configurée
        device = TOTPDevice.objects.filter(user=user, confirmed=True).first()
        
        # Compter les codes de sauvegarde non utilisés
        unused_backup_codes = BackupCode.objects.filter(user=user, used=False).count()
        
        return Response({
            'has_2fa': bool(device),
            'device_name': device.name if device else None,
            'last_used': device.last_used.isoformat() if device and device.last_used else None,
            'backup_codes_remaining': unused_backup_codes,
            'requires_2fa': getattr(user, 'role', None) == 'admin'
        })
        
    except Exception as e:
        logger.error(f"Erreur lors de la récupération du statut 2FA: {e}")
        return Response({'error': 'Erreur interne'}, status=500)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def regenerate_backup_codes(request):
    """
    Régénère les codes de sauvegarde pour l'utilisateur connecté
    """
    try:
        user = request.user
        
        # Supprimer les anciens codes
        BackupCode.objects.filter(user=user).delete()
        
        # Générer de nouveaux codes
        new_codes = BackupCode.generate_for_user(user, count=8)
        
        logger.info(f"Codes de sauvegarde régénérés pour {user.email}")
        
        return Response({
            'message': 'Codes de sauvegarde régénérés',
            'backup_codes': new_codes
        })
        
    except Exception as e:
        logger.error(f"Erreur lors de la régénération des codes de sauvegarde: {e}")
        return Response({'error': 'Erreur interne'}, status=500)
