from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
import pandas as pd

def test_supabase_connection():
    print("=== Test de connexion à Supabase avec SQLAlchemy ===\n")
    
    # URL de connexion
    DATABASE_URL = "postgresql://postgres.gezapnrpbdzwoozrvnjc:Corpnyv%400297@aws-1-eu-west-3.pooler.supabase.com:5432/postgres"
    
    try:
        print("🔍 Tentative de connexion à Supabase...")
        
        # Créer le moteur SQLAlchemy avec les paramètres SSL
        engine = create_engine(
            DATABASE_URL,
            connect_args={
                'sslmode': 'require',
                'connect_timeout': 10
            }
        )
        
        # Tester la connexion
        with engine.connect() as conn:
            print("✅ Connexion réussie!")
            
            # Exécuter une requête de test
            result = conn.execute(text("SELECT version()"))
            version = result.scalar()
            print(f"\nℹ️  Version de PostgreSQL: {version}")
            
            # Récupérer la liste des tables
            print("\n📋 Liste des tables dans le schéma public:")
            tables = conn.execute(text("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public'
            """))
            
            for table in tables:
                print(f"- {table[0]}")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Erreur de connexion:")
        print(f"Type: {type(e).__name__}")
        print(f"Message: {str(e)}")
        
        # Suggestions de dépannage
        print("\n🔧 Suggestions de dépannage:")
        print("1. Vérifiez votre connexion Internet")
        print("2. Vérifiez que votre adresse IP est autorisée dans les paramètres de Supabase")
        print("3. Vérifiez que vos identifiants sont corrects")
        print("4. Essayez de vous connecter via pgAdmin ou DBeaver pour tester la connexion")
        print("5. Vérifiez les journaux Supabase pour des erreurs de connexion")
        
        return False

if __name__ == "__main__":
    test_supabase_connection()
