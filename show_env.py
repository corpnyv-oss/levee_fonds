import os
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

# Afficher les variables d'environnement pertinentes
print("=== Variables d'environnement chargées ===")
print(f"POSTGRES_DB: {os.getenv('POSTGRES_DB')}")
print(f"POSTGRES_USER: {os.getenv('POSTGRES_USER')}")
print(f"POSTGRES_PASSWORD: {'*' * 8 if os.getenv('POSTGRES_PASSWORD') else 'Non défini'}")
print(f"POSTGRES_HOST: {os.getenv('POSTGRES_HOST')}")
print(f"POSTGRES_PORT: {os.getenv('POSTGRES_PORT')}")
print("======================================")
