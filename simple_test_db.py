import sys
import psycopg2
from psycopg2 import OperationalError

def main():
    print("Test de connexion à PostgreSQL...")
    
    try:
        # Paramètres de connexion
        conn_params = {
            'dbname': 'db_levee_fonds',
            'user': 'db_levee_fonds_user',
            'password': '3gWX7NcyKeyLbVTGHBerEiU5d37LSBHA',
            'host': 'dpg-d2l2ir95pdvs73a92fog-a.frankfurt-postgres.render.com',
            'port': '5432',
            'sslmode': 'require',
            'connect_timeout': 5
        }
        
        print("Paramètres de connexion:")
        for k, v in conn_params.items():
            if k != 'password':
                print(f"  {k}: {v}")
        
        print("\nTentative de connexion...")
        conn = psycopg2.connect(**conn_params)
        print("✅ Connexion réussie!")
        
        # Tester une requête simple
        with conn.cursor() as cur:
            cur.execute("SELECT version()")
            version = cur.fetchone()
            print(f"\nVersion de PostgreSQL: {version[0]}")
            
        conn.close()
        return 0
        
    except OperationalError as e:
        print(f"\n❌ Erreur de connexion: {e}")
        return 1
    except Exception as e:
        print(f"\n❌ Erreur inattendue: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
