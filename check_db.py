import os
import sys
import psycopg2
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

def test_connection():
    try:
        conn = psycopg2.connect(
            dbname=os.getenv('POSTGRES_DB', 'fapag_collecte'),
            user=os.getenv('POSTGRES_USER', 'postgres'),
            password=os.getenv('POSTGRES_PASSWORD', 'Root@FAPAG@2025'),
            host=os.getenv('POSTGRES_HOST', 'localhost'),
            port=os.getenv('POSTGRES_PORT', '5432'),
            connect_timeout=5
        )
        print("✅ Connexion à PostgreSQL réussie !")
        
        # Vérifier si la base de données existe
        cur = conn.cursor()
        cur.execute("SELECT datname FROM pg_database WHERE datname = %s", 
                   (os.getenv('POSTGRES_DB', 'fapag_collecte'),))
        
        if cur.fetchone():
            print(f"✅ La base de données {os.getenv('POSTGRES_DB')} existe.")
        else:
            print(f"❌ La base de données {os.getenv('POSTGRES_DB')} n'existe pas.")
        
        # Vérifier les tables existantes
        cur.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
        """)
        tables = cur.fetchall()
        print(f"\n📋 Tables existantes ({len(tables)}):")
        for table in tables:
            print(f"- {table[0]}")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Erreur de connexion à PostgreSQL: {e}")
        return False

if __name__ == "__main__":
    print("🔍 Test de connexion à la base de données PostgreSQL...")
    if not test_connection():
        print("\n💡 Conseils de dépannage:")
        print("1. Vérifiez que PostgreSQL est bien installé et en cours d'exécution")
        print("2. Vérifiez les identifiants dans le fichier .env")
        print("3. Assurez-vous que l'utilisateur a les droits nécessaires")
        print("4. Vérifiez que le port 5432 est accessible")
        sys.exit(1)
