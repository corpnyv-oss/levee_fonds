import psycopg2

try:
    conn = psycopg2.connect(
        dbname='postgres',
        user='postgres.gezapnrpbdzwoozrvnjc',
        password='Corpnyv@0297',
        host='aws-1-eu-west-3.pooler.supabase.com',
        port='5432',
        sslmode='require',
        connect_timeout=5
    )
    
    print("✅ Connexion réussie à Supabase!")
    
    # Tester la création d'une table temporaire
    with conn.cursor() as cur:
        # Vérifier la version de PostgreSQL
        cur.execute("SELECT version();")
        version = cur.fetchone()
        print(f"📊 Version de PostgreSQL: {version[0]}")
        
        # Vérifier les extensions disponibles
        cur.execute("SELECT * FROM pg_available_extensions;")
        print("\n🔧 Extensions disponibles:")
        for ext in cur.fetchall():
            print(f"- {ext[0]} (version: {ext[1]})")
        
        # Vérifier les tables existantes
        cur.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
        """)
        tables = cur.fetchall()
        
        if tables:
            print("\n📋 Tables existantes:")
            for table in tables:
                print(f"- {table[0]}")
        else:
            print("\nℹ️ Aucune table trouvée dans le schéma public.")
    
    conn.close()
    
except Exception as e:
    print(f"\n❌ Erreur de connexion à Supabase:")
    print(f"Type d'erreur: {type(e).__name__}")
    print(f"Détails: {e}")
    
    # Aide au débogage
    print("\n🔍 Vérifiez que:")
    print("1. Vos identifiants sont corrects")
    print("2. Votre adresse IP est autorisée dans les paramètres Supabase")
    print("3. Le mot de passe est correct (attention aux caractères spéciaux)")
    print("4. Le nom d'utilisateur est complet avec la partie après 'postgres.'")
    print("5. Le port est correct (5432 par défaut)")
