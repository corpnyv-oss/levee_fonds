import sys
import os

def main():
    print("=== Test d'exécution Python ===")
    print(f"Version de Python: {sys.version}")
    print(f"Répertoire de travail: {os.getcwd()}")
    print(f"Chemin Python: {sys.executable}")
    
    # Essayer d'importer des modules
    try:
        import django
        print(f"Django version: {django.get_version()}")
    except ImportError:
        print("Django n'est pas installé ou n'est pas accessible")
    
    try:
        import psycopg2
        print("psycopg2 est installé")
    except ImportError:
        print("psycopg2 n'est pas installé")
    
    # Tester l'écriture de fichier
    try:
        with open("test_file.txt", "w") as f:
            f.write("Test d'écriture de fichier réussi!")
        print("Test d'écriture de fichier réussi")
        os.remove("test_file.txt")
    except Exception as e:
        print(f"Erreur lors de l'écriture du fichier: {e}")

if __name__ == "__main__":
    main()
