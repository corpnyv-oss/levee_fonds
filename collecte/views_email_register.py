from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from .serializers import UtilisateurRegistrationSerializer
from django.core.mail import send_mail
from django.conf import settings
import uuid

User = get_user_model()

class RegistrationViewSet(viewsets.GenericViewSet):
    serializer_class = UtilisateurRegistrationSerializer

    @action(detail=False, methods=['post'])
    def register(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        # Generate activation token (in prod, store in a separate model / send secure email link)
        token = str(uuid.uuid4())
        # attach token to user object for demo purposes (not persisted securely)
        user.activation_token = token
        try:
            send_mail(
                subject='Confirm your account',
                message=f'Voici votre token d\'activation (dev only): {token}',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email]
            )
        except Exception:
            pass
        return Response({'detail': 'Compte créé. Vérifie ton email.', 'activation_token': token}, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['post'], url_path='activate')
    def activate(self, request):
        email = request.data.get('email')
        token = request.data.get('token')
        if not email or not token:
            return Response({'detail': 'Email et token requis'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({'detail': 'Utilisateur inconnu'}, status=status.HTTP_404_NOT_FOUND)
        if getattr(user, 'activation_token', None) == token:
            user.is_active = True
            user.save()
            return Response({'detail': 'Compte activé'}, status=status.HTTP_200_OK)
        return Response({'detail': 'Token invalide'}, status=status.HTTP_400_BAD_REQUEST)
