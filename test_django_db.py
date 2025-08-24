import os
import django
from django.conf import settings

def test_django_db():
    # Configuration Django minimale
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fapag_collecte_backend.settings')
    django.setup()
    
    # Importer les modules Django après la configuration
    from django.db import connection
    
    print("=== Test de connexion à la base de données Django ===")
    
    try:
        # Tester la connexion
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            one = cursor.fetchone()
            print(f"✅ Test de requête réussi: {one[0] == 1}")
            
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
        print(f"❌ Erreur de connexion: {e}")
        print("Vérifiez que:")
        print("1. Les informations de connexion sont correctes")
        print("2. Le serveur de base de données est en cours d'exécution")
        print(f"3. L'hôte {db_settings['HOST']} est accessible depuis votre réseau")
        print(f"4. Le port {db_settings['PORT']} n'est pas bloqué par un pare-feu")

if __name__ == "__main__":
    test_django_db()
