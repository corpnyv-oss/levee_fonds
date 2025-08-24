import os
import psycopg2
import ssl
from urllib.parse import urlparse
from dotenv import load_dotenv

def load_db_config():
    """Charge la configuration depuis les variables d'environnement"""
    load_dotenv()
    
    db_url = os.getenv('DATABASE_URL')
    if not db_url:
        print("❌ ERREUR: La variable DATABASE_URL n'est pas définie dans le fichier .env")
        return None
    
    try:
        # Extraire les informations de connexion depuis l'URL
        parsed = urlparse(db_url)
        return {
            'dbname': parsed.path[1:],  # Supprimer le premier '/'
            'user': parsed.username,
            'password': parsed.password,
            'host': parsed.hostname,
            'port': str(parsed.port),
            'sslmode': 'require',
            'connect_timeout': 5
        }
    except Exception as e:
        print(f"❌ ERREUR lors de l'analyse de DATABASE_URL: {str(e)}")
        return None

def test_connection():
    print("=== Test de connexion à la base de données PostgreSQL ===")
    
    # Charger la configuration
    db_params = load_db_config()
    if not db_params:
        return
    
    # Afficher les paramètres (masquer le mot de passe)
    print("\nParamètres de connexion:")
    print(f"  Base de données: {db_params['dbname']}")
    print(f"  Hôte: {db_params['host']}")
    print(f"  Port: {db_params['port']}")
    print(f"  Utilisateur: {db_params['user']}")
    print(f"  SSL: {db_params['sslmode']}")
    
    try:
        print("\nTentative de connexion...")
        
        # Créer un contexte SSL personnalisé
        ssl_context = ssl.create_default_context()
        ssl_context.verify_mode = ssl.CERT_REQUIRED
        
        # Essayer avec le contexte SSL
        conn = psycopg2.connect(
            **db_params,
            sslrootcert=ssl.get_default_verify_paths().cafile,
            sslcontext=ssl_context
        )
        
        print("✅ Connexion réussie!")
        
        # Tester une requête simple
        with conn.cursor() as cur:
            cur.execute("SELECT version();")
            version = cur.fetchone()
            print(f"\n=== Version de PostgreSQL ===\n{version[0]}")
            
            cur.execute("SELECT current_database(), current_user, inet_server_addr(), inet_server_port();")
            db_info = cur.fetchone()
            print("\n=== Informations de connexion ===")
            print(f"Base de données: {db_info[0]}")
            print(f"Utilisateur: {db_info[1]}")
            print(f"Adresse du serveur: {db_info[2]}")
            print(f"Port du serveur: {db_info[3]}")
        
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
