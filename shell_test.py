import os
import django

def test_connection():
    # Configuration Django
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fapag_collecte_backend.settings')
    django.setup()
    
    from django.db import connection
    
    print("=== Test de connexion à la base de données ===")
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            result = cursor.fetchone()
            print(f"✅ Test de requête réussi: {result[0] == 1}")
    except Exception as e:
        print(f"❌ Erreur: {e}")
        raise

if __name__ == "__main__":
    test_connection()
