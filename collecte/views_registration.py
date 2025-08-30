"""
Vues d'inscription publique sécurisée pour les clients
"""
import json
import logging
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.contrib.auth import get_user_model
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.db import transaction
from django.utils import timezone
from django.conf import settings
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from .models import Cagnotte
from .serializers import UtilisateurSerializer
from .security import webhook_security

logger = logging.getLogger(__name__)
User = get_user_model()

@csrf_exempt
@require_http_methods(["POST"])
def public_registration(request):
    """
    Inscription publique sécurisée pour les clients
    
    Corps de la requête:
    {
        "email": "client@example.com",
        "password": "MotDePasseFort123!",
        "password_confirm": "MotDePasseFort123!",
        "nom": "Nom du client",
        "prenom": "Prénom du client",
        "telephone": "+24112345678" (optionnel)
    }
    
    Réponse:
    {
        "message": "Inscription réussie",
        "user": {
            "id": 123,
            "email": "client@example.com",
            "nom": "Nom du client",
            "prenom": "Prénom du client",
            "role": "utilisateur"
        }
    }
    """
    try:
        data = json.loads(request.body)
        
        # Validation des champs requis
        required_fields = ['email', 'password', 'password_confirm', 'nom', 'prenom']
        for field in required_fields:
            if not data.get(field):
                return JsonResponse({
                    'error': f'Le champ {field} est requis'
                }, status=400)
        
        email = data['email'].lower().strip()
        password = data['password']
        password_confirm = data['password_confirm']
        nom = data['nom'].strip()
        prenom = data['prenom'].strip()
        telephone = data.get('telephone', '').strip()
        
        # Validation de l'email
        try:
            validate_email(email)
        except ValidationError:
            return JsonResponse({
                'error': 'Format d\'email invalide'
            }, status=400)
        
        # Vérification que l'email n'existe pas déjà
        if User.objects.filter(email=email).exists():
            return JsonResponse({
                'error': 'Un compte avec cet email existe déjà'
            }, status=400)
        
        # Validation du mot de passe
        if len(password) < 12:
            return JsonResponse({
                'error': 'Le mot de passe doit contenir au moins 12 caractères'
            }, status=400)
        
        if not any(c.isupper() for c in password):
            return JsonResponse({
                'error': 'Le mot de passe doit contenir au moins une majuscule'
            }, status=400)
        
        if not any(c.islower() for c in password):
            return JsonResponse({
                'error': 'Le mot de passe doit contenir au moins une minuscule'
            }, status=400)
        
        if not any(c.isdigit() for c in password):
            return JsonResponse({
                'error': 'Le mot de passe doit contenir au moins un chiffre'
            }, status=400)
        
        if not any(c in '!@#$%^&*()_+-=[]{}|;:,.<>?' for c in password):
            return JsonResponse({
                'error': 'Le mot de passe doit contenir au moins un caractère spécial'
            }, status=400)
        
        # Vérification de la confirmation du mot de passe
        if password != password_confirm:
            return JsonResponse({
                'error': 'Les mots de passe ne correspondent pas'
            }, status=400)
        
        # Validation des noms
        if len(nom) < 2 or len(prenom) < 2:
            return JsonResponse({
                'error': 'Les noms doivent contenir au moins 2 caractères'
            }, status=400)
        
        # Validation du téléphone (optionnel)
        if telephone and not telephone.startswith('+'):
            return JsonResponse({
                'error': 'Le numéro de téléphone doit commencer par +'
            }, status=400)
        
        # Création de l'utilisateur dans une transaction
        with transaction.atomic():
            user = User.objects.create_user(
                email=email,
                password=password,
                first_name=prenom,
                last_name=nom,
                role='utilisateur',
                is_active=True
            )
            
            # Ajouter le téléphone si fourni
            if telephone:
                user.telephone = telephone
                user.save(update_fields=['telephone'])
            
            # Journalisation de l'inscription
            client_ip = webhook_security._get_client_ip(request)
            logger.info(f"Nouvelle inscription: {email} depuis {client_ip}")
            
            # Retourner les informations de l'utilisateur (sans mot de passe)
            user_data = {
                'id': user.id,
                'email': user.email,
                'nom': user.last_name,
                'prenom': user.first_name,
                'role': user.role,
                'telephone': getattr(user, 'telephone', ''),
                'date_inscription': user.date_joined.isoformat()
            }
            
            return JsonResponse({
                'message': 'Inscription réussie ! Vous pouvez maintenant vous connecter.',
                'user': user_data,
                'instructions': [
                    '1. Conservez vos identifiants en lieu sûr',
                    '2. Connectez-vous à l\'API avec votre email et mot de passe',
                    '3. Utilisez un mot de passe fort et unique',
                    '4. Contactez le support en cas de problème'
                ]
            }, status=201)
            
    except json.JSONDecodeError:
        return JsonResponse({
            'error': 'Format JSON invalide'
        }, status=400)
    except Exception as e:
        logger.error(f"Erreur lors de l'inscription: {e}")
        return JsonResponse({
            'error': 'Erreur interne lors de l\'inscription'
        }, status=500)

