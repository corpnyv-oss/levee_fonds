import os
import sys
from pathlib import Path

# Ajouter le répertoire parent au chemin Python
sys.path.append(str(Path(__file__).parent))

# Importer les paramètres Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fapag_collecte_backend.settings')
import django
django.setup()

# Afficher la configuration de la base de données
from django.conf import settings

print("=== Configuration de la base de données ===")
print(f"Moteur: {settings.DATABASES['default']['ENGINE']}")
print(f"Nom de la base: {settings.DATABASES['default'].get('NAME', 'Non défini')}")
print(f"Utilisateur: {settings.DATABASES['default'].get('USER', 'Non défini')}")
print(f"Hôte: {settings.DATABASES['default'].get('HOST', 'Non défini')}")
print(f"Port: {settings.DATABASES['default'].get('PORT', 'Non défini')}")
print("======================================")

# Tester la connexion à la base de données
try:
    from django.db import connection
    with connection.cursor() as cursor:
        cursor.execute("SELECT 1")
        print("✅ Connexion à la base de données réussie!")
except Exception as e:
    print(f"❌ Erreur de connexion à la base de données: {e}")
