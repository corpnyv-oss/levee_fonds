import psycopg2

try:
    conn = psycopg2.connect(
        dbname='db_levee_fonds',
        user='db_levee_fonds_user',
        password='3gWX7NcyKeyLbVTGHBerEiU5d37LSBHA',
        host='dpg-d2l2ir95pdvs73a92fog-a',
        port='5432',
        sslmode='require'
    )
    print("✅ Connexion réussie à la base de données!")
    conn.close()
except Exception as e:
    print(f"❌ Erreur de connexion: {e}")
