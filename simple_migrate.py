import os
import django
from django.conf import settings

def run():
    # Configuration minimale de Django
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'levee_fonds',
            'USER': 'postgres',
            'PASSWORD': 'Root@FAPAG@2025',
            'HOST': 'localhost',
            'PORT': '5432',
        }
    }
    
    INSTALLED_APPS = [
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'collecte.apps.CollecteConfig',
    ]
    
    settings.configure(
        DATABASES=DATABASES,
        INSTALLED_APPS=INSTALLED_APPS,
        DEFAULT_AUTO_FIELD='django.db.models.BigAutoField',
        AUTH_USER_MODEL='collecte.Utilisateur',
    )
    
    django.setup()
    
    from django.core.management import call_command
    
    # Créer les migrations
    print("Création des migrations...")
    call_command('makemigrations', 'collecte')
    
    # Appliquer les migrations
    print("\nApplication des migrations...")
    call_command('migrate')
    
    # Créer un superutilisateur
    print("\nCréation d'un superutilisateur...")
    call_command('createsuperuser', '--noinput', '--username=admin', '--email=admin@example.com')
    
    print("\nTâches terminées avec succès!")

if __name__ == "__main__":
    run()
