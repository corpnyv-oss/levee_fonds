import os
import django
from django.conf import settings

def test_database_connection():
    # Configuration Django minimale
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'temp_db_settings')
    
    try:
        # Configurer Django
        django.setup()
        print("✅ Configuration Django chargée avec succès")
        
        # Importer la connexion à la base de données
        from django.db import connection
        
        # Tester la connexion
        print("\n=== Test de connexion à la base de données ===")
        with connection.cursor() as cursor:
            cursor.execute("SELECT version()")
            version = cursor.fetchone()
            print(f"✅ Version de PostgreSQL: {version[0]}")
            
            # Tester une requête simple
            cursor.execute("SELECT 1")
            result = cursor.fetchone()
            print(f"✅ Test de requête réussi: {result[0] == 1}")
        
        # Afficher les informations de connexion (sans le mot de passe)
        db_settings = settings.DATABASES['default']
        print("\n=== Configuration de la base de données ===")
        print(f"Moteur: {db_settings['ENGINE']}")
        print(f"Base de données: {db_settings['NAME']}")
        print(f"Utilisateur: {db_settings['USER']}")
        print(f"Hôte: {db_settings['HOST']}")
        print(f"Port: {db_settings['PORT']}")
        print("==================================")
        
    except Exception as e:
        print(f"\n❌ Erreur lors de la connexion à la base de données:")
        print(f"Type d'erreur: {type(e).__name__}")
        print(f"Message d'erreur: {str(e)}")
        
        # Afficher plus d'informations sur l'erreur
        import traceback
        print("\n=== Détails de l'erreur ===")
        traceback.print_exc()
        print("========================")
        
        print("\n💡 Conseils de dépannage:")
        print("1. Vérifiez que le serveur PostgreSQL est en cours d'exécution")
        print(f"2. Vérifiez que l'hôte {db_settings['HOST']} est accessible depuis votre réseau")
        print(f"3. Vérifiez que le port {db_settings['PORT']} n'est pas bloqué par un pare-feu")
        print("4. Vérifiez les identifiants de la base de données")
        print("5. Essayez de vous connecter avec un client PostgreSQL comme pgAdmin ou psql")

if __name__ == "__main__":
    print("=== Test de connexion à la base de données avec configuration temporaire ===")
    test_database_connection()
