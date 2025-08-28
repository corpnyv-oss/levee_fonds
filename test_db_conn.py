import psycopg2
from psycopg2 import OperationalError
import time

def test_connection():
    print("=== Test de connexion à la base de données ===\n")
    
    # Paramètres de connexion
    db_params = {
        'dbname': 'db_levee_fonds',
        'user': 'db_levee_fonds_user',
        'password': '3gWX7NcyKeyLbVTGHBerEiU5d37LSBHA',
        'host': 'dpg-d2l2ir95pdvs73a92fog-a.oregon-postgres.render.com',
        'port': '5432'
    }
    
    try:
        print("Tentative de connexion sans SSL...")
        conn = psycopg2.connect(**db_params, sslmode='disable')
        print("✅ Connexion réussie sans SSL!")
        conn.close()
        return True
        
    except OperationalError as e:
        print(f"❌ Échec de la connexion sans SSL: {e}")
    
    try:
        print("\nTentative de connexion avec SSL...")
        conn = psycopg2.connect(
            **db_params,
            sslmode='require',
            sslrootcert='',  # Chemin vers le certificat si nécessaire
            sslcert='',
            sslkey=''
        )
        print("✅ Connexion réussie avec SSL!")
        conn.close()
        return True
        
    except OperationalError as e:
        print(f"❌ Échec de la connexion avec SSL: {e}")
    
    print("\n=== Détails de la connexion ===")
    for key, value in db_params.items():
        print(f"{key}: {'*' * 8 if key == 'password' else value}")
    
    return False

if __name__ == "__main__":
    test_connection()
