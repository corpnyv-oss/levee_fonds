import os
import time
from pathlib import Path
from dotenv import load_dotenv

# Afficher le répertoire de travail actuel
print(f"Répertoire de travail: {os.getcwd()}")

# Chemin vers le fichier .env
env_path = Path(__file__).parent / '.env'
print(f"Chemin du fichier .env: {env_path}")
print(f"Le fichier .env existe: {env_path.exists()}")

# Charger les variables d'environnement avec un délai
print("Chargement des variables d'environnement...")
time.sleep(2)  # Délai de 2 secondes

# Charger le fichier .env explicitement
load_dotenv(env_path, override=True)

# Afficher les variables d'environnement
print("=== Variables d'environnement ===")
for key in ['DATABASE_URL', 'POSTGRES_DB', 'POSTGRES_USER', 'POSTGRES_PASSWORD', 'POSTGRES_HOST', 'POSTGRES_PORT']:
    print(f"{key}: {os.environ.get(key, 'Non défini')}")
print("==============================\n")

# Tester si la variable DATABASE_URL est définie
if 'DATABASE_URL' in os.environ:
    print("✅ La variable DATABASE_URL est définie")
else:
    print("❌ La variable DATABASE_URL n'est pas définie")

# Tester si le fichier .env est chargé
if load_dotenv():
    print("✅ Le fichier .env a été chargé avec succès")
else:
    print("⚠️ Le fichier .env n'a pas pu être chargé")
