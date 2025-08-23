from django.contrib.auth import get_user_model
from rest_framework_simplejwt.authentication import default_authentication_rule as default_rule

def custom_authentication_rule(user):
    """
    Règle d'authentification personnalisée pour JWT qui vérifie que l'utilisateur est actif.
    """
    # Vérifie que l'utilisateur existe et est actif
    if user is None or not user.is_active:
        return False
    
    # Vérifications supplémentaires si nécessaire
    # Par exemple, vérifier si le compte n'est pas verrouillé
    if hasattr(user, 'is_locked') and user.is_locked:
        return False
        
    return True
