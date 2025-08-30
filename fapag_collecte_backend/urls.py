"""
URL configuration for fapag_collecte_backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from . import views
from django.views.decorators.csrf import ensure_csrf_cookie
from axes.decorators import axes_dispatch
from django.shortcuts import render
from django.conf import settings
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from collecte.webhook_views import psp_webhook, test_webhook
from collecte.views_2fa import (
    setup_2fa, verify_2fa_setup, login_with_2fa,
    verify_backup_code, get_2fa_status, regenerate_backup_codes
)
from collecte.views_registration import (
    public_registration, check_email_availability,
    validate_password_strength, registration_info
)

schema_view = get_schema_view(
    openapi.Info(
        title="API Collecte de Fonds",
        default_version='v1',
        description="Documentation de l'API de collecte de fonds",
    ),
    public=True,
    # Use a flat tuple of permission classes (avoid nested tuple)
    permission_classes=(permissions.AllowAny,) if settings.DEBUG else (permissions.IsAdminUser,),
    url="http://127.0.0.1:8081",
)

@ensure_csrf_cookie
@axes_dispatch
def locked_out_view(request, *args, **kwargs):    
    return render(request, 'account_locked.html', status=403)

urlpatterns = [
    # Page d'accueil (accessible sans authentification)
    path('', views.accueil, name='accueil'),
    # Health check
    path('healthz/', views.health, name='healthz'),
    # Page de verrouillage de compte (django-axes)
    path('locked-out/', locked_out_view, name='axes_locked_out'),
    
    # Administration
    path('admin/', admin.site.urls),
    # 2FA - Temporairement désactivé pour corriger les erreurs
    # path('account/', include('two_factor.urls')),
    
    # Webhooks sécurisés (en dehors de l'API DRF)
    path('webhooks/psp/', psp_webhook, name='psp_webhook'),
    path('webhooks/test/', test_webhook, name='test_webhook'),
    
    # 2FA - Système robuste et simple
    path('2fa/setup/', setup_2fa, name='setup_2fa'),
    path('2fa/verify-setup/', verify_2fa_setup, name='verify_2fa_setup'),
    path('2fa/login/', login_with_2fa, name='login_with_2fa'),
    path('2fa/backup/', verify_backup_code, name='verify_backup_code'),
    path('2fa/status/', get_2fa_status, name='get_2fa_status'),
    path('2fa/regenerate-backup/', regenerate_backup_codes, name='regenerate_backup_codes'),

    # Inscription publique sécurisée
    path('auth/register/', public_registration, name='public_registration'),
    path('auth/check-email/', check_email_availability, name='check_email_availability'),
    path('auth/validate-password/', validate_password_strength, name='validate_password_strength'),
    path('auth/registration-info/', registration_info, name='registration_info'),

    # API
    path('api/', include('collecte.urls')),
    # JWT Auth endpoints
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # Documentation (accessible sans authentification)
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
