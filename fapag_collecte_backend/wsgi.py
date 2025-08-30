"""
WSGI config for fapag_collecte_backend project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import os
from django.core.wsgi import get_wsgi_application

# Configuration pour Render
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fapag_collecte_backend.settings')

# Configuration pour la production
if os.environ.get('RENDER'):
    # Variables d'environnement Render
    os.environ.setdefault('DEBUG', 'False')
    os.environ.setdefault('ALLOWED_HOSTS', '.onrender.com')

application = get_wsgi_application()
