"""
Paramètres de production pour le projet FAPAG Collecte.
Toutes les configurations sensibles sont gérées via des variables d'environnement.
"""

import os
import sys
from pathlib import Path
from decouple import config, Csv
import dj_database_url
from .settings import *
import logging

# Sentry (optionnel mais recommandé)
try:
    import sentry_sdk
    from sentry_sdk.integrations.django import DjangoIntegration
except Exception:
    sentry_sdk = None

# Détecter si on est sur Render
IS_RENDER = os.getenv('RENDER', '').lower() == 'true'

# ===== CONFIGURATION DE BASE =====
# ---------------------------------
SECRET_KEY = config('SECRET_KEY')
DEBUG = config('DEBUG', default=False, cast=bool)
# Liste des hôtes autorisés
RENDER_EXTERNAL_HOSTNAME = os.environ.get('RENDER_EXTERNAL_HOSTNAME')
if RENDER_EXTERNAL_HOSTNAME:
    ALLOWED_HOSTS = [RENDER_EXTERNAL_HOSTNAME, 'localhost', '127.0.0.1']
else:
    ALLOWED_HOSTS = config('ALLOWED_HOSTS', cast=Csv())

# ===== BASE DE DONNÉES =====
# ---------------------------
DATABASES = {
    'default': dj_database_url.config(
        default=config('DATABASE_URL'),
        conn_max_age=config('DB_CONN_MAX_AGE', default=600, cast=int),
        ssl_require=config('DB_SSL_REQUIRE', default=True, cast=bool)
    )
}

# ===== FICHIERS STATIQUES ET MÉDIAS =====
# ---------------------------------------
STATIC_URL = config('STATIC_URL', default='/static/')
STATIC_ROOT = os.path.join(BASE_DIR, config('STATIC_ROOT', default='staticfiles'))
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

# Configuration WhiteNoise pour les fichiers statiques
if not DEBUG:
    STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
    MIDDLEWARE.insert(1, 'whitenoise.middleware.WhiteNoiseMiddleware')

# Configuration des médias
MEDIA_URL = config('MEDIA_URL', default='/media/')
MEDIA_ROOT = os.path.join(BASE_DIR, config('MEDIA_ROOT', default='media'))

# Configuration du stockage des médias pour la production
if IS_RENDER:
    # Sur Render, on utilise le stockage local pour les médias
    DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'

# ===== SÉCURITÉ =====
# --------------------
SECURE_SSL_REDIRECT = config('SECURE_SSL_REDIRECT', default=not DEBUG, cast=bool)
SESSION_COOKIE_SECURE = config('SESSION_COOKIE_SECURE', default=not DEBUG, cast=bool)
CSRF_COOKIE_SECURE = config('CSRF_COOKIE_SECURE', default=not DEBUG, cast=bool)
SECURE_BROWSER_XSS_FILTER = config('SECURE_BROWSER_XSS_FILTER', default=True, cast=bool)
SECURE_CONTENT_TYPE_NOSNIFF = config('SECURE_CONTENT_TYPE_NOSNIFF', default=True, cast=bool)
X_FRAME_OPTIONS = config('X_FRAME_OPTIONS', default='DENY')
SECURE_HSTS_SECONDS = config('SECURE_HSTS_SECONDS', default=31536000, cast=int)  # 1 an
SECURE_HSTS_INCLUDE_SUBDOMAINS = config('SECURE_HSTS_INCLUDE_SUBDOMAINS', default=True, cast=bool)
SECURE_HSTS_PRELOAD = config('SECURE_HSTS_PRELOAD', default=True, cast=bool)
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Configuration CSRF pour Render
if IS_RENDER:
    CSRF_TRUSTED_ORIGINS = [
        f'https://{RENDER_EXTERNAL_HOSTNAME}',
        'http://localhost:3000',
        'http://127.0.0.1:3000'
    ]
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_SSL_REDIRECT = True

