import os
import sys
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

def reset_database():
    try:
        # Connexion à la base de données postgres par défaut
        conn = psycopg2.connect(
            dbname='postgres',
            user='postgres',
            password='Root@FAPAG@2025',
            host='localhost',
            port='5432'
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor()
        
        # Forcer la fermeture des connexions existantes
        print("🔒 Fermeture des connexions actives...")
        cursor.execute("""
            SELECT pg_terminate_backend(pg_stat_activity.pid)
            FROM pg_stat_activity
            WHERE pg_stat_activity.datname = 'levee_fonds'
            AND pid <> pg_backend_pid();
        """)
        
        # Supprimer la base de données si elle existe
        print("🗑️  Suppression de la base de données existante...")
        cursor.execute("DROP DATABASE IF EXISTS levee_fonds")
        
        # Créer une nouvelle base de données
        print("🆕 Création d'une nouvelle base de données...")
        cursor.execute("CREATE DATABASE levee_fonds")
        
        cursor.close()
        conn.close()
        
        print("✅ Base de données réinitialisée avec succès!")
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de la réinitialisation de la base de données: {e}")
        return False

def run_migrations():
    try:
        print("\n🔄 Exécution des migrations...")
        os.system('python manage.py makemigrations --settings=minimal_settings')
        os.system('python manage.py migrate --settings=minimal_settings')
        print("✅ Migrations terminées avec succès!")
        return True
    except Exception as e:
        print(f"❌ Erreur lors de l'exécution des migrations: {e}")
        return False

def create_superuser():
    try:
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
        
        return True
    except Exception as e:
        print(f"❌ Erreur lors de la création du superutilisateur: {e}")
        return False

if __name__ == "__main__":
    print("🔄 RÉINITIALISATION DE LA BASE DE DONNÉES ET MIGRATIONS\n")
    
    if reset_database():
        # Configurer les variables d'environnement pour Django
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'minimal_settings')
        import django
        django.setup()
        
        if run_migrations():
            create_superuser()
    
    print("\n✨ Tâches terminées. Vous pouvez maintenant démarrer le serveur avec :")
    print("python manage.py runserver --settings=minimal_settings")
