import pg8000
import ssl

def test_connection():
    print("=== Test de connexion avec pg8000 ===\n")
    
    # Paramètres de connexion
    conn_params = {
        'database': 'postgres',
        'user': 'postgres.gezapnrpbdzwoozrvnjc',
        'password': 'Corpnyv@0297',
        'host': 'aws-1-eu-west-3.pooler.supabase.com',
        'port': 5432,
        'ssl': {
            'sslmode': 'require',
            'sslrootcert': '',  # Ne pas vérifier le certificat pour les tests
        },
        'timeout': 10
    }
    
    try:
        print("🔍 Tentative de connexion...")
        print(f"🌐 Hôte: {conn_params['host']}")
        print(f"📁 Base de données: {conn_params['database']}")
        print(f"👤 Utilisateur: {conn_params['user']}")
        
        # Désactiver la vérification du certificat SSL
        ssl_context = ssl.create_default_context()
        ssl_context.check_hostname = False
        ssl_context.verify_mode = ssl.CERT_NONE
        
        # Créer la connexion
        conn = pg8000.connect(
            user=conn_params['user'],
            password=conn_params['password'],
            host=conn_params['host'],
            port=conn_params['port'],
            database=conn_params['database'],
            ssl_context=ssl_context,
            timeout=conn_params['timeout']
        )
        
        print("✅ Connexion réussie!")
        
        # Exécuter une requête de test
        cursor = conn.cursor()
        cursor.execute("SELECT version()")
        version = cursor.fetchone()
        print(f"\nℹ️  Version de PostgreSQL: {version[0]}")
        
        # Fermer la connexion
        conn.close()
        return True
        
    except Exception as e:
        print(f"\n❌ Erreur de connexion:")
        print(f"Type: {type(e).__name__}")
        print(f"Message: {str(e)}")
        
        # Suggestions de dépannage
        print("\n🔧 Suggestions de dépannage:")
        print("1. Vérifiez votre connexion Internet")
        print("2. Vérifiez que votre adresse IP est autorisée dans les paramètres de Supabase")
        print("3. Essayez de vous connecter via pgAdmin ou DBeaver pour tester la connexion")
        print("4. Vérifiez que le mot de passe et l'utilisateur sont corrects")
        print("5. Contactez le support Supabase si le problème persiste")
        
        return False

if __name__ == "__main__":
    test_connection()
