import psycopg2
import ssl
from psycopg2 import OperationalError, Error as PgError

def test_connection():
    conn = None
    try:
        print("Tentative de connexion à la base de données...")
        
        # Configuration SSL
        ssl_context = ssl.create_default_context()
        ssl_context.verify_mode = ssl.CERT_REQUIRED
        
        # Paramètres de connexion
        conn_params = {
            'dbname': 'db_levee_fonds',
            'user': 'db_levee_fonds_user',
            'password': '3gWX7NcyKeyLbVTGHBerEiU5d37LSBHA',
            'host': 'dpg-d2l2ir95pdvs73a92fog-a.frankfurt-postgres.render.com',
            'port': '5432',
            'connect_timeout': 10,
            'sslmode': 'require',
            'sslrootcert': ssl.get_default_verify_paths().cafile,
            'ssl': ssl_context
        }
        
        print("Paramètres de connexion:")
        for key in ['host', 'port', 'dbname', 'user']:
            print(f"  {key}: {conn_params[key]}")
            
        # Tentative de connexion
        conn = psycopg2.connect(**conn_params)
        print("✅ Connexion à la base de données réussie!")
        
        # Tester une requête simple
        cur = conn.cursor()
        cur.execute("SELECT version();")
        db_version = cur.fetchone()
        print(f"Version de PostgreSQL: {db_version[0]}")
        
        return True
        
    except PgError as e:
        print(f"❌ Erreur PostgreSQL: {e}")
        return False
    except Exception as e:
        print(f"❌ Erreur inattendue: {e}")
        return False
    finally:
        if conn is not None:
            conn.close()
            print("Connexion fermée.")

if __name__ == "__main__":
    test_connection()