# Configuration CSRF par défaut
CSRF_TRUSTED_ORIGINS = config('CSRF_TRUSTED_ORIGINS', default='', cast=Csv())
CSRF_COOKIE_HTTPONLY = config('CSRF_COOKIE_HTTPONLY', default=True, cast=bool)
CSRF_COOKIE_SAMESITE = config('CSRF_COOKIE_SAMESITE', default='Lax')
CSRF_USE_SESSIONS = config('CSRF_USE_SESSIONS', default=False, cast=bool)

# Configuration des sessions
SESSION_COOKIE_AGE = config('SESSION_COOKIE_AGE', default=1209600, cast=int)  # 2 semaines
SESSION_COOKIE_HTTPONLY = config('SESSION_COOKIE_HTTPONLY', default=True, cast=bool)
SESSION_COOKIE_SAMESITE = config('SESSION_COOKIE_SAMESITE', default='Lax')
SESSION_SAVE_EVERY_REQUEST = config('SESSION_SAVE_EVERY_REQUEST', default=False, cast=bool)

# ===== CONTENT SECURITY POLICY (django-csp) =====
# -----------------------------------------------
# Activer une CSP stricte en production. Ajuster selon les besoins front/CDN.
CSP_DEFAULT_SRC = ("'self'",)
CSP_SCRIPT_SRC = ("'self'",)
CSP_STYLE_SRC = ("'self'",)
CSP_IMG_SRC = ("'self'", 'data:')
CSP_FONT_SRC = ("'self'", 'data:')
CSP_CONNECT_SRC = ("'self'",)
CSP_FRAME_ANCESTORS = ("'none'",)
CSP_BASE_URI = ("'self'",)
CSP_OBJECT_SRC = ("'none'",)
CSP_FRAME_SRC = ("'none'",)
CSP_FORM_ACTION = ("'self'",)
CSP_UPGRADE_INSECURE_REQUESTS = True

# ===== MESSAGERIE =====
# ---------------------
EMAIL_BACKEND = config('EMAIL_BACKEND', default='django.core.mail.backends.console.EmailBackend')
EMAIL_HOST = config('EMAIL_HOST', default='')
EMAIL_PORT = config('EMAIL_PORT', default=587, cast=int)
EMAIL_USE_TLS = config('EMAIL_USE_TLS', default=True, cast=bool)
EMAIL_HOST_USER = config('EMAIL_HOST_USER', default='')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD', default='')
DEFAULT_FROM_EMAIL = config('DEFAULT_FROM_EMAIL', default='webmaster@example.com')
SERVER_EMAIL = config('SERVER_EMAIL', default=DEFAULT_FROM_EMAIL)

# ===== CORS =====
# ----------------
CORS_ALLOW_ALL_ORIGINS = False  # Interdit en production
CORS_ALLOWED_ORIGINS = config('CORS_ALLOWED_ORIGINS', default='', cast=Csv())
CORS_ALLOW_CREDENTIALS = config('CORS_ALLOW_CREDENTIALS', default=True, cast=bool)
if not DEBUG and not CORS_ALLOWED_ORIGINS:
    import warnings
    warnings.warn("CORS_ALLOWED_ORIGINS est vide en production. Définissez vos domaines autorisés.")

# ===== FEATURES FLAGS =====
# --------------------------
# Contrôle de l'exposition de la documentation API en production
ENABLE_API_DOCS = config('ENABLE_API_DOCS', default=False, cast=bool)

# ===== CACHE =====
# ----------------
CACHES = {
    'default': {
        'BACKEND': config('CACHE_BACKEND', default='django.core.cache.backends.locmem.LocMemCache'),
        'LOCATION': config('CACHE_LOCATION', default='unique-snowflake'),
    }
}

