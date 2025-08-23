import psycopg2
from psycopg2 import sql
import os

def setup_database():
    try:
        # Se connecter à la base de données postgres par défaut
        conn = psycopg2.connect(
            dbname='postgres',
            user='postgres',
            password='Root@FAPAG@2025',
            host='localhost',
            port='5432'
        )
        conn.autocommit = True
        cursor = conn.cursor()
        
        # Vérifier si la base de données existe déjà
        cursor.execute("SELECT 1 FROM pg_database WHERE datname = 'levee_fonds'")
        exists = cursor.fetchone()
        
        if not exists:
            print("Création de la base de données 'levee_fonds'...")
            cursor.execute(sql.SQL("CREATE DATABASE {}").format(
                sql.Identifier('levee_fonds'))
            )
            print("✅ Base de données créée avec succès!")
        else:
            print("ℹ️ La base de données 'levee_fonds' existe déjà.")
        
        # Créer les extensions nécessaires si elles n'existent pas
        cursor.execute("""
            CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
            CREATE EXTENSION IF NOT EXISTS "pgcrypto";
        """)
        
        cursor.close()
        conn.close()
        
        # Tester la connexion à la nouvelle base de données
        test_connection()
        
    except Exception as e:
        print(f"❌ Erreur lors de la configuration de la base de données: {e}")

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
        conn.close()
    except Exception as e:
        print(f"❌ Impossible de se connecter à la base de données: {e}")

if __name__ == "__main__":
    print("🔧 Configuration de la base de données PostgreSQL...")
    setup_database()
    print("\nPour exécuter les migrations, utilisez :")
    print("python manage.py migrate --settings=temp_db_settings")
