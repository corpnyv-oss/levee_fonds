import psycopg2
import sys
import socket
from urllib.parse import urlparse

def test_connection():
    print("=== Test de connexion directe à PostgreSQL ===")
    
    # Paramètres de connexion
    db_params = {
        'dbname': 'db_levee_fonds',
        'user': 'db_levee_fonds_user',
        'password': '3gWX7NcyKeyLbVTGHBerEiU5d37LSBHA',
        'host': 'dpg-d2l2ir95pdvs73a92fog-a.frankfurt-postgres.render.com',
        'port': '5432',
        'connect_timeout': 10,
        'sslmode': 'require'
    }
    
    print("Paramètres de connexion:")
    for key, value in db_params.items():
        if key != 'password':
            print(f"  {key}: {value}")
    
    # Tester la résolution DNS
    print("\n1. Test de résolution DNS...")
    try:
        host = db_params['host']
        ip = socket.gethostbyname(host)
        print(f"✅ Résolution DNS réussie: {host} → {ip}")
    except socket.gaierror as e:
        print(f"❌ Échec de la résolution DNS: {e}")
        return
    
    # Tester la connexion TCP
    print("\n2. Test de connexion TCP...")
    sock = None
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(10)
        print(f"  Connexion à {host}:{db_params['port']}...")
        sock.connect((host, int(db_params['port'])))
        print("✅ Connexion TCP établie avec succès")
    except Exception as e:
        print(f"❌ Échec de la connexion TCP: {e}")
        if sock:
            sock.close()
        return
    
    # Si nous sommes arrivés ici, la connexion TCP est établie
    sock.close()
    
    # Tester la connexion à la base de données
    print("\n3. Test de connexion à la base de données...")
    conn = None
    try:
        conn = psycopg2.connect(**db_params)
        print("✅ Connexion à PostgreSQL réussie!")
        
        # Exécuter une requête simple
        with conn.cursor() as cur:
            cur.execute("SELECT version()")
            version = cur.fetchone()
            print(f"\n=== Informations sur le serveur ===")
            print(f"Version: {version[0]}")
            
            # Afficher des informations sur la base de données
            cur.execute("""
                SELECT datname, usename, application_name, client_addr, state 
                FROM pg_stat_activity 
                WHERE pid = pg_backend_pid()
            """)
            columns = [desc[0] for desc in cur.description]
            db_info = dict(zip(columns, cur.fetchone()))
            print("\n=== Connexion active ===")
            for key, value in db_info.items():
                print(f"{key}: {value}")
                
    except psycopg2.OperationalError as e:
        print(f"❌ Erreur opérationnelle: {e}")
    except psycopg2.Error as e:
        print(f"❌ Erreur PostgreSQL: {e}")
    except Exception as e:
        print(f"❌ Erreur inattendue: {e}")
        import traceback
        traceback.print_exc()
    finally:
        if conn:
            conn.close()
            print("\nConnexion fermée.")

if __name__ == "__main__":
    test_connection()
    print("\n=== Test terminé ===")
