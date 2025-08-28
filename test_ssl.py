import psycopg2
import ssl
from urllib.parse import urlparse

# Paramètres de connexion
DB_URL = "postgresql://db_levee_fonds_user:3gWX7NcyKeyLbVTGHBerEiU5d37LSBHA@dpg-d2l2ir95pdvs73a92fog-a.oregon-postgres.render.com:5432/db_levee_fonds"

# Parser l'URL de la base de données
result = urlparse(DB_URL)
username = result.username
password = result.password
database = result.path[1:]  # Supprimer le premier '/'
hostname = result.hostname
port = result.port

print("=== Test de connexion SSL à PostgreSQL ===\n")
print(f"Hôte: {hostname}")
print(f"Port: {port}")
print(f"Base de données: {database}")
print(f"Utilisateur: {username}")
print("Mot de passe: ********\n")

# Essayer différentes configurations SSL
for sslmode in ['disable', 'allow', 'prefer', 'require', 'verify-ca', 'verify-full']:
    try:
        print(f"\nEssai avec sslmode='{sslmode}'...")
        
        conn = psycopg2.connect(
            dbname=database,
            user=username,
            password=password,
            host=hostname,
            port=port,
            sslmode=sslmode,
            connect_timeout=5
        )
        
        # Si on arrive ici, la connexion a réussi
        print(f"✅ Connexion réussie avec sslmode='{sslmode}'")
        
        # Tester une requête simple
        cursor = conn.cursor()
        cursor.execute("SELECT version();")
        version = cursor.fetchone()
        print(f"Version de PostgreSQL: {version[0]}")
        
        # Fermer la connexion
        conn.close()
        break
        
    except Exception as e:
        print(f"❌ Échec avec sslmode='{sslmode}': {str(e).split('(')[0]}")
        continue
