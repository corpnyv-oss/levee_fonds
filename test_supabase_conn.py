import psycopg2
import sys

def test_connection():
    print("=== Test de connexion à PostgreSQL ===\n")
    
    # Paramètres de connexion
    conn_params = {
        'dbname': 'db_levee_fonds',
        'user': 'db_levee_fonds_user',
        'password': '3gWX7NcyKeyLbVTGHBerEiU5d37LSBHA',
        'host': 'dpg-d2l2ir95pdvs73a92fog-a.oregon-postgres.render.com',
        'port': '5432',
        'sslmode': 'require',
        'connect_timeout': 5
    }
    
    try:
        print("Tentative de connexion...")
        conn = psycopg2.connect(**conn_params)
        print("✅ Connexion réussie!")
        
        # Tester une requête simple
        cursor = conn.cursor()
        cursor.execute("SELECT version();")
        version = cursor.fetchone()
        print(f"\nVersion de PostgreSQL: {version[0]}")
        
        # Fermer la connexion
        conn.close()
        return True
        
    except Exception as e:
        print(f"\n❌ Erreur de connexion:")
        print(f"Type: {type(e).__name__}")
        print(f"Message: {str(e)}")
        
        # Afficher les détails de la connexion (masquer le mot de passe)
        print("\nParamètres de connexion:")
        for key, value in conn_params.items():
            safe_value = '********' if key == 'password' else value
            print(f"{key}: {safe_value}")
        
        return False

if __name__ == "__main__":
    test_connection()
