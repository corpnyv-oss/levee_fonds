import os
import django

def test():
    # Configuration Django
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fapag_collecte_backend.settings')
    
    try:
        django.setup()
        print("✅ Django est correctement configuré")
        
        from django.db import connection
        print("✅ Module de base de données Django chargé")
        
        # Tester la connexion
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            result = cursor.fetchone()
            print(f"✅ Test de connexion réussi: {result[0] == 1}")
            
    except Exception as e:
        print(f"❌ Erreur: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    print("=== Test de configuration Django ===")
    test()
