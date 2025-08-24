import os
import psycopg2
from psycopg2 import OperationalError

def test_connection():
    """Teste la connexion à la base de données PostgreSQL"""
    print("=== Test de connexion sécurisé à PostgreSQL ===")
    
    try:
        # Tenter d'établir une connexion
        conn = psycopg2.connect(
            dbname=os.getenv('DB_NAME'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            host=os.getenv('DB_HOST'),
            port=os.getenv('DB_PORT', '5432'),
            sslmode='require',
            connect_timeout=5
        )
        
        print("✅ Connexion réussie!")
        
        # Tester une requête simple
        with conn.cursor() as cur:
            cur.execute("SELECT version();")
            version = cur.fetchone()
            print(f"\n=== Version de PostgreSQL ===\n{version[0]}")
            
        conn.close()
        return True
        
    except OperationalError as e:
        print(f"❌ Erreur de connexion: {str(e)}")
        return False
    except Exception as e:
        print(f"❌ Erreur inattendue: {str(e)}")
        return False

if __name__ == "__main__":
    # Vérifier les variables d'environnement requises
    required_vars = ['DB_NAME', 'DB_USER', 'DB_PASSWORD', 'DB_HOST']
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        print(f"❌ Variables d'environnement manquantes: {', '.join(missing_vars)}")
        print("Veuillez définir ces variables dans votre fichier .env")
    else:
        test_connection()
