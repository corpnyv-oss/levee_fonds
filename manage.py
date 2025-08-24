#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
from pathlib import Path
from dotenv import load_dotenv


def load_env():
    """Load environment variables from .env file."""
    # Chemin vers le répertoire contenant manage.py
    base_dir = Path(__file__).resolve().parent
    
    # Charger d'abord le .env par défaut
    env_path = base_dir / '.env'
    if env_path.exists():
        load_dotenv(env_path, override=True)
        print(f"✅ Fichier .env chargé depuis: {env_path}")
    else:
        print("⚠️  Fichier .env non trouvé. Utilisation des variables d'environnement système.")


def main():
    """Run administrative tasks."""
    # Charger les variables d'environnement
    load_env()
    
    # Vérifier que SECRET_KEY est défini
    if not os.getenv('SECRET_KEY'):
        print("❌ ERREUR: La variable SECRET_KEY n'est pas définie")
        print("Veuillez la définir dans le fichier .env ou dans les variables d'environnement système.")
        sys.exit(1)
    
    # Afficher les variables d'environnement pour le débogage
    print("\n=== Variables d'environnement ===")
    for key in ['DATABASE_URL', 'POSTGRES_DB', 'POSTGRES_USER', 'POSTGRES_PASSWORD', 'POSTGRES_HOST', 'POSTGRES_PORT']:
        print(f"{key}: {'***' if 'PASSWORD' in key else os.environ.get(key, 'Non défini')}")
    print("==============================\n")
    
    # Utiliser les paramètres Django par défaut
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fapag_collecte_backend.settings')
    
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
