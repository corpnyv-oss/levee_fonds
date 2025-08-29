import os
from django.core.wsgi import get_wsgi_application

# Utiliser les paramètres standards (prod si DJANGO_PRODUCTION, sinon settings par défaut)
settings_module = 'fapag_collecte_backend.production_settings' if os.getenv('DJANGO_PRODUCTION') else 'fapag_collecte_backend.settings'
os.environ.setdefault('DJANGO_SETTINGS_MODULE', settings_module)

application = get_wsgi_application()
