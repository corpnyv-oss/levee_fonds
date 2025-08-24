import os
import sys
from pathlib import Path

def check_settings():
    print("=== Vérification de la configuration Django ===\n")
    
    # Vérifier si le fichier settings.py existe
    settings_path = Path(__file__).parent / 'fapag_collecte_backend' / 'settings.py'
    if not settings_path.exists():
        print(f"❌ Fichier de configuration introuvable: {settings_path}")
        return False
    
    print(f"✅ Fichier de configuration trouvé: {settings_path}")
    
    # Vérifier si le module Django est installé
    try:
        import django
        print(f"✅ Django est installé (version: {django.__version__})")
    except ImportError:
        print("❌ Django n'est pas installé")
        return False
    
    # Vérifier la configuration de la base de données
    try:
        # Ajouter le répertoire parent au path Python
        sys.path.append(str(Path(__file__).parent))
        
        # Importer les settings
        from fapag_collecte_backend import settings
        
        # Vérifier la configuration de la base de données
        if hasattr(settings, 'DATABASES') and 'default' in settings.DATABASES:
            db = settings.DATABASES['default']
            print("\n=== Configuration de la base de données ===")
            print(f"Moteur: {db.get('ENGINE')}")
            print(f"Base de données: {db.get('NAME')}")
            print(f"Utilisateur: {db.get('USER')}")
            print(f"Hôte: {db.get('HOST')}")
            print(f"Port: {db.get('PORT')}")
            
            # Vérifier les dépendances nécessaires
            if 'postgresql' in db.get('ENGINE', ''):
                try:
                    import psycopg2
                    print("\n✅ psycopg2 est installé")
                except ImportError:
                    print("\n❌ psycopg2 n'est pas installé. Essayez: pip install psycopg2-binary")
                    return False
        else:
            print("\n❌ Aucune configuration de base de données trouvée dans les settings")
            return False
            
        return True
        
    except Exception as e:
        print(f"\n❌ Erreur lors de la vérification des paramètres: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    check_settings()