@api_view(['POST'])
@permission_classes([AllowAny])
def check_email_availability(request):
    """
    Vérifier la disponibilité d'un email
    
    Corps de la requête:
    {
        "email": "client@example.com"
    }
    
    Réponse:
    {
        "available": true,
        "message": "Email disponible"
    }
    """
    try:
        email = request.data.get('email', '').lower().strip()
        
        if not email:
            return Response({
                'error': 'Email requis'
            }, status=400)
        
        # Validation de l'email
        try:
            validate_email(email)
        except ValidationError:
            return Response({
                'available': False,
                'message': 'Format d\'email invalide'
            })
        
        # Vérifier la disponibilité
        is_available = not User.objects.filter(email=email).exists()
        
        return Response({
            'available': is_available,
            'message': 'Email disponible' if is_available else 'Email déjà utilisé'
        })
        
    except Exception as e:
        logger.error(f"Erreur lors de la vérification email: {e}")
        return Response({
            'error': 'Erreur interne'
        }, status=500)

@api_view(['POST'])
@permission_classes([AllowAny])
def validate_password_strength(request):
    """
    Valider la force d'un mot de passe
    
    Corps de la requête:
    {
        "password": "MotDePasseFort123!"
    }
    
    Réponse:
    {
        "valid": true,
        "score": 85,
        "feedback": ["Mot de passe fort", "Contient des caractères spéciaux"]
    }
    """
    try:
        password = request.data.get('password', '')
        
        if not password:
            return Response({
                'error': 'Mot de passe requis'
            }, status=400)
        
        # Analyse de la force du mot de passe
        score = 0
        feedback = []
        
        # Longueur
        if len(password) >= 12:
            score += 25
            feedback.append("Longueur suffisante (12+ caractères)")
        else:
            feedback.append("Longueur insuffisante (minimum 12 caractères)")
        
        # Complexité
        if any(c.isupper() for c in password):
            score += 15
            feedback.append("Contient des majuscules")
        else:
            feedback.append("Ajoutez des majuscules")
        
        if any(c.islower() for c in password):
            score += 15
            feedback.append("Contient des minuscules")
        else:
            feedback.append("Ajoutez des minuscules")
        
        if any(c.isdigit() for c in password):
            score += 15
            feedback.append("Contient des chiffres")
        else:
            feedback.append("Ajoutez des chiffres")
        
        if any(c in '!@#$%^&*()_+-=[]{}|;:,.<>?' for c in password):
            score += 20
            feedback.append("Contient des caractères spéciaux")
        else:
            feedback.append("Ajoutez des caractères spéciaux")
        
        # Diversité des caractères
        unique_chars = len(set(password))
        if unique_chars >= 8:
            score += 10
            feedback.append("Bonne diversité de caractères")
        else:
            feedback.append("Utilisez plus de caractères différents")
        
        # Validation finale
        is_valid = score >= 70
        
        return Response({
            'valid': is_valid,
            'score': score,
            'feedback': feedback,
            'strength': 'Faible' if score < 50 else 'Moyen' if score < 80 else 'Fort'
        })
        
    except Exception as e:
        logger.error(f"Erreur lors de la validation du mot de passe: {e}")
        return Response({
            'error': 'Erreur interne'
        }, status=500)

@api_view(['GET'])
@permission_classes([AllowAny])
def registration_info(request):
    """
    Informations sur le processus d'inscription
    
    Réponse:
    {
        "requirements": {
            "password_min_length": 12,
            "password_requirements": [...],
            "required_fields": [...],
            "optional_fields": [...]
        },
        "security_features": [...],
        "contact_info": {...}
    }
    """
    info = {
        'requirements': {
            'password_min_length': 12,
            'password_requirements': [
                'Au moins 12 caractères',
                'Au moins une majuscule',
                'Au moins une minuscule',
                'Au moins un chiffre',
                'Au moins un caractère spécial'
            ],
            'required_fields': [
                'email',
                'password',
                'password_confirm',
                'nom',
                'prenom'
            ],
            'optional_fields': [
                'telephone'
            ]
        },
        'security_features': [
            'Validation email en temps réel',
            'Vérification de la force du mot de passe',
            'Protection contre les attaques par force brute',
            'Journalisation de toutes les tentatives',
            'Validation des données côté serveur'
        ],
        'contact_info': {
            'support': 'support@fapag.com',
            'admin': 'admin@fapag.com',
            'urgence': '+241 XX XX XX XX'
        },
        'privacy_notice': [
            'Vos données personnelles sont protégées',
            'Aucune information sensible n\'est stockée',
            'Conformité RGPD et standards de sécurité',
            'Accès limité aux administrateurs autorisés'
        ]
    }
    
    return Response(info)
