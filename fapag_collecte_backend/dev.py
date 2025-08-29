from .settings import *

# Désactiver toutes les vérifications de sécurité pour le développement
DEBUG = True
ALLOWED_HOSTS = ['*']

# Désactiver HTTPS
SECURE_SSL_REDIRECT = False
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False
SECURE_PROXY_SSL_HEADER = None

# Désactiver la vérification du host
USE_X_FORWARDED_HOST = False
SECURE_REDIRECT_EXEMPT = ['.*']

# Désactiver la validation du host
import django.http.request
django.http.request.host_validation_re = lambda *args, **kwargs: True

# Désactiver la vérification CSRF
CSRF_TRUSTED_ORIGINS = ['http://*', 'https://*']
