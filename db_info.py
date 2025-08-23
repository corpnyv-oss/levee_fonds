import psycopg2
from psycopg2 import sql

def get_db_info():
    try:
        # Se connecter à la base de données postgres par défaut
        conn = psycopg2.connect(
            dbname='postgres',
            user='postgres',
            password='Root@FAPAG@2025',
            host='localhost',
            port='5432'
        )
        conn.autocommit = True
        cursor = conn.cursor()
        
        # 1. Vérifier les bases de données existantes
        print("📊 BASES DE DONNÉES DISPONIBLES:")
        cursor.execute("""
            SELECT d.datname as name,
                   pg_size_pretty(pg_database_size(d.datname)) as size,
                   pg_encoding_to_char(d.encoding) as encoding,
                   u.usename as owner
            FROM pg_database d
            JOIN pg_user u ON d.datdba = u.usesysid
            WHERE d.datistemplate = false
            ORDER BY d.datname;
        """)
        dbs = cursor.fetchall()
        for db in dbs:
            print(f"- {db[0]} (Taille: {db[1]}, Encodage: {db[2]}, Propriétaire: {db[3]})")
        
        # 2. Vérifier les connexions actives
        print("\n🔌 CONNEXIONS ACTIVES:")
        cursor.execute("""
            SELECT pid, usename, application_name, client_addr, state, query_start, 
                   age(now(), query_start) as query_age, query 
            FROM pg_stat_activity 
            WHERE datname = 'levee_fonds';
        """)
        connections = cursor.fetchall()
        if connections:
            for conn_info in connections:
                print(f"- PID: {conn_info[0]}, Utilisateur: {conn_info[1]}, App: {conn_info[2]}")
                print(f"  Adresse: {conn_info[3]}, État: {conn_info[4]}, Âge: {conn_info[6]}")
                print(f"  Requête: {conn_info[7][:100]}..." if conn_info[7] else "  Pas de requête active")
        else:
            print("Aucune connexion active sur la base 'levee_fonds'")
            
        # 3. Vérifier les extensions installées
        print("\n🧩 EXTENSIONS INSTALLÉES:")
        cursor.execute("SELECT extname, extversion FROM pg_extension;")
        for ext in cursor.fetchall():
            print(f"- {ext[0]} (v{ext[1]})")
        
        # 4. Vérifier si la base 'levee_fonds' existe et ses tables
        cursor.execute("SELECT 1 FROM pg_database WHERE datname = 'levee_fonds'")
        if cursor.fetchone():
            print("\n📦 BASE 'levee_fonds' TROUVÉE")
            
            # Se connecter à la base 'levee_fonds' pour vérifier les tables
            conn_levee = psycopg2.connect(
                dbname='levee_fonds',
                user='postgres',
                password='Root@FAPAG@2025',
                host='localhost',
                port='5432'
            )
            cursor_levee = conn_levee.cursor()
            
            # Lister les tables
            cursor_levee.execute("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public';
            """)
            tables = cursor_levee.fetchall()
            print(f"\n📋 TABLES DANS 'levee_fonds':")
            if tables:
                for table in tables:
                    print(f"- {table[0]}")
            else:
                print("Aucune table trouvée dans la base 'levee_fonds'")
                
            cursor_levee.close()
            conn_levee.close()
        else:
            print("\n❌ La base de données 'levee_fonds' n'existe pas")
            print("\nPour créer la base de données, exécutez:")
            print("CREATE DATABASE levee_fonds OWNER postgres;")
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"❌ Erreur lors de la récupération des informations: {e}")
        print("\nVérifiez que:")
        print("1. PostgreSQL est en cours d'exécution")
        print("2. Les identifiants sont corrects (utilisateur: postgres, mot de passe: Root@FAPAG@2025)")
        print("3. Le port 5432 est accessible")

if __name__ == "__main__":
    print("🔍 OBTENTION DES INFORMATIONS SUR LA BASE DE DONNÉES...\n")
    get_db_info()
    print("\n✅ Vérification terminée")
