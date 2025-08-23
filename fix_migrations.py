import os
import sys
import django
from pathlib import Path

# Configuration de l'environnement Django
BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fapag_collecte_backend.settings')
django.setup()

# Nettoyage des migrations existantes
print("🧹 Nettoyage des migrations existantes...")
migrations_dir = BASE_DIR / 'collecte' / 'migrations'
for f in migrations_dir.glob('*.py'):
    if f.name != '__init__.py':
        f.unlink()

print("ℹ️  Nettoyage des migrations terminé")

# Création des migrations
print("\n🔄 Création des migrations...")
from django.core.management import call_command
call_command('makemigrations', 'collecte')

# Application des migrations
print("\n🔄 Application des migrations...")
call_command('migrate')

# Création d'un superutilisateur
print("\n👤 Création d'un superutilisateur...")
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
    print("✅ Superutilisateur créé avec succès!")
    print("   Nom d'utilisateur: admin")
    print("   Mot de passe: admin123")
else:
    print("ℹ️ Un superutilisateur existe déjà.")

print("\n✨ Tâches terminées avec succès !")
