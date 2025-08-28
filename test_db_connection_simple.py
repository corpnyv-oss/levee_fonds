import psycopg2

try:
    conn = psycopg2.connect(
        dbname='postgres',
        user='postgres.gezapnrpbdzwoozrvnjc',
        password='Corpnyv@0297',
        host='aws-1-eu-west-3.pooler.supabase.com',
        port='5432',
        sslmode='require'
    )
    print("✅ Connexion à la base de données réussie!")
    
    # Exécuter une requête simple
    with conn.cursor() as cur:
        cur.execute("SELECT version();")
        version = cur.fetchone()
        print(f"Version de PostgreSQL: {version[0]}")
    
    conn.close()
    
except Exception as e:
    print(f"❌ Erreur de connexion à la base de données: {e}")
    print("Vérifiez que les informations de connexion sont correctes et que la base de données est accessible.")
