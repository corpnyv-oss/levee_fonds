import asyncio
import asyncpg
import ssl

async def test_connection():
    print("=== Test de connexion avec asyncpg ===\n")
    
    # Paramètres de connexion
    conn_params = {
        'database': 'db_levee_fonds',
        'user': 'db_levee_fonds_user',
        'password': '3gWX7NcyKeyLbVTGHBerEiU5d37LSBHA',
        'host': 'dpg-d2l2ir95pdvs73a92fog-a.oregon-postgres.render.com',
        'port': '5432',
        'ssl': 'require',  # Forcer l'utilisation de SSL
        'command_timeout': 10,
        'server_settings': {
            'application_name': 'test_connection',
            'search_path': 'public',
        }
    }
    
    try:
        print("Tentative de connexion...")
        conn = await asyncpg.connect(**conn_params)
        print("✅ Connexion réussie!")
        
        # Exécuter une requête de test
        version = await conn.fetchval('SELECT version()')
        print(f"\nVersion de PostgreSQL: {version}")
        
        # Fermer la connexion
        await conn.close()
        return True
        
    except Exception as e:
        print(f"\n❌ Erreur de connexion:")
        print(f"Type: {type(e).__name__}")
        print(f"Message: {str(e)}")
        
        # Afficher les détails de la connexion (masquer le mot de passe)
        print("\nParamètres de connexion:")
        for key, value in conn_params.items():
            if key == 'password':
                print(f"password: ********")
            elif key == 'server_settings':
                print("server_settings: {...}")
            else:
                print(f"{key}: {value}")
        
        return False

if __name__ == "__main__":
    asyncio.run(test_connection())
