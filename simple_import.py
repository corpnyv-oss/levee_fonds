print("=== Test d'importation simple ===\n")

try:
    print("1. Essai d'importation de sys...")
    import sys
    print(f"✅ sys importé depuis: {sys.executable}")
    print(f"   Version Python: {sys.version}")
    
    print("\n2. Essai d'importation de django...")
    import django
    print(f"✅ Django importé (version: {django.__version__})")
    
    print("\n3. Configuration des paramètres Django...")
    import os
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fapag_collecte_backend.settings')
    django.setup()
    print("✅ Configuration Django chargée")
    
    print("\n4. Test de la connexion à la base de données...")
    from django.db import connection
    with connection.cursor() as cursor:
        cursor.execute("SELECT 1")
        result = cursor.fetchone()
        print(f"✅ Connexion à la base de données réussie: {result[0] == 1}")
    
except Exception as e:
    print(f"\n❌ Erreur: {e}")
    import traceback
    traceback.print_exc()
