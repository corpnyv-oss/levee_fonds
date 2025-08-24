import psycopg2

try:
    print("Tentative de connexion...")
    conn = psycopg2.connect(
        dbname='db_levee_fonds',
        user='db_levee_fonds_user',
        password='3gWX7NcyKeyLbVTGHBerEiU5d37LSBHA',
        host='dpg-d2l2ir95pdvs73a92fog-a.frankfurt-postgres.render.com',
        port='5432',
        sslmode='require'
    )
    print("✅ Connexion réussie!")
    conn.close()
except Exception as e:
    print(f"❌ Erreur: {e}")
