import sys
import os
import psycopg2
from psycopg2 import OperationalError
from urllib.parse import urlparse

print("=== Début du débogage de la connexion à la base de données ===\n")

# Configuration de la base de données
db_config = {
    'dbname': 'db_levee_fonds',
    'user': 'db_levee_fonds_user',
    'password': '3gWX7NcyKeyLbVTGHBerEiU5d37LSBHA',
    'host': 'dpg-d2l2ir95pdvs73a92fog-a',
    'port': '5432',
    'sslmode': 'require',
    'connect_timeout': 5
}

print("Configuration de la base de données:")
for key, value in db_config.items():
    print(f"  {key}: {'*' * 8 if key == 'password' else value}")

print("\nTentative de connexion à la base de données...")

try:
    conn = psycopg2.connect(**db_config)
    print("✅ Connexion réussie à la base de données!")
    
    # Tester la connexion
    cursor = conn.cursor()
    cursor.execute("SELECT version();")
    version = cursor.fetchone()
    print(f"\nVersion de PostgreSQL: {version[0]}")
    
    # Vérifier les bases de données disponibles
    cursor.execute("SELECT datname FROM pg_database;")
    databases = [db[0] for db in cursor.fetchall()]
    print("\nBases de données disponibles:", ", ".join(databases))
    
    cursor.close()
    conn.close()
    
except OperationalError as e:
    print(f"\n❌ Erreur de connexion: {e}")
    print("\nVérifiez que:")
    print("1. Le serveur PostgreSQL est en cours d'exécution et accessible")
    print("2. Les identifiants de connexion sont corrects")
    print("3. Le pare-feu autorise les connexions sur le port 5432")
    print("4. Le nom d'hôte est correct et résout correctement")
    print("5. Le SSL est correctement configuré sur le serveur")
    
    # Suggestions basées sur le message d'erreur
    if "connection to server at" in str(e) and "failed" in str(e):
        print("\nConseil: Vérifiez que l'hôte est correct et accessible depuis votre réseau.")
    elif "password authentication failed" in str(e):
        print("\nConseil: Vérifiez le nom d'utilisateur et le mot de passe.")
    elif "database" in str(e) and "does not exist" in str(e):
        print("\nConseil: La base de données spécifiée n'existe pas.")
    elif "timeout" in str(e):
        print("\nConseil: Le serveur ne répond pas dans le délai imparti. Vérifiez la connectivité réseau.")
    
    sys.exit(1)

except Exception as e:
    print(f"\n❌ Erreur inattendue: {e}")
    sys.exit(1)

print("\n=== Fin du débogage ===")
