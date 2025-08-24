"""
Exceptions personnalisées pour l'API
"""
from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status

def custom_exception_handler(exc, context):
    # Appel au gestionnaire d'exceptions par défaut
    response = exception_handler(exc, context)

    # Si c'est une erreur non gérée par DRF
    if response is None:
        return Response(
            {
                'error': 'Une erreur serveur est survenue',
                'status_code': status.HTTP_500_INTERNAL_SERVER_ERROR,
                'details': str(exc) if str(exc) else 'Aucun détail disponible'
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    # Personnalisation des erreurs d'authentification
    if response.status_code == status.HTTP_401_UNAUTHORIZED:
        response.data = {
            'error': 'Non authentifié',
            'status_code': status.HTTP_401_UNAUTHORIZED,
            'details': 'Les informations d\'authentification n\'ont pas été fournies.'
        }
    
    # Personnalisation des erreurs d'autorisation
    elif response.status_code == status.HTTP_403_FORBIDDEN:
        response.data = {
            'error': 'Permission refusée',
            'status_code': status.HTTP_403_FORBIDDEN,
            'details': 'Vous n\'avez pas la permission d\'effectuer cette action.'
        }
    
    # Personnalisation des erreurs 404
    elif response.status_code == status.HTTP_404_NOT_FOUND:
        response.data = {
            'error': 'Non trouvé',
            'status_code': status.HTTP_404_NOT_FOUND,
            'details': 'La ressource demandée n\'a pas été trouvée.'
        }
    
    # Pour toutes les autres erreurs
    else:
        response.data = {
            'error': response.data.get('detail', 'Une erreur est survenue'),
            'status_code': response.status_code,
            'details': response.data
        }

    return response
