import psycopg2

try:
    conn = psycopg2.connect(
        dbname='postgres',
        user='postgres',
        password='Root@FAPAG@2025',
        host='localhost',
        port='5432'
    )
    print("✅ Connexion réussie à PostgreSQL!")
    
    # Exécuter une requête simple
    cur = conn.cursor()
    cur.execute("SELECT version();")
    version = cur.fetchone()
    print(f"Version de PostgreSQL: {version[0]}")
    
    # Lister les bases de données
    cur.execute("SELECT datname FROM pg_database WHERE datistemplate = false;")
    print("\nBases de données disponibles:")
    for db in cur.fetchall():
        print(f"- {db[0]}")
    
    cur.close()
    conn.close()
    
except Exception as e:
    print(f"❌ Erreur de connexion: {e}")
