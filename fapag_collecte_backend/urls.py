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
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.views.generic import TemplateView
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from . import views
from axes.decorators import axes_dispatch
from django.views.decorators.csrf import ensure_csrf_cookie

# Activation de l'authentification à deux facteurs
from two_factor.urls import urlpatterns as tf_urls
# Désactivé temporairement pour les migrations
# from two_factor.gateways.twilio.urls import urlpatterns as tf_twilio_urls
# from two_factor.gateways.twilio.views import PhoneSetupView, PhoneDeleteView

schema_view = get_schema_view(
    openapi.Info(
        title="API Collecte de Fonds",
        default_version='v1',
        description="Documentation de l'API de collecte de fonds",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

@ensure_csrf_cookie
@axes_dispatch
def locked_out_view(request, *args, **kwargs):    
    return render(request, 'account_locked.html', status=403)

# URLs pour l'authentification à deux facteurs
two_factor_patterns = [
    # Désactivé temporairement pour les migrations
    # path('account/two_factor/twilio/setup/', PhoneSetupView.as_view(), name='phone_setup'),
    # path('account/two_factor/twilio/setup/<int:pk>/', PhoneSetupView.as_view(), name='phone_setup'),
    # path('account/two_factor/twilio/delete/<int:pk>/', PhoneDeleteView.as_view(), name='phone_delete'),
    path('', include(tf_urls)),
    # Désactivé temporairement pour les migrations
    # path('', include(tf_twilio_urls)),
    # Vues personnalisées pour la configuration des numéros de téléphone (désactivées pour les migrations)
    # path('phone/setup/', PhoneSetupView.as_view(), name='phone_setup'),
    # path('phone/delete/<int:pk>/', PhoneDeleteView.as_view(), name='phone_delete'),
]

urlpatterns = [
    # Page d'accueil (accessible sans authentification)
    path('', views.accueil, name='accueil'),
    
    # Authentification à deux facteurs
    path('account/', include(two_factor_patterns)),
    
    # Page de verrouillage de compte
    path('locked-out/', locked_out_view, name='account_locked'),
    
    # Administration
    path('admin/', admin.site.urls),
    
    # API
    path('api/', include('collecte.urls')),
    
    # Documentation (accessible sans authentification)
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
