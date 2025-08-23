import psycopg2
from psycopg2 import OperationalError

def test_connection():
    try:
        conn = psycopg2.connect(
            dbname='levee_fonds',
            user='postgres',
            password='Root@FAPAG@2025',
            host='localhost',
            port='5432'
        )
        print("✅ Connexion à la base de données réussie!")
        
        # Vérifier si la table utilisateur existe
        cursor = conn.cursor()
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
        """)
        tables = cursor.fetchall()
        print("\n📋 Tables disponibles dans la base de données:")
        for table in tables:
            print(f"- {table[0]}")
            
        conn.close()
    except OperationalError as e:
        print(f"❌ Erreur de connexion à la base de données: {e}")
        print("\n🔧 Vérifiez que:")
        print("1. PostgreSQL est en cours d'exécution")
        print("2. Les identifiants dans le script sont corrects")
        print("3. Le port 5432 est accessible")
        print(f"4. La base de données 'levee_fonds' existe")

if __name__ == "__main__":
    test_connection()
