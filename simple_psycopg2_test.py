import psycopg2
import sys

def test_connection():
    print("=== Test de connexion PostgreSQL avec psycopg2 ===")
    
    conn_params = {
        'dbname': 'db_levee_fonds',
        'user': 'db_levee_fonds_user',
        'password': '3gWX7NcyKeyLbVTGHBerEiU5d37LSBHA',
        'host': 'dpg-d2l2ir95pdvs73a92fog-a.frankfurt-postgres.render.com',
        'port': '5432',
        'connect_timeout': 5,
        'sslmode': 'require'
    }
    
    print("Paramètres de connexion:")
    for key, value in conn_params.items():
        if key != 'password':
            print(f"  {key}: {value}")
    
    try:
        print("\nTentative de connexion...")
        conn = psycopg2.connect(**conn_params)
        print("✅ Connexion réussie!")
        
        with conn.cursor() as cur:
            cur.execute("SELECT version()")
            version = cur.fetchone()
            print(f"\n=== Version de PostgreSQL ===")
            print(version[0])
            
            cur.execute("SELECT current_database(), current_user, inet_server_addr()")
            db_info = cur.fetchone()
            print("\n=== Informations de connexion ===")
            print(f"Base de données: {db_info[0]}")
            print(f"Utilisateur: {db_info[1]}")
            print(f"Adresse du serveur: {db_info[2]}")
            
        return True
        
    except Exception as e:
        print(f"\n❌ Erreur de connexion: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        if 'conn' in locals():
            conn.close()
            print("\nConnexion fermée.")

if __name__ == "__main__":
    test_connection()
