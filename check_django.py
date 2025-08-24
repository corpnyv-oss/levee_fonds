import sys
import os
from pathlib import Path

def check_django():
    print("=== Vérification de l'installation de Django ===\n")
    
    # Vérifier si Django est installé
    try:
        import django
        print(f"✅ Django est installé (version: {django.__version__})")
    except ImportError:
        print("❌ Django n'est pas installé")
        print("Veuillez l'installer avec: pip install django")
        return False
    
    # Vérifier si le répertoire du projet existe
    project_dir = Path(__file__).parent / 'fapag_collecte_backend'
    if not project_dir.exists():
        print(f"❌ Le répertoire du projet est introuvable: {project_dir}")
        return False
    
    print(f"✅ Répertoire du projet trouvé: {project_dir}")
    
    # Vérifier si settings.py existe
    settings_file = project_dir / 'settings.py'
    if not settings_file.exists():
        print(f"❌ Le fichier settings.py est introuvable dans: {project_dir}")
        return False
    
    print(f"✅ Fichier settings.py trouvé: {settings_file}")
    
    # Essayer de charger les paramètres Django
    try:
        # Ajouter le répertoire parent au path Python
        sys.path.append(str(Path(__file__).parent))
        
        # Configurer les paramètres Django
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fapag_collecte_backend.settings')
        django.setup()
        
        print("✅ Configuration Django chargée avec succès")
        
        # Vérifier la configuration de la base de données
        from django.conf import settings
        
        if hasattr(settings, 'DATABASES') and 'default' in settings.DATABASES:
            db = settings.DATABASES['default']
            print("\n=== Configuration de la base de données ===")
            print(f"Moteur: {db.get('ENGINE')}")
            print(f"Base de données: {db.get('NAME')}")
            print(f"Utilisateur: {db.get('USER')}")
            print(f"Hôte: {db.get('HOST')}")
            print(f"Port: {db.get('PORT')}")
            
            # Vérifier la connexion à la base de données
            try:
                from django.db import connection
                with connection.cursor() as cursor:
                    cursor.execute("SELECT 1")
                    result = cursor.fetchone()
                    print("\n✅ Test de connexion à la base de données réussi!")
                    return True
            except Exception as e:
                print(f"\n❌ Erreur de connexion à la base de données: {e}")
                return False
        else:
            print("\n❌ Aucune configuration de base de données trouvée dans les paramètres")
            return False
            
    except Exception as e:
        print(f"\n❌ Erreur lors du chargement de la configuration Django: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    check_django()
