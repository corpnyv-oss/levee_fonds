import asyncio
import asyncpg
import ssl

async def test_supabase_connection():
    print("=== Test de connexion à Supabase avec asyncpg ===\n")
    
    # Paramètres de connexion
    conn_params = {
        'database': 'postgres',
        'user': 'postgres.gezapnrpbdzwoozrvnjc',
        'password': 'Corpnyv@0297',
        'host': 'aws-1-eu-west-3.pooler.supabase.com',
        'port': '5432',
        'ssl': 'require',
        'command_timeout': 10,
        'server_settings': {
            'application_name': 'test_connection',
            'search_path': 'public',
        }
    }
    
    try:
        print("🔍 Tentative de connexion à Supabase...")
        print(f"🌐 Hôte: {conn_params['host']}")
        print(f"📁 Base de données: {conn_params['database']}")
        print(f"👤 Utilisateur: {conn_params['user']}")
        
        # Établir la connexion
        conn = await asyncpg.connect(**conn_params)
        print("✅ Connexion réussie!")
        
        # Exécuter une requête de test
        version = await conn.fetchval('SELECT version()')
        print(f"\nℹ️  Version de PostgreSQL: {version}")
        
        # Vérifier les tables existantes
        tables = await conn.fetch("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
        """)
        
        print("\n📋 Tables disponibles:")
        for table in tables:
            print(f"- {table['table_name']}")
        
        # Fermer la connexion
        await conn.close()
        return True
        
    except Exception as e:
        print(f"\n❌ Erreur de connexion:")
        print(f"Type: {type(e).__name__}")
        print(f"Message: {str(e)}")
        
        # Suggestions de dépannage
        print("\n🔧 Suggestions de dépannage:")
        print("1. Vérifiez votre connexion Internet")
        print("2. Vérifiez que le pare-feu autorise les connexions sortantes sur le port 5432")
        print("3. Vérifiez vos identifiants de connexion")
        print("4. Vérifiez que l'adresse IP est autorisée dans les paramètres de Supabase")
        print("5. Essayez de désactiver temporairement votre pare-feu/antivirus pour les tests")
        
        return False

if __name__ == "__main__":
    asyncio.run(test_supabase_connection())
