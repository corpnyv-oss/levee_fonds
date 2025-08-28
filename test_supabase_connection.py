import psycopg2
from dotenv import load_dotenv
import os

def test_supabase_connection():
    conn_params = {
        'dbname': 'postgres',
        'user': 'postgres.gezapnrpbdzwoozrvnjc',
        'password': 'Corpnyv@0297',
        'host': 'aws-1-eu-west-3.pooler.supabase.com',
        'port': '5432',
        'sslmode': 'require',
        'connect_timeout': 10
    }
    
    try:
        print("🔄 Tentative de connexion à Supabase...")
        print(f"🔗 Hôte: {conn_params['host']}")
        print(f"📁 Base de données: {conn_params['dbname']}")
        print(f"👤 Utilisateur: {conn_params['user']}")
        
        conn = psycopg2.connect(**conn_params)
        cursor = conn.cursor()
        
        # Tester la connexion
        cursor.execute("SELECT version();")
        version = cursor.fetchone()
        
        print("✅ Connexion réussie!")
        print(f"📊 Version de PostgreSQL: {version[0]}")
        
        # Vérifier les tables existantes
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
        """)
        tables = cursor.fetchall()
        
        if tables:
            print("\n📋 Tables trouvées:")
            for table in tables:
                print(f"- {table[0]}")
        else:
            print("\nℹ️ Aucune table trouvée dans le schéma public.")
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"\n❌ Erreur de connexion:")
        print(f"Type d'erreur: {type(e).__name__}")
        print(f"Détails: {e}")
        
        # Aide au débogage
        print("\n🔍 Vérifiez que:")
        print("1. Vos identifiants Supabase sont corrects")
        print("2. L'hôte est accessible depuis votre réseau")
        print("3. Le mot de passe est correct")
        print("4. La base de données existe")
        print("5. Votre IP est autorisée dans les paramètres Supabase")

if __name__ == "__main__":
    test_supabase_connection()
