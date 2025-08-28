import sys
import os
import platform

def check_environment():
    print("=== Vérification de l'environnement ===")
    print(f"Système d'exploitation: {platform.system()} {platform.release()}")
    print(f"Python: {sys.executable}")
    print(f"Version Python: {platform.python_version()}")
    
    # Vérifier les variables d'environnement
    print("\n=== Variables d'environnement ===")
    for var in ['POSTGRES_DB', 'POSTGRES_USER', 'POSTGRES_PASSWORD', 'POSTGRES_HOST', 'POSTGRES_PORT']:
        print(f"{var}: {'***' if 'PASSWORD' in var else os.environ.get(var, 'Non défini')}")
    
    # Vérifier les imports
    print("\n=== Vérification des imports ===")
    try:
        import psycopg2
        print("✅ psycopg2 est installé")
    except ImportError:
        print("❌ psycopg2 n'est pas installé")
    
    try:
        import django
        print(f"✅ Django est installé (version {django.__version__})")
    except ImportError:
        print("❌ Django n'est pas installé")

if __name__ == "__main__":
    check_environment()
