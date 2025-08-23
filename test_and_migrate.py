import os
import sys
import django
from pathlib import Path

# Configuration de l'environnement Django
BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'temp_db_settings')
django.setup()

# Test de connexion à la base de données
print("🔍 Test de connexion à la base de données...")
try:
    from django.db import connection
    with connection.cursor() as cursor:
        cursor.execute("SELECT 1")
        result = cursor.fetchone()
        if result[0] == 1:
            print("✅ Connexion à la base de données réussie!")
        else:
            print("❌ La connexion a réussi mais la requête a échoué")
            sys.exit(1)
    
    # Vérifier les migrations en attente
    print("\n🔄 Vérification des migrations en attente...")
    from django.core.management import call_command
    call_command('makemigrations', 'collecte', interactive=False, dry_run=True)
    
    # Appliquer les migrations
    print("\n🔄 Application des migrations...")
    call_command('migrate', interactive=False)
    
    # Vérifier s'il y a un superutilisateur
    from django.contrib.auth import get_user_model
    User = get_user_model()
    if not User.objects.filter(is_superuser=True).exists():
        print("\n👤 Création d'un superutilisateur...")
        User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
        print("✅ Superutilisateur créé avec succès!")
        print("   Nom d'utilisateur: admin")
        print("   Mot de passe: admin123")
    else:
        print("\nℹ️ Un superutilisateur existe déjà dans la base de données.")
    
    print("\n✨ Tous les tests ont été effectués avec succès!")
    print("Vous pouvez maintenant démarrer le serveur avec la commande suivante:")
    print("python manage.py runserver --settings=temp_db_settings")
    
except Exception as e:
    print(f"\n❌ Erreur: {str(e)}")
    print("\n🔧 Conseils de dépannage:")
    print("1. Vérifiez que PostgreSQL est en cours d'exécution")
    print("2. Vérifiez les identifiants de la base de données dans temp_db_settings.py")
    print("3. Assurez-vous que l'utilisateur a les droits nécessaires sur la base de données")
    print("4. Vérifiez que le port 5432 est accessible")
    sys.exit(1)
