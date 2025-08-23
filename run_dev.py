import os
import sys
import django
from django.core.management import execute_from_command_line

def main():
    # Configuration de l'environnement Django
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fapag_collecte_backend.settings')
    
    try:
        # Essayer d'importer les paramètres
        from django.conf import settings
        
        # Configuration de Django
        django.setup()
        
        # Exécuter les commandes de gestion
        print("\n=== Exécution de makemigrations ===")
        execute_from_command_line(['manage.py', 'makemigrations'])
        
        print("\n=== Exécution de migrate ===")
        execute_from_command_line(['manage.py', 'migrate'])
        
        # Créer un superutilisateur si nécessaire
        from django.contrib.auth import get_user_model
        User = get_user_model()
        if not User.objects.filter(email='admin@example.com').exists():
            print("\n=== Création d'un superutilisateur ===")
            User.objects.create_superuser(
                username='admin',
                email='admin@example.com',
                password='admin123',
                role='admin'
            )
            print("Superutilisateur créé avec succès!")
            print("Email: admin@example.com")
            print("Mot de passe: admin123")
        
        # Démarrer le serveur de développement
        print("\n=== Démarrage du serveur de développement ===")
        execute_from_command_line(['manage.py', 'runserver'])
        
    except Exception as e:
        print(f"\n❌ Une erreur s'est produite: {str(e)}")
        print("\nDétails de l'erreur:")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
