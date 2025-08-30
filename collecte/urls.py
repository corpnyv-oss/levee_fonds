from rest_framework.routers import DefaultRouter
from .views import (
    CagnotteViewSet, ParticipationViewSet, TransactionViewSet,
    WebhookEventViewSet, ActualiteViewSet, UtilisateurViewSet
)
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)
from django.urls import path

router = DefaultRouter()
router.register(r'cagnottes', CagnotteViewSet)
router.register(r'participations', ParticipationViewSet)
router.register(r'transactions', TransactionViewSet)
router.register(r'webhooks', WebhookEventViewSet)
router.register(r'actualites', ActualiteViewSet)
router.register(r'utilisateurs', UtilisateurViewSet)

urlpatterns = router.urls
urlpatterns += [
    # Authentification JWT
    path('auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]