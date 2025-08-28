import os
import certifi
from decouple import config
from fapag_collecte_backend.settings import *

# Configurer les certificats SSL
os.environ['SSL_CERT_FILE'] = certifi.where()

# Configuration de la base de données via DATABASE_URL
import dj_database_url

database_url = os.environ.get('DATABASE_URL')
if not database_url:
    raise ValueError("La variable d'environnement DATABASE_URL doit être définie")

DATABASES = {
    'default': dj_database_url.config(
        default=database_url,
        conn_max_age=600,
        conn_health_checks=True,
        ssl_require=True
    )
}

# Configuration spécifique à PostgreSQL pour le développement
DATABASES['default']['OPTIONS'] = {
    'connect_timeout': 10,
    'sslmode': 'require',
    'options': '-c search_path=public -c statement_timeout=30000ms',
}

# Désactiver la sécurité HTTPS en développement
SECURE_SSL_REDIRECT = False
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False
SECURE_HSTS_SECONDS = 0
SECURE_HSTS_INCLUDE_SUBDOMAINS = False
SECURE_HSTS_PRELOAD = False

# Autoriser toutes les origines pour le développement
CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True

# Désactiver la vérification du host
ALLOWED_HOSTS = ['*']

# Configuration pour les tests
TEST_RUNNER = 'django.test.runner.DiscoverRunner'
TESTING = True

# Configuration minimale pour le débogage
DEBUG = True

# Désactiver la mise en cache pendant les tests
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
}
INSTALLED_APPS = [
    # ... autres applications ...
    'sslserver',
]

# Désactiver django-axes pour le développement
AXES_ENABLED = False
