import sys
import os
from pathlib import Path
from dotenv import load_dotenv

# Charger les variables d'environnement
BASE_DIR = Path(__file__).resolve().parent
ENV_PATH = BASE_DIR / '.env'
if ENV_PATH.exists():
    load_dotenv(ENV_PATH, override=True)
    print(f"✅ Fichier .env chargé depuis: {ENV_PATH}")
else:
    print("⚠️  Fichier .env non trouvé. Utilisation des variables d'environnement système.")

# Afficher les variables d'environnement
print("\n=== Variables d'environnement ===")
for key in ['DATABASE_URL', 'POSTGRES_DB', 'POSTGRES_USER', 'POSTGRES_PASSWORD', 'POSTGRES_HOST', 'POSTGRES_PORT']:
    print(f"{key}: {'***' if 'PASSWORD' in key else os.environ.get(key, 'Non défini')}")
print("==============================\n")

# Tester la connexion à la base de données
try:
    import psycopg2
    
    print("Tentative de connexion à la base de données...")
    
    conn = psycopg2.connect(
        dbname='db_levee_fonds',
        user='db_levee_fonds_user',
        password='3gWX7NcyKeyLbVTGHBerEiU5d37LSBHA',
        host='dpg-d2l2ir95pdvs73a92fog-a',
        port='5432',
        sslmode='require',
        connect_timeout=5
    )
    
    cursor = conn.cursor()
    cursor.execute("SELECT version();")
    version = cursor.fetchone()
    
    print("✅ Connexion réussie à la base de données!")
    print(f"Version de PostgreSQL: {version[0]}")
    
    cursor.close()
    conn.close()
    
except Exception as e:
    print(f"❌ Erreur de connexion à la base de données: {e}")
    print("Vérifiez que:")
    print("1. Le serveur PostgreSQL est en cours d'exécution")
    print("2. Les identifiants de connexion sont corrects")
    print("3. Le pare-feu autorise les connexions sur le port 5432")
    print(f"4. L'hôte {os.environ.get('POSTGRES_HOST', 'dpg-d2l2ir95pdvs73a92fog-a')} est accessible depuis votre machine")
    sys.exit(1)
