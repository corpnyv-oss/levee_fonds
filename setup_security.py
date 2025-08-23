#!/usr/bin/env python
"""
Script de configuration de la sécurité pour le projet FAPAG.
Ce script configure automatiquement les paramètres de sécurité et installe les dépendances nécessaires.
"""

import os
import sys
import subprocess
import platform
from pathlib import Path

def check_python_version():
    """Vérifie que la version de Python est suffisante."""
    if sys.version_info < (3, 8):
        print("[ERREUR] Python 3.8 ou supérieur est requis.")
        sys.exit(1)

def install_dependencies():
    """Installe les dépendances requises."""
    dependencies = [
        'python-json-logger>=2.0.7',
        'django-axes>=8.0.0',
        'argon2-cffi>=23.1.0',
        'cryptography>=42.0.0',
        'python-jose[cryptography]>=3.3.0',
        'sentry-sdk>=1.39.1',
    ]
    
    print("Installation des dépendances de sécurité...")
    try:
        # Mise à jour de pip d'abord
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '--upgrade', 'pip'])        
        # Installation des dépendances une par une pour un meilleur débogage
        for dep in dependencies:
            try:
                print(f"Installation de {dep}...")
                subprocess.check_call([sys.executable, '-m', 'pip', 'install', dep])
            except subprocess.CalledProcessError as e:
                print(f"⚠ Attention: Échec de l'installation de {dep}: {e}")
                print("Tentative de continuation...")
        
        print("✅ Installation des dépendances terminée.")
    except Exception as e:
        print(f"❌ Erreur critique lors de l'installation: {e}")
        print("Certaines dépendances n'ont pas pu être installées.")
        sys.exit(1)

def setup_directories():
    """Crée les répertoires nécessaires pour les logs et les sauvegardes."""
    base_dir = Path(__file__).parent
    dirs = [
        base_dir / 'logs',
        base_dir / 'backups',
        base_dir / 'media',
        base_dir / 'static',
    ]
    
    print("Création des répertoires...")
    for directory in dirs:
        try:
            directory.mkdir(exist_ok=True, parents=True)
            print(f"✅ Répertoire créé : {directory}")
        except Exception as e:
            print(f"❌ Erreur lors de la création de {directory}: {e}")

def generate_secret_key():
    """Génère une clé secrète sécurisée."""
    from django.core.management.utils import get_random_secret_key
    return get_random_secret_key()

def setup_environment():
    """Configure le fichier .env avec les variables d'environnement nécessaires."""
    env_file = Path('.env')
    if env_file.exists():
        print("⚠ Le fichier .env existe déjà. Voulez-vous le sauvegarder avant de continuer? (o/n)")
        if input().lower() == 'o':
            backup_file = f".env.backup_{int(time.time())}"
            env_file.rename(backup_file)
            print(f"✅ Fichier .env sauvegardé sous {backup_file}")
    
    secret_key = generate_secret_key()
    
    env_content = f"""# Configuration de l'application
DEBUG=False
SECRET_KEY={secret_key}

# Configuration de la base de données
DB_NAME=fapag_db
DB_USER=fapag_user
DB_PASSWORD=change_this_password
DB_HOST=localhost
DB_PORT=5432

# Configuration du serveur de messagerie
EMAIL_HOST=your_smtp_host
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your_email@example.com
EMAIL_HOST_PASSWORD=your_email_password
DEFAULT_FROM_EMAIL=no-reply@example.com

# Configuration de sécurité
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
SECURE_HSTS_SECONDS=31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS=True
SECURE_HSTS_PRELOAD=True
SECURE_REFERRER_POLICY=same-origin

# Configuration CORS
CORS_ALLOWED_ORIGINS=http://localhost:3000

# Configuration des logs
LOG_LEVEL=INFO
LOG_MAX_SIZE=10  # MB
LOG_BACKUP_COUNT=5
"""
    
    with open('.env', 'w') as f:
        f.write(env_content)
    
    print("✅ Fichier .env créé avec succès.")
    print("⚠ N'oubliez pas de modifier les valeurs par défaut dans le fichier .env")

def main():
    print("=== Configuration de la sécurité FAPAG ===\n")
    
    # Vérifications préalables
    check_python_version()
    
    # Installation des dépendances
    install_dependencies()
    
    # Création des répertoires
    setup_directories()
    
    # Configuration de l'environnement
    setup_environment()
    
    print("\n=== Configuration terminée avec succès ===")
    print("Prochaines étapes :")
    print("1. Modifiez le fichier .env avec vos paramètres")
    print("2. Exécutez les migrations : python manage.py migrate")
    print("3. Créez un superutilisateur : python manage.py createsuperuser")
    print("4. Lancez le serveur : python manage.py runserver")

if __name__ == "__main__":
    import time
    main()
