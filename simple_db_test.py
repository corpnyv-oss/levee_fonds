import psycopg2
import time

def test_connection():
    print("Tentative de connexion à la base de données...")
    try:
        conn = psycopg2.connect(
            dbname='db_levee_fonds',
            user='db_levee_fonds_user',
            password='3gWX7NcyKeyLbVTGHBerEiU5d37LSBHA',
            host='dpg-d2l2ir95pdvs73a92fog-a.frankfurt-postgres.render.com',
            port=5432,
            connect_timeout=5,
            sslmode='require'
        )
        print("✅ Connexion réussie!")
        
        # Tester une requête simple
        with conn.cursor() as cur:
            cur.execute("SELECT version();")
            version = cur.fetchone()
            print(f"Version de PostgreSQL: {version[0]}")
            
    except Exception as e:
        print(f"❌ Erreur de connexion: {e}")
        import traceback
        traceback.print_exc()
    finally:
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    print("=== Test de connexion PostgreSQL ===")
    test_connection()
