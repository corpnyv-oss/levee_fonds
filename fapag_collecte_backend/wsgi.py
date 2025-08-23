"""
WSGI config for fapag_collecte_backend project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Charger les variables d'environnement depuis .env
BASE_DIR = Path(__file__).resolve().parent.parent
ENV_PATH = BASE_DIR / '.env'
if ENV_PATH.exists():
    load_dotenv(ENV_PATH)
    print(f"✅ Fichier .env chargé depuis: {ENV_PATH}")
else:
    print("⚠️  Fichier .env non trouvé. Utilisation des variables d'environnement système.")

# Vérifier que SECRET_KEY est défini
if not os.getenv('SECRET_KEY'):
    raise ValueError("La variable SECRET_KEY n'est pas définie dans les variables d'environnement")

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fapag_collecte_backend.settings')

application = get_wsgi_application()
