import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import sys

def create_database():
    try:
        # Connexion à la base de données postgres par défaut
        conn = psycopg2.connect(
            dbname='postgres',
            user='postgres',
            password='Root@FAPAG@2025',
            host='localhost',
            port='5432'
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor()
        
        # Vérifier si la base de données existe déjà
        cursor.execute("SELECT 1 FROM pg_database WHERE datname = 'levee_fonds'")
        exists = cursor.fetchone()
        
        if not exists:
            print("Création de la base de données 'levee_fonds'...")
            cursor.execute("CREATE DATABASE levee_fonds")
            print("✅ Base de données créée avec succès!")
        else:
            print("ℹ️ La base de données 'levee_fonds' existe déjà.")
        
        cursor.close()
        conn.close()
        
        # Tester la connexion à la nouvelle base de données
        test_connection()
        
    except Exception as e:
        print(f"❌ Erreur lors de la configuration de la base de données: {e}")
        sys.exit(1)

def test_connection():
    try:
        conn = psycopg2.connect(
            dbname='levee_fonds',
            user='postgres',
            password='Root@FAPAG@2025',
            host='localhost',
            port='5432'
        )
        print("✅ Connexion à la base de données 'levee_fonds' réussie!")
        
        # Vérifier les extensions nécessaires
        cursor = conn.cursor()
        cursor.execute("""
            CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
            CREATE EXTENSION IF NOT EXISTS "pgcrypto";
        """)
        conn.commit()
        print("✅ Extensions nécessaires vérifiées/installées")
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"❌ Impossible de se connecter à la base de données: {e}")
        sys.exit(1)

if __name__ == "__main__":
    print("🔧 Configuration de la base de données PostgreSQL...")
    create_database()
    
    print("\nPour exécuter les migrations, utilisez :")
    print("python manage.py migrate --settings=minimal_settings")