# Configuration pour Redis si utilisé
if 'redis' in CACHES['default']['BACKEND'].lower():
    CACHES['default']['OPTIONS'] = {
        'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        'PASSWORD': config('REDIS_PASSWORD', default=''),
    }

# ===== CELERY =====
# ------------------
CELERY_BROKER_URL = config('CELERY_BROKER_URL', default='redis://localhost:6379/0')
CELERY_RESULT_BACKEND = config('CELERY_RESULT_BACKEND', default=CELERY_BROKER_URL)
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = config('TIME_ZONE', default='UTC')

# ===== WHITENOISE =====
# ----------------------
if 'whitenoise.middleware.WhiteNoiseMiddleware' not in MIDDLEWARE:
    MIDDLEWARE.insert(1, 'whitenoise.middleware.WhiteNoiseMiddleware')

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
WHITENOISE_MAX_AGE = config('WHITENOISE_MAX_AGE', default=31536000, cast=int)  # 1 an

# ===== ADMINISTRATION =====
# -------------------------
ADMIN_ENABLED = config('ADMIN_ENABLED', default=DEBUG, cast=bool)
# Désactiver l'interface d'administration en production si nécessaire
if not ADMIN_ENABLED and 'django.contrib.admin' in INSTALLED_APPS:
    INSTALLED_APPS.remove('django.contrib.admin')
    MIDDLEWARE = [m for m in MIDDLEWARE if not m.startswith('django.contrib.')]

# Configuration des logs pour la production
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}

# ===== CONFIGURATION DU STOCKAGE =====
# ------------------------------------
# Configuration pour Amazon S3 (optionnel)
if config('USE_S3', default='False', cast=bool):
    DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
    AWS_ACCESS_KEY_ID = config('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = config('AWS_SECRET_ACCESS_KEY')
    AWS_STORAGE_BUCKET_NAME = config('AWS_STORAGE_BUCKET_NAME')
    AWS_S3_REGION_NAME = config('AWS_S3_REGION_NAME', default=None)
    AWS_S3_CUSTOM_DOMAIN = config('AWS_S3_CUSTOM_DOMAIN', default=None)
    AWS_DEFAULT_ACL = config('AWS_DEFAULT_ACL', default='private')
    AWS_QUERYSTRING_AUTH = config('AWS_QUERYSTRING_AUTH', default=True, cast=bool)
    AWS_QUERYSTRING_EXPIRE = config('AWS_QUERYSTRING_EXPIRE', default=3600, cast=int)
    AWS_S3_FILE_OVERWRITE = config('AWS_S3_FILE_OVERWRITE', default=False, cast=bool)
    AWS_S3_OBJECT_PARAMETERS = {
        'CacheControl': f'max-age={config("AWS_CACHE_MAX_AGE", default=86400, cast=int)}',
    }

# ===== LOGGING =====
# -------------------
LOG_LEVEL = config('LOG_LEVEL', default='INFO' if not DEBUG else 'DEBUG')
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
        'file': {
            'level': LOG_LEVEL,
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(BASE_DIR, 'logs', 'django.log'),
            'maxBytes': 1024 * 1024 * 5,  # 5MB
            'backupCount': 5,
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'file'],
            'level': LOG_LEVEL,
            'propagate': True,
        },
    },
}

# Créer le dossier de logs s'il n'existe pas
os.makedirs(os.path.join(BASE_DIR, 'logs'), exist_ok=True)

# ===== SENTRY INIT =====
# ----------------------
SENTRY_DSN = config('SENTRY_DSN', default='')
if sentry_sdk and SENTRY_DSN:
    sentry_sdk.init(
        dsn=SENTRY_DSN,
        integrations=[DjangoIntegration()],
        traces_sample_rate=config('SENTRY_TRACES_SAMPLE_RATE', default=0.0, cast=float),
        send_default_pii=config('SENTRY_SEND_PII', default=False, cast=bool),
        environment=config('SENTRY_ENVIRONMENT', default='production'),
    )

