import pg8000
import ssl

def test_connection():
    print("=== Test de connexion avec pg8000 ===\n")
    
    # Paramètres de connexion
    conn_params = {
        'database': 'db_levee_fonds',
        'user': 'db_levee_fonds_user',
        'password': '3gWX7NcyKeyLbVTGHBerEiU5d37LSBHA',
        'host': 'dpg-d2l2ir95pdvs73a92fog-a.oregon-postgres.render.com',
        'port': 5432,
        'ssl_context': True,  # Activer SSL
        'timeout': 10
    }
    
    try:
        print("Tentative de connexion avec SSL...")
        conn = pg8000.connect(**conn_params)
        print("✅ Connexion réussie!")
        
        # Exécuter une requête de test
        cursor = conn.cursor()
        cursor.execute("SELECT version()")
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
