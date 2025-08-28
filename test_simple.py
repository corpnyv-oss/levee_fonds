print("Démarrage du test simple...")
try:
    import psycopg2
    print("✅ psycopg2 est bien importé")
    
    print("\nTentative de connexion à la base de données...")
    conn = psycopg2.connect(
        dbname='postgres',
        user='postgres.gezapnrpbdzwoozrvnjc',
        password='Corpnyv@0297',
        host='aws-1-eu-west-3.pooler.supabase.com',
        port=5432,
        sslmode='require'
    )
    print("✅ Connexion réussie !")
    
    with conn.cursor() as cur:
        cur.execute("SELECT version();")
        version = cur.fetchone()
        print(f"\nVersion de PostgreSQL: {version[0]}")
    
    conn.close()
    
except Exception as e:
    print(f"\n❌ Erreur: {e}")
    print("\nVérifiez que:")
    print("1. Vous êtes connecté à Internet")
    print("2. Les identifiants de la base de données sont corrects")
    print("3. Votre IP est autorisée dans les paramètres de sécurité de Supabase")
    print("4. Le service de base de données est actif sur Supabase")
