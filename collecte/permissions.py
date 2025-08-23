from rest_framework import permissions

class IsAdminOrReadOnly(permissions.BasePermission):
    """Autorise la modification seulement aux admins, lecture pour tous."""
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_authenticated and getattr(request.user, 'role', None) == 'admin' 


class IsOwnerOrAdmin(permissions.BasePermission):
    """Autorise l'accès si l'utilisateur est admin ou propriétaire de la ressource."""

    def has_object_permission(self, request, view, obj):
        # Admin full access
        if request.user.is_authenticated and getattr(request.user, 'role', None) == 'admin':
            return True

        # SAFE methods: require authentication but allow if owner
        if request.method in permissions.SAFE_METHODS:
            return self._is_owner(request.user, obj)

        # Write methods: owner only
        return self._is_owner(request.user, obj)

    def _is_owner(self, user, obj):
        """
        Détermine si `user` est propriétaire de `obj`.
        Tente plusieurs chemins standard avant de gérer les cas spécifiques.
        """
        # Attributs usuels
        for attr in ('utilisateur', 'user', 'owner', 'created_by'):
            if hasattr(obj, attr):
                return getattr(obj, attr) == user

        # Cas Transaction: propriétaire via la Participation liée
        if hasattr(obj, 'participation') and hasattr(obj.participation, 'utilisateur'):
            return obj.participation.utilisateur == user

        # Cas WebhookEvent -> Transaction -> Participation -> utilisateur
        if hasattr(obj, 'transaction') and hasattr(obj.transaction, 'participation'):
            part = obj.transaction.participation
            if hasattr(part, 'utilisateur'):
                return part.utilisateur == user

        return False