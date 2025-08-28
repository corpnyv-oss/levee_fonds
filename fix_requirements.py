"""
Script pour vérifier et installer les dépendances manquantes
"""
import subprocess
import sys

def check_and_install(package):
    try:
        __import__(package.split('==')[0] if '==' in package else package)
        print(f"✅ {package} est déjà installé")
        return True
    except ImportError:
        print(f"⚠️  Installation de {package}...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
            print(f"✅ {package} installé avec succès")
            return True
        except subprocess.CalledProcessError:
            print(f"❌ Échec de l'installation de {package}")
            return False

# Liste des dépendances requises
REQUIRED_PACKAGES = [
    'django>=4.2.0,<5.0.0',
    'djangorestframework>=3.14.0',
    'django-cors-headers>=4.0.0',
    'dj-database-url>=2.1.0',
    'psycopg2-binary>=2.9.9',
    'django-environ>=0.11.2',
    'django-axes>=7.0.0',
    'djangorestframework-simplejwt>=5.3.0',
    'django-two-factor-auth>=1.15.4',
    'django-otp>=1.2.0',
    'qrcode>=7.4.2',
    'phonenumbers>=8.13.11',
    'django-csp>=3.7',
    'python-dotenv>=1.0.0',
    'drf-yasg>=1.21.7',
    'django-filter>=23.5',
    'Pillow>=10.0.0',
    'celery>=5.3.0',
    'redis>=4.5.0',
    'gunicorn>=21.2.0',
    'whitenoise>=6.5.0',
    'python-memcached>=1.59'
]

if __name__ == "__main__":
    print("Vérification des dépendances...")
    all_installed = all(check_and_install(pkg) for pkg in REQUIRED_PACKAGES)
    
    if all_installed:
        print("\n✅ Toutes les dépendances sont installées avec succès!")
        print("Vous pouvez maintenant exécuter les migrations avec:\n")
        print("python manage.py migrate")
    else:
        print("\n❌ Certaines dépendances n'ont pas pu être installées.")
        print("Veuillez les installer manuellement ou vérifier votre connexion Internet.")
