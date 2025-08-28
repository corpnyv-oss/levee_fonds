"""
ASGI config for fapag_collecte_backend project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/asgi/
"""

import os
from django.core.asgi import get_asgi_application

# Utiliser les paramètres de production en environnement de production
settings_module = 'fapag_collecte_backend.production_settings' if os.getenv('DJANGO_PRODUCTION') else 'fapag_collecte_backend.settings'
os.environ.setdefault('DJANGO_SETTINGS_MODULE', settings_module)

application = get_asgi_application()
