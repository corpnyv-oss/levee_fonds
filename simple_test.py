import psycopg2
from psycopg2 import OperationalError
import os

def test_connection():
    try:
        conn = psycopg2.connect(
            dbname='db_levee_fonds',
            user='db_levee_fonds_user',
            password='3gWX7NcyKeyLbVTGHBerEiU5d37LSBHA',
            host='dpg-d2l2ir95pdvs73a92fog-a.frankfurt-postgres.render.com',
            port='5432',
            sslmode='require'
        )
        print("✅ Connexion réussie à la base de données!")
        
        # Tester une requête simple
        cursor = conn.cursor()
        cursor.execute("SELECT version();")
        version = cursor.fetchone()
        print(f"Version de PostgreSQL: {version[0]}")
        
        cursor.close()
        conn.close()
        
    except OperationalError as e:
        print(f"❌ Erreur de connexion: {e}")
        print("Vérifiez que:")
        print("1. Vous êtes connecté à Internet")
        print("2. L'hôte est accessible depuis votre réseau")
        print("3. Les identifiants sont corrects")
        print("4. Le port 5432 n'est pas bloqué par un pare-feu")

if __name__ == "__main__":
    test_connection()
